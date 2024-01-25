import numpy as np
import scipy as sp
from scipy import ndimage
from tifffile import imread
from tifffile import imwrite
import matplotlib.pyplot as plt
from stardist.models import StarDist2D
from stardist.plot import render_label
from csbdeep.utils import normalize
from csbdeep.io import save_tiff_imagej_compatible
import tensorflow as tf
import scipy.io as sio
import mat73

def star_slice(image_t):
    model = StarDist2D.from_pretrained('2D_versatile_fluo')       
    for q in range (0,z):
        imgnewz=image_t[q,:,:]
        labelz, _ = model.predict_instances(normalize(imgnewz))
        label_spacez.append(labelz)
    for w in range (0,y):
        imgnewy=image_t[:,w,:]
        labely, _ = model.predict_instances(normalize(imgnewy))
        label_spacey.append(labely)
    for e in range (0,x):
        imgnewx=image_t[:,:,e]
        labelx, _ = model.predict_instances(normalize(imgnewx))
        label_spacex.append(labelx)
    label_arrayz=np.dstack(label_spacez)
    label_arrayy=np.dstack(label_spacey)
    label_arrayx=np.dstack(label_spacex)
    return(label_arrayz, label_arrayy, label_arrayx)

def Refine(iteration_number, array_z, array_y, array_x):
    ref_spacez=[]
    ref_spacey=[]
    ref_spacex=[]
    for t in range(0,50):
        labeledz=array_z[:,:,t]
        values=np.unique(labeledz)
        values= values.tolist()
        split_list=[]
        for w in values:
            split=np.where(labeledz != w, 0, labeledz)
            spl=np.where(split>1, 1, split)
            split_list.append(spl)
        bigger=[]
        for u in range(0,len(split_list)):
            dil=sp.ndimage.morphology.binary_dilation(split_list[u], structure=None, iterations=iteration_number, mask=None, output=None, border_value=0, origin=0, brute_force=False)
            dila=dil.astype(int)
            bigger.append(dila)
        grand=sum(bigger)
        cut=np.where(grand >1, 0, grand)
        bin_labz=np.where(labeledz > 1, 1, labeledz)
        bin_maskerz=cut*bin_labz
        ref_spacez.append(bin_maskerz)
    for p in range(0,250):
        labeledy=array_y[:,:,p]
        values=np.unique(labeledy)
        values= values.tolist()
        split_list=[]
        for w in values:
            split=np.where(labeledy != w, 0, labeledy)
            spl=np.where(split>1, 1, split)
            split_list.append(spl)
        bigger=[]
        for o in range(0,len(split_list)):
            dil=sp.ndimage.morphology.binary_dilation(split_list[o], structure=None, iterations=iteration_number+1, mask=None, output=None, border_value=0, origin=0, brute_force=False)
            dila=dil.astype(int)
            bigger.append(dila)
        grand=sum(bigger)
        cut=np.where(grand >1, 0, grand)
        bin_laby=np.where(labeledy > 1, 1, labeledy)
        bin_maskery=cut*bin_laby
        ref_spacey.append(bin_maskery)
    for a in range(0,250):
        labeledx=array_x[:,:,a]
        values=np.unique(labeledx)
        values= values.tolist()
        split_list=[]
        for w in values:
            split=np.where(labeledx != w, 0, labeledx)
            spl=np.where(split>1, 1, split)
            split_list.append(spl)
        bigger=[]
        for d in range(0,len(split_list)):
            dil=sp.ndimage.morphology.binary_dilation(split_list[d], structure=None, iterations=iteration_number+1, mask=None, output=None, border_value=0, origin=0, brute_force=False)
            dila=dil.astype(int)
            bigger.append(dila)
        grand=sum(bigger)
        cut=np.where(grand >1, 0, grand)
        bin_labx=np.where(labeledx > 1, 1, labeledx)
        bin_maskerx=cut*bin_labx
        ref_spacex.append(bin_maskerx)
    ref_spacez=np.dstack(ref_spacez)
    ref_spacez2=np.swapaxes(ref_spacez,0,2)
    ref_spacez3=np.swapaxes(ref_spacez2,1,2)
    ref_spacey=np.dstack(ref_spacey)
    ref_spacey2=np.swapaxes(ref_spacey,1,2)
    ref_spacex=np.dstack(ref_spacex)
    return(ref_spacez3, ref_spacey2, ref_spacex)

def Put_Together(array1,array2,array3):
    neat=refz*refy
    neat2=refz*refx
    neat3=neat+neat2
    return neat3


