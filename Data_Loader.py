#taken from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly and modified to load 3D image and mask pairs stored in npy
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, image_IDs, masks_IDs, batch_size=3, dim=(128,128,64), n_channels=1
                 , shuffle=False):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.masks_IDs = masks_IDs
        self.image_IDs = image_IDs
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.image_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        image_IDs_temp = [self.image_IDs[k] for k in indexes]
        mask_IDs_temp=[self.masks_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(image_IDs_temp, mask_IDs_temp)

        return X,y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.image_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, image_IDs_temp, mask_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size, *self.dim, self.n_channels))

        # Generate data
        for i in range(0,len(image_IDs_temp)):
            # Store image
            X[i] = np.expand_dims(np.load('E:/S3i/Assembled/Image_Patch/' +str(image_IDs_temp[i])),-1)

            # Store mask
            y[i] = np.expand_dims(np.load('E:/S3i/Assembled/Mask_Patch/' +str(mask_IDs_temp[i])),-1)

        return X, y
