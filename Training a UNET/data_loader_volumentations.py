import numpy as np
import os
from volumentations import *


def organize(image_dir, mask_dir):
    part1=[]
    for i in range(0,len(os.listdir(image_dir))):
        im1=image_dir +str(os.listdir(image_dir)[i])
        part1.append(im1)
    part2=[]
    for i in range(0,len(os.listdir(mask_dir))):
        im2=mask_dir +str(os.listdir(mask_dir)[i])
        part2.append(im2)
    return part1, part2

def get_augmentation():
    return Compose([
        ElasticTransform((0, 0.40), interpolation=1, p=.4),
        RandomGamma(gamma_limit=(50, 120), p=.4),
        GaussianNoise(var_limit=(0, 0.02), p=.4),
        Flip(0, p=0.5),
        Flip(1, p=0.5),
        Flip(2, p=0.5),
        RandomRotate90((1, 2), p=0.5)],p=1.0) 

def data_generator_aug(original_dir, mask_dir):
    original_files = original_dir
    mask_files = mask_dir
    #original_files.sort()
    #mask_files.sort()

    for original_file, mask_file in zip(original_files, mask_files):
        original_array=np.load(original_file)
        #original_array=original_array[0:32,0:32,0:32]
        original_array=original_array.astype(np.float32)/np.max(original_array)
        #original_array=np.expand_dims(original_array, axis= -1)
        mask_array=np.load(mask_file)
        #mask_array=mask_array[0:32,0:32,0:32]
        mask_array=mask_array.astype(np.float32)/1
        data={'image': original_array, 'mask': mask_array}
        #mask_array=np.expand_dims(mask_array, axis= -1)
        aug = get_augmentation()
        aug_data=aug(**data)
        img, lbl = np.clip(aug_data['image'],0,1), aug_data['mask']
        img=np.expand_dims(img, axis= -1)
        lbl=np.expand_dims(lbl, axis= -1)
        yield img, lbl
        