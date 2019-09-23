import tensorflow as tf
import os

old_v = tf.logging.get_verbosity()  #Return how much logging output will be produced. 
tf.logging.set_verbosity(tf.logging.ERROR)

from tensorflow.examples.tutorial.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot = True) 
tf.logging.set_verbosity(old_v)
#one-hot = True argument only means that, in contract to Binary representation,
#the labels will be presented in a way that only one bie will be on for
#a specifit digit. 

config = tf.ConfigProto()
#Allowing GPU memory growth
config.gpu_options.allow_growth = True
#To find out which devices your operations and tensors are assigned to, create the session
#with log_device_placement configuration option set to True. 
config.log_device_placement = True
session = tf.Session(config=config)

#Placeholders are used to feed external data into a TensorFlow graph. It allows a value to 
#be assigned later i.e. a place in the memory where we'll store a value later on. 
#%%
#Variables are used to store the state of a graph. Varaibles need a value to be initialized 

