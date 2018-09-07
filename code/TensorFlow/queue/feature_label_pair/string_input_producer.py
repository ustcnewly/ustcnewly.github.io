import tensorflow as tf
import numpy as np
import glob
import os
import time
from ZSL_AE_config import config_ZSL_AE


# config graph
n_hidden_attr2mask = 700
n_hidden_feat2attr = 700
learning_rate = 1e-5
batch_size = 500
keep_prob = 1
lambda1 = 1e-5
lambda2 = 1e-5

n_feat,n_attr,n_class,_,n_hidden = config_ZSL_AE(n_hidden_attr2mask, n_hidden_feat2attr)

# set paths
root_folder = 'liniu_ZSL_small_dataset'
train_data_folder = os.path.join(root_folder, 'train')
train_summary_folder = os.path.join(train_data_folder, 'summary')
train_checkpoint_folder = os.path.join(train_data_folder, 'checkpoint')


csv_file_list = glob.glob(os.path.join(train_data_folder, "*.csv"))
filename_queue = tf.train.string_input_producer(csv_file_list, num_epochs=10)
reader = tf.TextLineReader()
#reader = tf.WholeFileReader()
_, value = reader.read(filename_queue)
record_defaults = np.ones((n_feat+n_attr+n_class,1)).tolist()
input_data = tf.stack(tf.decode_csv(value, record_defaults = record_defaults))

input_features = input_data[0:n_feat]
input_attributes = input_data[n_feat:n_feat+n_attr]
input_classes = input_data[n_feat+n_attr:]


in_x, in_y = tf.train.batch([input_features, input_classes], batch_size=500)

feat_dim = n_feat
cate_num = n_class

n_hidden = 500000

with tf.name_scope('l1') as scope:
  W = tf.Variable(tf.zeros([feat_dim, n_hidden]), name='weights')
  b = tf.Variable(tf.zeros([n_hidden]), name='biases')
  hidden = tf.matmul(in_x,W)+b
with tf.name_scope('l2') as scope:
  W = tf.Variable(tf.zeros([n_hidden, cate_num]), name='weights')
  b = tf.Variable(tf.zeros([cate_num]), name='biases')
  scores = tf.matmul(hidden,W)+b
  
tf.summary.histogram('score2', scores)



# calculate loss
all_loss = dict({'loss': 0})

tmp_loss = tf.square(scores-in_y)
tmp_loss = tf.reduce_sum(tmp_loss, reduction_indices=[1])
all_loss['loss'] += tf.reduce_mean(tmp_loss)

tf.summary.scalar('loss', all_loss['loss'])
correct_prediction = tf.equal(tf.argmax(scores, 1), tf.argmax(in_y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('acc', accuracy)

optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(all_loss['loss'])

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
init = tf.local_variables_initializer()
sess.run(init)

merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter('./train', sess.graph)
test_writer = tf.summary.FileWriter('./test')

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess, coord)

t_start = time.time()
i = 0
try:
    while not coord.should_stop():
        _,train_loss = sess.run([train, all_loss['loss']])
        print 'iter %d \n' %(i)
        
        i += 1
except Exception as e:
    coord.request_stop(e)
finally:
    coord.request_stop()
    coord.join(threads)

print 'time: %f s\n' %(time.time()-t_start)
