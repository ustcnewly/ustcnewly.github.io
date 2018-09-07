import os
import tensorflow as tf
import pandas as pd


def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def image_to_tfexample(image_data, class_id, image_format):
    return tf.train.Example(features=tf.train.Features(feature={
            'label': int64_feature(class_id),
            'image/encoded': bytes_feature(image_data),
            'image/format': bytes_feature(image_format),
    }))
    
def _convert_dataset(specs_name, filenames, class_ids, dataset_dir):
    with tf.Graph().as_default():
        config = tf.ConfigProto() 
        config.gpu_options.allow_growth=True 
        with tf.Session(config=config):
            output_filename = os.path.join(dataset_dir,  specs_name+'.tfrecord')
            if os.path.exists(output_filename):
                os.remove(output_filename)

            with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
                for i in range(len(filenames)):
                    # Read the filename:
                    print filenames[i]            
                    class_id = int( class_ids[i])
                    image_data = tf.gfile.FastGFile(filenames[i], 'rb').read()        
                    
                    example = image_to_tfexample(image_data,  class_id,  'jpg')    
                    tfrecord_writer.write(example.SerializeToString())

if __name__ == "__main__":
    
    image_list_dir = '/media/liniu/black_passport/my_projects/project_ZSLAEPR_ICCV/dataset/list/'    
    dataset_dir = '/media/liniu/Data/tfrecord_dataset/DAEZSL/'
    datasets = ['CUB', 'SUN']
    flags = ['train', 'test']
    for dataset in datasets:
        for flag in flags:
            image_list_file = os.path.join(image_list_dir,  '%s_%s_list.txt' %(dataset, flag))
            specs_name  = '%s_%s' %(dataset, flag)
           
            csv_data = pd.read_csv(image_list_file,  delimiter=' ', header=None)    
            sample_num = csv_data.shape[0]
                        
            filenames = csv_data.loc[:,0].tolist()
            class_ids = csv_data.loc[:,1].tolist()    
            class_num = max(class_ids)+1
            specs_name  = '%s_%s_%d_%d' %(dataset, flag, sample_num, class_num)
            
            _convert_dataset(specs_name,   filenames,  class_ids,  dataset_dir)
        

    
