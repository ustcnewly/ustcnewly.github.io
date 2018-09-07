import os
import tensorflow as tf
slim = tf.contrib.slim

_ITEMS_TO_DESCRIPTIONS = {
        'label': 'start from 0',
        'image': 'RGB image',
}
    
def get_slim_dataset(tfrecord_file, sample_num):
    
    reader = tf.TFRecordReader

    keys_to_features = {
            'label': tf.FixedLenFeature([], tf.int64, default_value=tf.zeros([], dtype=tf.int64)),
            'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/format': tf.FixedLenFeature((), tf.string, default_value='jpg')
    }

    items_to_handlers = {
            'label':  slim.tfexample_decoder.Tensor('label'),
            'image': slim.tfexample_decoder.Image('image/encoded', 'image/format'),
    }

    decoder = slim.tfexample_decoder.TFExampleDecoder(
            keys_to_features, items_to_handlers)
    
    return slim.dataset.Dataset(
            data_sources=tfrecord_file,
            reader=reader,
            decoder=decoder,  
            num_samples=sample_num,
            items_to_descriptions=_ITEMS_TO_DESCRIPTIONS)
    
def load_list(tfrecord_file, mode, FLAGS):
    
    basename = os.path.basename(tfrecord_file)
    basename, _ = os.path.splitext(basename)
    sample_num = int(basename.split('_')[-2])
    
    with tf.name_scope("load_images"): 
    
        dataset = get_slim_dataset(tfrecord_file, sample_num)
        
        provider = slim.dataset_data_provider.DatasetDataProvider(dataset, shuffle=(mode=='train' and FLAGS.shuffle==1),
                common_queue_capacity=32 * FLAGS.batch_size, common_queue_min=16 * FLAGS.batch_size)
        
        [img, label] = provider.get(['image', 'label'])        
        img = tf.image.convert_image_dtype(img, dtype=tf.float32)
        img = tf.cond(tf.equal(tf.shape(img)[2],1), lambda:  tf.image.grayscale_to_rgb(img), lambda: img)
        img.set_shape([299, 299, 3])
        
     
        img_batch, label_batch = tf.train.batch([img, label], FLAGS.batch_size,   
                                                                          FLAGS.num_preprocessing_threads, (FLAGS.num_preprocessing_threads+2) * FLAGS.batch_size)
        
        return img_batch, label_batch, sample_num
