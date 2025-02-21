import numpy as np
from unet2D import *
from prediction_cubes import *
from predict import *
import tensorflow as tf
from tifffile import imread 
import matplotlib.pyplot as plt
import SBAccess
import SBSupport
import patchify

input_shape=(608,608,1)
num_classes=1
model2d=create_2d_unet(input_shape, num_classes)

model2d.load_weights(r"C:\Users\3i\Myo\weights-improvement-ds_2d_tvloss-62-0.3268111050128937-0.86.hdf5")
imt = SBSupport.get_array(0, 0)
imt=np.squeeze(imt)
np.shape(imt)
pad1=pad_3D(labels_16, (256, 1216, 1216))

sav=[]
for i in range(0,256,1):
    cutup=patchify(np.squeeze(pad1[i,:,:]), (608,608),608) 
    ah,be,ce,de=np.shape(cutup)
    a=range(0,ah,1)
    b=range(0,be,1)
    for z in a:
        for w in b:
            test_image=np.squeeze(cutup[z:z+1,w:w+1,:,:])
            test_image=np.expand_dims(test_image,0)
            test_image=test_image/np.max(test_image)
            #test_image=test_image.astype(np.float32)
            out=np.squeeze(model2d.predict(test_image))
            cutup[z,w,:,:]=out
    see=unpatchify(cutup, (1216, 1216))
    sav.append(see)
