rgb_path_queue = tf.train.string_input_producer(rgb_paths, shuffle=False)
fc_path_queue = tf.train.string_input_producer(rgb_paths, shuffle=False)

rgb_img_path, contents = reader.read(rgb_path_queue)
rgb_img = tf.image.decode_jpeg(contents)
rgb_img = tf.image.convert_image_dtype(rgb_img, dtype=tf.float32)

fc_img_path, contents = reader.read(fc_path_queue)
fc_img = tf.image.decode_png(contents)
fc_img = tf.image.convert_image_dtype(fc_img, dtype=tf.float32)


rgb_paths_batch, fc_paths_batch, inputs_batch, targets_batch = tf.train.shuffle_batch([rgb_img_path, fc_img_path, input_img, target_img], a.batch_size, (a.num_preprocessing_threads+2) * a.batch_size,   a.batch_size, a.num_preprocessing_threads)
