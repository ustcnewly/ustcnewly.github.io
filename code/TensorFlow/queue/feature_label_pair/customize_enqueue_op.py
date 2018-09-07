import tensorflow as tf
import numpy as np
import os
import time
import csv
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


fid = open(os.path.join(train_data_folder, "file1.csv"), 'r')

data_iter = csv.reader(fid,  delimiter = ',')
csv_data = [data for data in data_iter]
csv_data = np.asarray(csv_data)  

input_data = tf.convert_to_tensor(csv_data, tf.float32)

q = tf.FIFOQueue(capacity=5, dtypes=tf.float32) # enqueue 5 batches
# We use the "enqueue" operation so 1 element of the queue is the full batch
enqueue_op = q.enqueue(input_data)
numberOfThreads = 5
qr = tf.train.QueueRunner(q, [enqueue_op] * numberOfThreads)

tf.train.add_queue_runner(qr)
d_input = q.dequeue()
in_x = d_input[:,0:n_feat]
in_y = d_input[:,n_feat+n_attr:]


feat_dim = n_feat
cate_num = n_class

with tf.name_scope('LR') as scope:
  W = tf.Variable(tf.zeros([feat_dim, cate_num]), name='weights')
  b = tf.Variable(tf.zeros([cate_num]), name='biases')

scores = tf.matmul(in_x,W)+b
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
for i in range(100):
  _,train_loss = sess.run([train, all_loss['loss']])
  print 'iter %d \n' %(i)

coord.request_stop()
coord.join(threads)

print 'time: %f s\n' %(time.time()-t_start)
