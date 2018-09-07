path_queue = tf.train.slice_input_producer([rgb_paths, fc_paths], shuffle=True)
rgb_img_path = path_queue[0]
contents = tf.read_file(path_queue[0])
rgb_img = tf.image.decode_jpeg(contents)
rgb_img = tf.image.convert_image_dtype(rgb_img, dtype=tf.float32)

fc_img_path = path_queue[1]
contents = tf.read_file(path_queue[1])
fc_img = tf.image.decode_png(contents)
fc_img = tf.image.convert_image_dtype(fc_img, dtype=tf.float32)

fc_img = tf.image.resize_images(fc_img, [518, 692])
rgb_img = tf.image.resize_images(rgb_img, [256, 256])

rgb_paths_batch, fc_paths_batch, inputs_batch, targets_batch = tf.train.batch([rgb_img_path, fc_img_path, input_img, target_img], a.batch_size, a.num_preprocessing_threads, (a.num_preprocessing_threads+2) * a.batch_size)
