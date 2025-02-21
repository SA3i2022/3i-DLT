#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Data_Loader import *
from data_loader_volumentations import *

# In[2]:


ims,mas=organize("/projects/salbersfester@xsede.org/Alpine Scripts/image/", "/projects/salbersfester@xsede.org/Alpine Scripts/mask/")


# In[3]:


from sklearn.model_selection import train_test_split


# In[4]:


train_image, image_valid,train_mask, mask_valid= train_test_split(ims, mas, test_size=0.30, random_state=2025)


# In[6]:


import tensorflow as tf
import tensorflow.keras as keras


# In[5]:


dataset = tf.data.Dataset.from_generator(lambda: data_generator_aug(train_image, train_mask),output_signature=(tf.TensorSpec(shape=(32,32,32,1), dtype=tf.float32),
                      tf.TensorSpec(shape=(576,576,1), dtype=tf.float32)))

dataset_validation = tf.data.Dataset.from_generator(lambda: data_generator(image_valid, mask_valid),output_signature=(tf.TensorSpec(shape=(32,32,32,1), dtype=tf.float32),
                      tf.TensorSpec(shape=(576,576,1), dtype=tf.float32)))


# In[ ]:


from unet2D import *


# In[ ]:


input_shape=(32,32,32,1)
num_classes=1
model=create_3d_unet(input_shape,num_classes)
#model.load_weights('/projects/salbersfester@xsede.org/Alpine Scripts/weights-improvement-dlover-13-0.95.hdf5')

# In[7]:


from loss_functions import dice_loss
from loss_functions import tversky_loss


# In[ ]:


optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5)
model.compile(optimizer=optimizer, loss=tversky_loss, metrics=["accuracy", dice_loss])


# In[ ]:


from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.data
import datetime


# In[ ]:


batch_size=4
# Create batched and prefetched datasets
batched_dataset = dataset.prefetch(tensorflow.data.AUTOTUNE).repeat(count=1000).batch(batch_size) #.shuffle(buffer_size=50)
validation_batched_dataset = dataset_validation.prefetch(tensorflow.data.AUTOTUNE).repeat(count=1000).batch(batch_size) #.shuffle(buffer_size=50)


# In[ ]:


filepath="weights-improvement-ds_2d_tvloss-{epoch:02d}-{val_loss}-{val_accuracy:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=False, save_freq='epoch', mode='max')

model.fit(
    batched_dataset,
    epochs=100,
    steps_per_epoch = len(train_image)//4,
    validation_data=validation_batched_dataset,
    validation_steps = len(image_valid)//4,
    callbacks=[checkpoint])

