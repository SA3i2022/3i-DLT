import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, BatchNormalization, ReLU

def create_2d_unet(input_shape, num_classes):
    # Contracting path
    inputs = tf.keras.Input(input_shape)
    conv1 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
    conv1 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(conv1)
    b1 = tf.keras.layers.BatchNormalization()(conv1)
    r1 = tf.keras.layers.ReLU()(b1)
    pool1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(r1)

    conv2 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(pool1)
    conv2 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(conv2)
    b2 = tf.keras.layers.BatchNormalization()(conv2)
    r2 = tf.keras.layers.ReLU()(b2)
    pool2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(r2)

    conv3 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(pool2)
    conv3 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(conv3)
    b3 = tf.keras.layers.BatchNormalization()(conv3)
    r3 = tf.keras.layers.ReLU()(b3)
    pool3 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(r3)

    # Bottom
    conv4 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(pool3)
    b4 = tf.keras.layers.BatchNormalization()(conv4)
    r4 = tf.keras.layers.ReLU()(b4)
    conv4 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(r4)

    # Expanding path
    up5 = tf.keras.layers.UpSampling2D(size=(2, 2))(conv4)
    up5 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(up5)
    up5 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(up5)
    merge5 = tf.keras.layers.concatenate([conv3, up5], axis=-1)
    merge5 = tf.keras.layers.BatchNormalization()(merge5)
    merge5 = tf.keras.layers.ReLU()(merge5)

    up6 = tf.keras.layers.UpSampling2D(size=(2, 2))(merge5)
    up6 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(up6)
    up6 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(up6)
    merge6 = tf.keras.layers.concatenate([conv2, up6], axis=-1)
    merge6 = tf.keras.layers.BatchNormalization()(merge6)
    merge6 = tf.keras.layers.ReLU()(merge6)

    up7 = tf.keras.layers.UpSampling2D(size=(2, 2))(merge6)
    up7 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(up7)
    up7 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(up7)
    merge7 = tf.keras.layers.concatenate([conv1, up7], axis=-1)
    merge7 = tf.keras.layers.BatchNormalization()(merge7)
    merge7 = tf.keras.layers.ReLU()(merge7)

    # Output
    outputs = tf.keras.layers.Conv2D(num_classes, 1, activation='sigmoid')(merge7)

    # Create the model
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model