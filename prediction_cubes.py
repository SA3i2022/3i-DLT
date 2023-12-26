def cubify(arr, newshape):
    oldshape= np.array(arr.shape)
    repeats= (oldshape / newshape).astype(int)
    tmpshape= np.column_stack([repeats, newshape]).ravel()
    order= np.arange(len(tmpshape))
    order= np.concatenate([order[::2], order[1::2]])
    # newshape must divide oldshape evenly or else ValueError will be raised
    return arr.reshape(tmpshape).transpose(order).reshape(-1, *newshape)

def pad_3D(array, target):
  target_size= target
  original_array= array

  pad_widths= [(0, target_size[i] - original_array.shape[i]) for i in range(original_array.ndim)]
  padded_array = np.pad(original_array, pad_widths, mode='constant')
  return padded_array

def uncubify(arr, oldshape):
    N, newshape= arr.shape[0], arr.shape[1:]
    oldshape= np.array(oldshape)    
    repeats= (oldshape / newshape).astype(int)
    tmpshape= np.concatenate([repeats, newshape])
    order= np.arange(len(tmpshape)).reshape(2, -1).ravel(order='F')
    return arr.reshape(tmpshape).transpose(order).reshape(oldshape)
  

    
