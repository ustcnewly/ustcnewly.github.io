import tensorflow as tf

class ImageReader(object):

    def __init__(self):
        # Initializes function that decodes RGB JPEG data.
        self._img_path = tf.placeholder(dtype=tf.string)
        contents = tf.read_file(self._img_path)
        self.img = tf.image.decode_jpeg(contents)
        
    def read_image_dims(self, sess, image_path):
        img = sess.run(self.img, feed_dict={self._img_path: image_path})
        return img.shape
    

def check_img_list(filenames):
    with tf.Graph().as_default():
        image_reader = ImageReader()
        config = tf.ConfigProto() 
        config.gpu_options.allow_growth=True 
        with tf.Session(config=config) as sess:
            for i in range(len(filenames)):             
                img_shape = image_reader.read_image_dims(sess, filenames[i])


if __name__ == "__main__":
    
    rgb_paths = file('img_list').readlines()   
    rgb_paths = [item.strip() for item in rgb_paths]
    check_img_list(rgb_paths)


    
