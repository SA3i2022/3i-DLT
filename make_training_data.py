import numpy as np
import patchify

def make_training_data(input_image, input_mask, save_image, save_mask, patch_size, step_size):
    image=np.load(input_image)
    mask=np.load(input_mask)
    a,b,c=patch_size
    patcha=patchify.patchify(image, patch_size, step=step_size)
    un,deux,trois,_,_,_=np.shape(patcha)
    patchb=patchify.patchify(mask, patch_size, step=step_size)
    comp=np.zeros(patch_size)
    for i in range(0,un):
        for q in range(0,deux):
            for r in range(0,trois):
                sets=patchb[i,q,r,0:a,0:b,0:c]
                if np.all(sets==comp):
                #this is to prevent writting a cube that is just all zeros 
                    continue 
                else:
                    line=input_image.split('/')[-1]
                    index = line.find('.npy')
                    output_line = line[:index] + '_' +str(i)+'_'+str(q)+'_'+str(r)+line[index:]
                    np.save(str(save_image)+str(output_line), sets)
                    
                    sets2=patcha[i,q,r,0:a,0:b,0:c]
                    line2=input_mask.split('/')[-1]
                    index2=line2.find('.npy')
                    output_line2=line2[:index2] + '_' +str(i)+'_'+str(q)+'_'+str(r)+line2[index2:]
                    np.save(str(save_mask)+str(output_line2), sets2)
