import numpy as np
import os

def open_npy_file(path, cap_number, channel):
    for i in os.listdir(path):
        #finding the .imgdir for the capture you are interested in 
        if cap_number and ".imgdir" in i:
            b=i
    new_path=os.path.join(path, str(b))
    for q in os.listdir(new_path):
        #finding the npy file for the channel you are interested in 
        if channel and "ImageData" in q:
            c=q
    newer_path=os.path.join(new_path, str(c))
    #opens the npy file that has your channel data in it 
    im=np.load(newer_path)
    return (im)
  
