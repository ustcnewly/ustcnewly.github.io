import tensorflow as tf
import argparse
import os
import math
import time
import datetime
from GAN_conv_fc_deconv_dual import create_model_dual
from GAN_fc import create_model_fc
slim = tf.contrib.slim

parser = argparse.ArgumentParser()
parser.add_argument("--gpu",  default ='0,1', help="available gpus")
parser.add_argument("--stage",  type=int, default =1, help="coarse, fine, all")
parser.add_argument("--gan_flag",  type=int, default =1, help="1:GAN 0: regression network")
parser.add_argument("--load_type",  default ='tfrecord', help="list or tfrecord")
parser.add_argument("--network_type",  default ='fc', help="conv_fc_deconv, deconv, dual")
parser.add_argument("--channel",  default =0, type=int, help="0:R 1:G 2:B")
parser.add_argument("--train_rgb_img_list", help="list  of training rgb images")
parser.add_argument("--train_fc_img_list", help="list  of training fc images")
parser.add_argument("--test_rgb_img_list", help="list  of test rgb images")
parser.add_argument("--test_fc_img_list", help="list  of test fc images")
parser.add_argument("--nthread", type=int, default = 10,  help="num of threads to prefetch data")
parser.add_argument("--mode", default='train', choices=["train", "test", "export"])

parser.add_argument("--checkpoint", default=None, help="directory with checkpoint to resume training from or use for testing")
parser.add_argument("--checkiter", type=int, default=None, help="checkpoint model-%d")

parser.add_argument("--max_steps", type=int, help="number of training steps (0 to disable)")
parser.add_argument("--max_epochs", type=int, default = 10000, help="number of training epochs")

parser.add_argument("--nf", type=int, default=32, help="number of filters in generator and discriminator")
parser.add_argument("--batch_size", type=int, default=256, help="number of images in batch")
parser.add_argument("--shuffle",  type = int,  default =1, help="whether to shuffle training batches")
parser.add_argument("--init_lr", type=float, default=0.0001, help="initial learning rate for adam")
parser.add_argument("--beta1", type=float, default=0.5, help="momentum term of adam")
parser.add_argument("--l1_weight", type=float, default=1000.0, help="weight on L1 term for generator gradient")

# export options
parser.add_argument("--output_filetype", default="png", choices=["png", "jpeg"])
a = parser.parse_args()

a.ngf = a.nf
a.ndf = a.nf
a.gpu_ids = [int(x) for x in a.gpu.split(',')]
a.split_batch_size = int(a.batch_size/len(a.gpu_ids))

if a.network_type=='dual':
    create_model_func = create_model_dual
elif a.network_type =='fc':
    create_model_func = create_model_fc
else:
    print '%s not supported!' %(a.network_type)
    exit(-1)
    
def deprocess(image):
    with tf.name_scope("deprocess"):
        # [-1, 1] => [0, 1]
        return (image + 1) / 2
            

def save_images(a, fetches, step=None):
    image_dir = os.path.join(a.checkpoint,  "images_"+a.mode, str(a.checkiter))
    if a.mode=='test':
        test_basename = os.path.basename(a.test_rgb_img_list)
        test_basename = test_basename.replace('rgb_','')
        image_dir =os.path.join(image_dir, test_basename) 
        
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
    for i, img_id in enumerate(fetches["img_ids"]):
        if a.load_type=='tfrecord':
            name = 'COCO_train2014_%012d' %(img_id)
        else:
            name, _ = os.path.splitext(os.path.basename(img_id.decode("utf8")))        
        
        for kind in [ "outputs_coarse", "targets"]:            
            if step is not None and 'outputs' in kind:
                filename = name + "-%s-%08d.png" % (kind, step)
            else:
                filename = name + "-%s.png"%(kind)
            out_path = os.path.join(image_dir, filename)
            contents = fetches[kind][i]
            with open(out_path, "wb") as f:
                f.write(contents)


