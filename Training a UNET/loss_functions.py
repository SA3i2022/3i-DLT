import tensorflow as tf

def dice_loss(y_true, y_pred):
    smooth = 1e-5  # Smoothing factor to prevent division by zero
    y_true = tf.cast(y_true, dtype=y_pred.dtype)
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    dice_coefficient = (2.0 * intersection + smooth) / (union + smooth)
    dice_loss = 1.0 - dice_coefficient
    return dice_loss

#I did not write this, I do not remember where this is from, might be a gpt unclear
def tversky_loss(y_true, y_pred, alpha=0.2, beta=0.8, smooth=1e-5):
    """
    Tversky loss function for binary segmentation.
    y_true: Ground truth binary masks.
    y_pred: Predicted binary masks.
    alpha: Weight of the false positives penalty.
    beta: Weight of the false negatives penalty.
    smooth: Smoothing factor to prevent division by zero.
    """
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    # Flatten the inputs
    y_true_flat = tf.reshape(y_true, [-1])
    y_pred_flat = tf.reshape(y_pred, [-1])

    # Calculate the true positives, false positives, and false negatives
    true_positives = tf.reduce_sum(y_true_flat * y_pred_flat)
    false_positives = tf.reduce_sum((1 - y_true_flat) * y_pred_flat)
    false_negatives = tf.reduce_sum(y_true_flat * (1 - y_pred_flat))

    # Calculate the Tversky coefficient
    tversky_coefficient = (true_positives + smooth) / (true_positives + alpha * false_positives + beta * false_negatives + smooth)

    # Calculate the Tversky loss
    tversky_loss = 1.0 - tversky_coefficient

    return tversky_loss
