import os
import math
import numpy as np
import time

import tensorflow as tf
from config import _configure_learning_rate, _configure_optimizer
from DAEZSL_semantic_network import DAEZSL_network
from load_from_tfrecord import load_list

tf.app.flags.DEFINE_float( 'adadelta_rho', 0.95, 'The decay rate for adadelta.')
tf.app.flags.DEFINE_float( 'adagrad_initial_accumulator_value', 0.1,  'Starting value for the AdaGrad accumulators.')
tf.app.flags.DEFINE_float('adam_beta1', 0.9, 'The exponential decay rate for the 1st moment estimates.')
tf.app.flags.DEFINE_float('adam_beta2', 0.999, 'The exponential decay rate for the 2nd moment estimates.')
tf.app.flags.DEFINE_float('opt_epsilon', 1.0, 'Epsilon term for the optimizer.')
tf.app.flags.DEFINE_float('ftrl_learning_rate_power', -0.5, 'The learning rate power.')
tf.app.flags.DEFINE_float( 'ftrl_initial_accumulator_value', 0.1,'Starting value for the FTRL accumulators.')
tf.app.flags.DEFINE_float( 'ftrl_l1', 0.0, 'The FTRL l1 regularization strength.')
tf.app.flags.DEFINE_float( 'ftrl_l2', 0.0, 'The FTRL l2 regularization strength.')
tf.app.flags.DEFINE_float( 'momentum', 0.9,'The momentum for the MomentumOptimizer and RMSPropOptimizer.')
tf.app.flags.DEFINE_float('rmsprop_momentum', 0.9, 'Momentum.')
tf.app.flags.DEFINE_float('rmsprop_decay', 0.9, 'Decay term for RMSProp.')
tf.app.flags.DEFINE_float( 'num_epochs_per_decay', 10.0,'Number of epochs after which learning rate decays.')
tf.app.flags.DEFINE_string( 'learning_rate_decay_type', 'exponential', 'Specifies how the learning rate is decayed.')
tf.app.flags.DEFINE_float('end_learning_rate', 0.0001, 'The minimal end learning rate used by a polynomial decay learning rate.')
tf.app.flags.DEFINE_float( 'learning_rate_decay_factor', 0.95, 'Learning rate decay factor.')

tf.app.flags.DEFINE_string('dataset_name',  'SUN', 'dataset name')
tf.app.flags.DEFINE_string('train_type',  'all', ' all or DAEZSL')
tf.app.flags.DEFINE_integer( 'gpu_id', 0, 'The GPU card to use.')
tf.app.flags.DEFINE_integer( 'batch_size', 64, 'size of batch.')
tf.app.flags.DEFINE_integer( 'shuffle', 1, 'whether to shuffle training batches')
tf.app.flags.DEFINE_float( 'init_lr', 1e-3, 'The initial learning rate.')
tf.app.flags.DEFINE_float( 'weight_decay', 0.0, 'The coefficient before weight decay regularzier.')
tf.app.flags.DEFINE_float( 'hinge_weight', 1e0, 'The weight on the hinge loss.')
tf.app.flags.DEFINE_string('optimizer',  'adam', 'dataset name')

slim = tf.contrib.slim
FLAGS = tf.app.flags.FLAGS

if FLAGS.dataset_name=='CUB':
    tfrecord_train_file = '/media/liniu/Data/tfrecord_dataset/DAEZSL/CUB_train_8855_150.tfrecord'
    tfrecord_test_file = '/media/liniu/Data/tfrecord_dataset/DAEZSL/CUB_test_2933_50.tfrecord'
elif FLAGS.dataset_name=='SUN':
    tfrecord_train_file = '/media/liniu/Data/tfrecord_dataset/DAEZSL/SUN_train_14140_707.tfrecord'
    tfrecord_test_file = '/media/liniu/Data/tfrecord_dataset/DAEZSL/SUN_test_200_10.tfrecord'
else:
    print 'dataset %s not supported!' %(FLAGS.dataset_name)
    