def main():
    
    if a.checkpoint is None:
        train_basename = os.path.basename(a.train_rgb_img_list)
        train_basename = train_basename.replace('rgb_','')
        param_str = 'ngf%d_ndf%d_beta1%f_l1w%f' %(a.ngf, a.ndf, a.beta1, a.l1_weight)     
        a.checkpoint = os.path.join('/media/liniu/Data/FC2RGB_output/%s/%s/%s_channel%d/'
                                    %(train_basename, a.load_type, a.network_type, a.channel),  param_str)
        if not os.path.exists(a.checkpoint):
            os.makedirs(a.checkpoint)

    if a.mode == "test":
        if a.checkpoint is None:
            raise Exception("checkpoint required for test mode")
        
    # inputs and targets are [batch_size, height, width, channels]
    model = create_model_func(a)
    steps_per_epoch = model.steps_per_epoch
    
    # set frequency    
    a.save_freq = steps_per_epoch

    outputs_coarse = deprocess(model.outputs_coarse)
    targets = deprocess(model.targets)

    def convert(image):
        return tf.image.convert_image_dtype(image, dtype=tf.uint8, saturate=True)

    # reverse any processing on images so they can be written to disk or displayed to user
    with tf.name_scope("convert_outputs"):
        converted_outputs_coarse = convert(outputs_coarse)
    with tf.name_scope("convert_targets"):
        converted_targets = convert(targets)
        
    with tf.name_scope("encode_images"):
        display_fetches = {
            "img_ids": model.img_indices,
            "outputs_coarse": tf.map_fn(tf.image.encode_png, converted_outputs_coarse, dtype=tf.string, name="output_pngs_coarse"),
            "targets": tf.map_fn(tf.image.encode_png, converted_targets, dtype=tf.string, name="target_pngs")
        }
    

    # summaries
    with tf.name_scope("outputs_summary"):
        #tf.summary.image("outputs", converted_outputs)
        tf.summary.scalar("discriminator_loss", model.discrim_loss)
        tf.summary.scalar("generator_loss_GAN_coarse", model.gen_loss_GAN_coarse)
        tf.summary.scalar("generator_loss_L1_coarse", model.gen_loss_L1_coarse)
        tf.summary.histogram("predict_fake_coarse", model.predict_fake_coarse)
        tf.summary.histogram("predict_real", model.predict_real)
        
    parameter_count = tf.reduce_sum([tf.reduce_prod(tf.shape(v)) for v in tf.trainable_variables()])
    
    saver = tf.train.Saver( tf.trainable_variables(), max_to_keep=100)

    timestr = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    logdir = os.path.join(a.checkpoint, 'logdir_%s' %(timestr)) if a.mode=='train' else None
    sv = tf.train.Supervisor(logdir=logdir, save_summaries_secs=0, saver=None)
        
    with sv.managed_session() as sess:

        print("loading model from checkpoint")
        
        if a.checkiter is not None:
            checkpoint = os.path.join(a.checkpoint, 'model-%d'%(a.checkiter))
        else:
            checkpoint = tf.train.latest_checkpoint(a.checkpoint)

        if checkpoint is None:
            last_step = -1
        else:
            last_step = int(checkpoint[checkpoint.find('model-')+6:])
            a.checkiter = last_step
            saver.restore(sess, checkpoint)
            
        print sess.run(sv.global_step)
        print 'param number: %d' %(sess.run(parameter_count))
    
        max_steps = 2**32
        if a.max_epochs is not None:
            max_steps = steps_per_epoch * a.max_epochs
        if a.max_steps is not None:
            max_steps = a.max_steps

        if a.mode == "test":
            # testing
            # at most, process the test data once
            #max_steps = min(examples.steps_per_epoch, max_steps)
            max_steps = 1
            for step in range(max_steps):
                print 'test step %d/%d' %(step, max_steps)
                results = sess.run(display_fetches)
                save_images(a, results)

        else:
            # training
            step = last_step+1
            
            while (step<max_steps):
                def should(freq):
                    return freq > 0 and ((step + 1) % freq == 0 or step == max_steps - 1)            
                
                fetches = {
                    "train": model.train,
                    "global_step": sv.global_step,
                    "discrim_loss": model.discrim_loss,
                    "gen_loss_GAN_coarse":  model.gen_loss_GAN_coarse,
                    "gen_loss_L1_coarse": model.gen_loss_L1_coarse,
                    "predict_fake_coarse": model.predict_fake_coarse,
                    "predict_real": model.predict_real
                }
                
                if should(a.save_freq):
                    fetches["summary"] = sv.summary_op
                    fetches["display"] = display_fetches
                
                #[fc_imgs, rgb_imgs] = sess.run([examples.inputs, examples.targets])
                
                start = time.time()
                results = sess.run(fetches)     
                
                # global_step will have the correct step count if we resume from a checkpoint
                train_epoch = math.ceil(step / steps_per_epoch)
                train_step = step % steps_per_epoch + 1
                rate = a.batch_size / (time.time() - start)
                print("progress  epoch %d  step %d  image/sec %0.1f " % (train_epoch, train_step, rate))
                print("gen_loss_L1_coarse", results["gen_loss_L1_coarse"])
 
                if should(a.save_freq):
                    print("recording summary")
                    sv.summary_writer.add_summary(results["summary"], step)                    
                    print("saving display images")
                    save_images(a, results["display"], step=step)
                    print("saving model")
                    saver.save(sess, os.path.join(a.checkpoint, "model"), global_step=step)
 
                if sv.should_stop():
                    break
                
                step += 1

if __name__ == '__main__':
    main()
