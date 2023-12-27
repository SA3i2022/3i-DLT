from prediction_cubes import uncubify
import numpy as np
import tensprflow as tf
def predict_w_model(cubed_array, model, pad_size, original_shape):
  a,c,d,e=np.shape(cubed_array)
  sav=[]
  b=range(0,a,1)
  for i in b:
    test_image=padded_array2[i:i+1]
    out=model.predict(test_image)
    sav.append(out)
  sav=np.squeeze(sav)
  seeit=sav[:,0:c-pad_size,0:d-pad_size,0:e-pad_size]
  see=uncubify(seeit, original_shape)
  return see
