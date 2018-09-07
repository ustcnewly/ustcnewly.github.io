import tensorflow as tf
import numpy as np
import os
import time
import csv
from ZSL_AE_config import config_ZSL_AE


# config graph
n_hidden_attr2mask = 700
n_hidden_feat2attr = 700
n_hidden = 500000
learning_rate = 1e-5
batch_size = 500
keep_prob = 1
lambda1 = 1e-5
lambda2 = 1e-5

n_feat,n_attr,n_class,_,_ = config_ZSL_AE(n_hidden_attr2mask, n_hidden_feat2attr)

# set paths
root_folder = 'liniu_ZSL_small_dataset'
train_data_folder = os.path.join(root_folder, 'train')
train_summary_folder = os.path.join(train_data_folder, 'summary')
train_checkpoint_folder = os.path.join(train_data_folder, 'checkpoint')

csv_file = os.path.join(train_data_folder, "file_duplicate_50000.csv")
fid = open(csv_file, 'r')
data_iter = csv.reader(fid,  delimiter = ',')
enqueue_size = batch_size
enqueue_data = np.zeros([enqueue_size, n_feat+n_attr+n_class], np.float32)
#===============================================================================
def prefetch():
  global enqueue_size,data_iter
  count = 0
  while(1):
    for data in data_iter:
      enqueue_data[count,:] = np.array(data)
      count = count+1
      if count==enqueue_size:
        return enqueue_data
     
    fid = open(csv_file, 'r')
    data_iter = csv.reader(fid,  delimiter = ',')
  

prefetch_data = tf.py_func(prefetch, [], tf.float32)
batch_data = tf.train.batch([prefetch_data], batch_size, shapes=[(n_feat+n_attr+n_class)], capacity=2*batch_size, enqueue_many=True)
in_x = batch_data[:,0:n_feat]
in_y = batch_data[:,n_feat+n_attr:]


with tf.name_scope('l1') as scope:
  W = tf.Variable(tf.zeros([n_feat, n_hidden]), name='weights')
  b = tf.Variable(tf.zeros([n_hidden]), name='biases')
  hidden = tf.matmul(in_x,W)+b
with tf.name_scope('l2') as scope:
  W = tf.Variable(tf.zeros([n_hidden, n_class]), name='weights')
  b = tf.Variable(tf.zeros([n_class]), name='biases')
  scores = tf.matmul(hidden,W)+b

# calculate loss
all_loss = dict({'loss': 0})

tmp_loss = tf.square(scores-in_y)
tmp_loss = tf.reduce_sum(tmp_loss, reduction_indices=[1])
all_loss['loss'] += tf.reduce_mean(tmp_loss)

correct_prediction = tf.equal(tf.argmax(scores, 1), tf.argmax(in_y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(all_loss['loss'])

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
init = tf.local_variables_initializer()
sess.run(init)

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

t_start = time.time()

for ibatch in range(100):
  
  _,train_loss = sess.run([train, all_loss['loss']])
  #batch_data = sess.run([batch_data])
  #print np.array(batch_data).shape
  print 'iter %d \n' %(ibatch)

print 'time %fs\n' %(time.time()-t_start)
coord.request_stop()
coord.join(threads)

