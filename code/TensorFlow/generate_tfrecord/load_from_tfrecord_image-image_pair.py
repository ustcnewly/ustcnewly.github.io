import os
import tensorflow as tf
import collections
import math
slim = tf.contrib.slim

Examples = collections.namedtuple("Examples", "img_indices, inputs, targets, count, steps_per_epoch")

def list2tfrecord(rgb_path, tfrecord_dir='/media/liniu/Data/tfrecord_dataset/'): 
    basename = os.path.basename(rgb_path)
    basename = basename.replace('rgb_', '')
    return os.path.join(tfrecord_dir, basename+'.tfrecord')

_ITEMS_TO_DESCRIPTIONS = {
        'img_id': 'image id',
        'rgb_image': 'RGB images',
        'fc_image': 'FlatCam images'
}

def preprocess(image):
    with tf.name_scope("preprocess"):
        # [0, 1] => [-1, 1]
        return image * 2 - 1
    
def get_slim_dataset(tfrecord_file, sample_num):
    
    reader = tf.TFRecordReader

    keys_to_features = {
            'img_id': tf.FixedLenFeature([], tf.int64, default_value=tf.zeros([], dtype=tf.int64)),
            'rgb_image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'rgb_image/format': tf.FixedLenFeature((), tf.string, default_value='jpg'),
            'fc_image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'fc_image/format': tf.FixedLenFeature((), tf.string, default_value='png'),
    }

    items_to_handlers = {
            'img_id':  slim.tfexample_decoder.Tensor('img_id'),
            'rgb_image': slim.tfexample_decoder.Image('rgb_image/encoded', 'rgb_image/format'),
             'fc_image': slim.tfexample_decoder.Image('fc_image/encoded', 'fc_image/format'),
    }

    decoder = slim.tfexample_decoder.TFExampleDecoder(
            keys_to_features, items_to_handlers)
    
    return slim.dataset.Dataset(
            data_sources=tfrecord_file,
            reader=reader,
            decoder=decoder,  
            num_samples=sample_num,
            items_to_descriptions=_ITEMS_TO_DESCRIPTIONS)
    
def load_list(a):

    if a.mode=='train':
        tfrecord_file = list2tfrecord(a.train_rgb_img_list)
    else:
        tfrecord_file = list2tfrecord(a.test_rgb_img_list)
        
    basename = os.path.basename(tfrecord_file)
    basename, _ = os.path.splitext(basename)
    sample_num = int(basename.split('_')[-1])
    
    with tf.name_scope("load_images"): 
    
        dataset = get_slim_dataset(tfrecord_file, sample_num)
        
        provider = slim.dataset_data_provider.DatasetDataProvider(dataset, shuffle=(a.mode=='train' and a.shuffle==1),
                common_queue_capacity=32 * a.batch_size, common_queue_min=16 * a.batch_size)
        
        [img_id, ori_img, fc_img] = provider.get(['img_id', 'rgb_image', 'fc_image'])
        
        ori_img = tf.image.convert_image_dtype(ori_img, dtype=tf.float32)
        rgb_img = tf.cond(tf.equal(tf.shape(ori_img)[2],1), lambda:  tf.image.grayscale_to_rgb(ori_img), lambda: ori_img)
        
        fc_img = tf.image.convert_image_dtype(fc_img, dtype=tf.float32)
        
        if a.network_type=='deconv':
            if a.channel>=0:
                fc_img = tf.slice(fc_img, [0,0,int(a.channel)], [518, 692, 1])
        else:
            crop_size = 512
            offset = [(518-crop_size)/2+1, (692-crop_size)/2+1]
            fc_img = tf.image.crop_to_bounding_box(fc_img, int(offset[0]), int(offset[1]), crop_size, crop_size)
            if a.channel>=0:
                fc_img = tf.slice(fc_img, [0,0,int(a.channel)], [crop_size, crop_size, 1])
        
        if a.channel>=0:
            rgb_img = tf.slice(rgb_img, [0,0,int(a.channel)], [256, 256, 1])
                          
        input_img = preprocess(fc_img)
        target_img = preprocess(rgb_img)

        if a.channel==-1:
            if a.network_type=='deconv':
                input_img.set_shape([518, 692, 3])
            else:
                input_img.set_shape([512, 512, 3])
                
            target_img.set_shape([256, 256, 3])

        img_indices, inputs_batch, targets_batch = tf.train.batch([img_id, input_img, target_img], a.batch_size,   
                                                                          a.nthread, (a.nthread+2) * a.batch_size)
        
        #batch_queue = slim.prefetch_queue.prefetch_queue([img_indices,  inputs_batch, targets_batch], capacity=10)
        #img_indices, inputs_batch, targets_batch = batch_queue.dequeue()
        
        steps_per_epoch = int(math.ceil(sample_num/ a.batch_size))
    
        return Examples(
            img_indices=img_indices,
            inputs=inputs_batch,
            targets=targets_batch,
            count=sample_num,
            steps_per_epoch=steps_per_epoch,
        )