def _get_init_fn(checkpoint_path, checkpoint_exclude_scopes=None, checkpoint_exclude_keywords=None):
    """Returns a function run by the chief worker to warm-start the training.

    Note that the init_fn is only run when initializing the model during the very
    first global step.

    Returns:
        An init function run by the supervisor.
    """

    exclusions = []
    if checkpoint_exclude_scopes:
        exclusions = [scope.strip()  for scope in checkpoint_exclude_scopes.split(',')]

    keywords = []
    if checkpoint_exclude_keywords:
        keywords = [keyword.strip()   for keyword in checkpoint_exclude_keywords.split(',')]
        
    variables_to_restore = []
        
    model_variables = tf.get_collection(tf.GraphKeys.MODEL_VARIABLES)
    model_variables += tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'VAE')        
            
    for var in model_variables:
        excluded = False
        for exclusion in exclusions:
            if var.op.name.startswith(exclusion):
                excluded = True
                break
        for keyword in keywords:
            if keyword in var.op.name:
                excluded = True
                break
        if not excluded:
            variables_to_restore.append(var)

    if tf.gfile.IsDirectory(checkpoint_path):
        checkpoint_path = tf.train.latest_checkpoint(checkpoint_path)
    else:
        checkpoint_path = checkpoint_path

    tf.logging.info('Fine-tuning from %s' % checkpoint_path)

    return slim.assign_from_checkpoint_fn(checkpoint_path, variables_to_restore)

def _get_variables_to_train():
    """Returns a list of variables to train.

    Returns:
        A list of variables to train by the optimizer.
    """
    if FLAGS.trainable_scopes is None:
        return tf.trainable_variables()
    else:
        scopes = [scope.strip() for scope in FLAGS.trainable_scopes.split(',')]

    variables_to_train = []
    for scope in scopes:
        variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
        variables_to_train.extend(variables)
    return variables_to_train

def get_checkpoint_exclude(checkpoint_path):
    if checkpoint_path.startswith('general'):
        checkpoint_exclude_scopes= 'DAEZSL,InceptionV3/Logits,InceptionV3/AuxLogits '
        checkpoint_exclude_keywords = None #'moving_mean,moving_variance'
    else:
        checkpoint_exclude_scopes= None
        checkpoint_exclude_keywords = None #'moving_mean,moving_variance'
    return checkpoint_exclude_scopes, checkpoint_exclude_keywords
    
