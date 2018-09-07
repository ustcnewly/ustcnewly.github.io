import os
import tensorflow as tf
import pandas as pd

def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def image_to_tfexample(img_id, rgb_image_data, rgb_image_format, fc_image_data, fc_image_format):
    return tf.train.Example(features=tf.train.Features(feature={
            'img_id': int64_feature(img_id),
            'rgb_image/encoded': bytes_feature(rgb_image_data),
            'rgb_image/format': bytes_feature(rgb_image_format),
            'fc_image/encoded': bytes_feature(fc_image_data),
            'fc_image/format': bytes_feature(fc_image_format)
    }))
    
def _convert_dataset(specs_name, rgb_filenames, fc_filenames, dataset_dir):
    with tf.Graph().as_default():
        config = tf.ConfigProto() 
        config.gpu_options.allow_growth=True 

        output_filename = os.path.join(dataset_dir,  specs_name+'.tfrecord')
        if os.path.exists(output_filename):
            os.remove(output_filename)

        with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
            for i in range(len(rgb_filenames)):
                # Read the filename:
                print '%d/%d' %(i, len(rgb_filenames))

                rgb_image_data = tf.gfile.FastGFile(rgb_filenames[i], 'rb').read()
                fc_image_data = tf.gfile.FastGFile(fc_filenames[i], 'rb').read()
                basename = os.path.basename(rgb_filenames[i])
                basename,_ = os.path.splitext(basename)
                img_id = int(basename.split('_')[-1])
                
                example = image_to_tfexample(img_id, rgb_image_data, 'rgb', fc_image_data, 'png')
                tfrecord_writer.write(example.SerializeToString())

if __name__ == "__main__":
    
    sample_num = 40775
    stage = 'test'
   
    dataset_dir = '/media/liniu/Data/tfrecord_dataset/' 
    if not tf.gfile.Exists(dataset_dir):
        tf.gfile.MakeDirs(dataset_dir)

    rgb_img_list =  '../../list/COCO2014_rgb_%s_list_%d' %(stage, sample_num)
    fc_img_list =  '../../list/COCO2014_fc_%s_list_%d' %(stage, sample_num)
    specs_name  = 'COCO2014_%s_list_%d' %(stage, sample_num)
   
    rgb_csv_data = pd.read_csv(rgb_img_list, header=None)    
    fc_csv_data = pd.read_csv(fc_img_list, header=None)  
    rgb_filenames = rgb_csv_data.loc[:,0].tolist()
    fc_filenames = fc_csv_data.loc[:,0].tolist()    
    assert(len(rgb_filenames)==len(fc_filenames))
    
    _convert_dataset(specs_name,  rgb_filenames, fc_filenames, dataset_dir)
    

    
