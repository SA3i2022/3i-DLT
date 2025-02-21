import numpy as np
import os
import albumentations as A


transform = A.Compose([
    A.ElasticTransform(alpha=150,sigma=50,p=.4),
    A.GaussNoise(std_range=(0.1, 0.2), p=.4),
    A.HorizontalFlip(p=.5),
    A.RandomBrightnessContrast(p=.4),
])

def data_generator_2D_aug(original_dir, mask_dir):
    original_files = original_dir
    mask_files = mask_dir
    original_files.sort()
    mask_files.sort()

    for original_file, mask_file in zip(original_files, mask_files):
        original_array = np.load(original_file)
        
        #original_array=original_array[0:32,0:32,0:32]
        original_array=original_array/np.max(original_array)
        original_array=original_array.astype(np.float32)
        #original_array=np.expand_dims(original_array, axis= -1)
        mask_array = np.load(mask_file)
        
       #mask_array=mask_array[0:32,0:32,0:32]
        mask_array=mask_array/1
        mask_array=mask_array.astype(np.float32)
        #mask_array=np.expand_dims(mask_array, axis= -1)
        
        transformed = transform(image=original_array, mask=mask_array)
        transformed_image = transformed['image']
        transformed_mask = transformed['mask']
        original_array=np.expand_dims(transformed_image, axis= -1)
        mask_array=np.expand_dims(transformed_mask, axis= -1)


        yield original_array, mask_array
        
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