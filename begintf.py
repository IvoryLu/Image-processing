
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
