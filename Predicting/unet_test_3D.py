import numpy as np
from UNET import *
from prediction_cubes import *
from predict import *
import tensorflow as tf
from tifffile import imread 
import matplotlib.pyplot as plt
import socket
import SBAccess
import SBSupport


input_shape=(32,32,32,1)
num_classes=1
model=create_3d_unet(input_shape, num_classes)
model.summary()

model.load_weights(r'C:\Users\3i\Myo\weights-improvement-ds_3d_tvloss-99-0.09981132298707962-0.98.hdf5')

imt = SBSupport.get_array(0, 0)
imt=np.squeeze(imt)
np.shape(imt)

pad1=pad_3D(imt, (384, 1248, 1248))

cutup=patchify(pad1, (32,32,32),32)
np.shape(cutup)

ah,be,ce,de,eh,ef=np.shape(cutup)
sav=[]
a=range(0,ah,1)
b=range(0,be,1)
c=range(0,ce,1)
for z in a:
    for w in b:
        for x in c:
            test_image=np.squeeze(cutup[z:z+1,w:w+1,x:x+1,:,:,:])
            test_image=np.expand_dims(test_image,0)
            test_image=test_image/np.max(test_image)
            #test_image=test_image.astype(np.float32)
            out=np.squeeze(model.predict(test_image))
            cutup[z,w,x,:,:,:]=out
see=unpatchify(cutup, (384, 1248, 1248)

               