def main(_):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.gpu_id)
    FLAGS.num_preprocessing_threads = 10
    FLAGS.max_epoch_num = 200
    FLAGS.model_name='inception_v3'
    FLAGS.method_name = 'DAEZSL' 
    FLAGS.save_epoch_freq = 1
    
    FLAGS.train_dir='output/%s/%s/hw_%.10f_wd_%.10f' %(FLAGS.method_name, FLAGS.dataset_name,  
                                                       FLAGS.hinge_weight, FLAGS.weight_decay)
    FLAGS.checkpoint_path='general_models/%s/model.ckpt' %(FLAGS.model_name)  
    log_file_path = os.path.join(FLAGS.train_dir, 'log')
    
    if not os.path.isdir(FLAGS.train_dir):
        os.makedirs(FLAGS.train_dir)

    with tf.Graph().as_default():
        
        train_images, train_labels, train_sample_num  = load_list(tfrecord_train_file, 'train', FLAGS)     
        train_class_attributes = np.loadtxt( 'class_attributes/%s_train_class_attributes'%(FLAGS.dataset_name), np.float32) 
        train_batch_num = int(math.ceil(train_sample_num/ float(FLAGS.batch_size)))        
        
        test_images, test_labels, test_sample_num  = load_list(tfrecord_test_file, 'test', FLAGS) 
        test_class_attributes = np.loadtxt( 'class_attributes/%s_test_class_attributes'%(FLAGS.dataset_name), np.float32)
        test_batch_num = int(math.ceil(test_sample_num/ float(FLAGS.batch_size)))       
        
        output_collection, update_losses, merged = DAEZSL_network('train',  FLAGS.model_name,  train_images, train_labels,  train_class_attributes, FLAGS)       
        test_correct_arr = DAEZSL_network('test', FLAGS.model_name,  test_images, test_labels,  test_class_attributes,  FLAGS, reuse=True)
        train_batch_loss_with_decay = output_collection['total_loss_with_decay'] 

        saver = tf.train.Saver(max_to_keep=FLAGS.max_epoch_num)
        global_step = slim.create_global_step()
        
        common_lr = _configure_learning_rate(train_sample_num, global_step, FLAGS)
        optimizer = _configure_optimizer(common_lr, FLAGS)
        
        if FLAGS.train_type=='all':
            FLAGS.trainable_scopes = None
        else:
            FLAGS.trainable_scopes='DAEZSL'
            
        variables_to_train = _get_variables_to_train()
        grads_and_vars = optimizer.compute_gradients(train_batch_loss_with_decay,  variables_to_train)
        update_ops = [optimizer.apply_gradients(grads_and_vars, global_step=global_step)]
        update_ops += [update_losses]
        if FLAGS.train_type=='all':
            # update moving_mean, moving_variance for batch normalization
            update_ops += tf.get_collection(tf.GraphKeys.UPDATE_OPS) 
        
        update_op = tf.group(*update_ops)
        with tf.control_dependencies([update_op]):
            train_op = tf.identity(train_batch_loss_with_decay)        
        
        # main code
        config = tf.ConfigProto() 
        #config.gpu_options.allow_growth=True 

        with tf.Session(config=config) as sess:        
            
            train_writer = tf.summary.FileWriter(os.path.join(FLAGS.train_dir, 'train'))
                                                
            # initialization
            sess.run(tf.global_variables_initializer())

            save_check_flag = False
            test_acc_history = []
            
            with slim.queues.QueueRunners(sess):
            
                iepoch = 0
                while iepoch<FLAGS.max_epoch_num:
                    if not os.path.exists(os.path.join(FLAGS.train_dir,  'model.ckpt-%d.meta'%(iepoch))):
                        break
                    iepoch += FLAGS.save_epoch_freq
                    
                if iepoch==0:
                    checkpoint_path = FLAGS.checkpoint_path                
                elif save_check_flag==False:
                    checkpoint_path = os.path.join(FLAGS.train_dir,  'model.ckpt-%d'%(iepoch-FLAGS.save_epoch_freq))
           
                checkpoint_exclude_scopes, checkpoint_exclude_keywords = get_checkpoint_exclude(checkpoint_path)   
                init_fn=_get_init_fn(checkpoint_path, checkpoint_exclude_scopes, checkpoint_exclude_keywords)
                init_fn(sess)
                          
                while iepoch<FLAGS.max_epoch_num:         
                    #training
                    for ibatch in  range(train_batch_num):
                        
                        t1= time.time()
                        _, summary, batch_output_collection = sess.run([train_op, merged, output_collection])      
                        print 'iepoch %d: train %d/%d  %f image-per-sec ' %(iepoch, ibatch, train_batch_num, FLAGS.batch_size/(time.time()-t1))
                        #print batch_output_collection['regularizers']
                        #print batch_output_collection['regularizers']
                        #=======================================================
                        # print batch_output_collection['L2_loss']
                        # print batch_output_collection['hinge_loss']
                        # print batch_output_collection['regularizers']
                        # print batch_output_collection['feature_mask']
                        #=======================================================
                        

                    # test
                    if iepoch % FLAGS.save_epoch_freq == 0:
                        train_writer.add_summary(summary, iepoch)
                  
                        correct_num = 0
                        for ibatch  in range(test_batch_num):
                            print 'iepoch %d: test %d/%d' %(iepoch, ibatch, test_batch_num)
                            correct_arr = sess.run(test_correct_arr)   
                            correct_num += np.sum(correct_arr)
                        residual = test_batch_num*FLAGS.batch_size-test_sample_num
                        if residual>0:
                            correct_num -= np.sum(correct_arr[-residual:])      
                        test_acc = float(correct_num)/test_sample_num                                                               
                    
                        fid = open(log_file_path, 'a+')
                        cur_lr = sess.run(optimizer._lr)
                        fid.write('%d %f %f\n' %(iepoch, cur_lr,   test_acc))
                        fid.close()
                        #saver.save(sess, checkpoint_file_path)      
                              
                        test_acc_history.append(test_acc)
                        if max(test_acc_history[-10:])<max(test_acc_history):
                            break            
                                 
                    iepoch += 1                                             
                
if __name__ == '__main__':
    tf.app.run()
