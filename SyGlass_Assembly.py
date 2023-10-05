import numpy as np
from tifffile import imread

def SyGlassROIAssembly(folder_dir, ch):
    folder_dirt = folder_dir
    it=[]
    for images in os.listdir(folder_dirt):
        substring = "Image"
        if substring in images:
            sa=imread(folder_dirt+ '/'+images)
            sa=sa[:,:,ch]
            sa=np.expand_dims(sa, 2)
        else:
            sa=imread(folder_dirt+ '/'+images)
            sa=np.expand_dims(sa, 2)         
        it.append(sa)
    ist=np.concatenate((it[0],it[1]),axis=2)
    for i in range(2,len(os.listdir(folder_dirt))):
        ist=np.concatenate((ist,it[i]),axis=2)
    np.shape(ist)
    b=np.swapaxes(ist,0,1)
    return b
