import imp
import tensorflow as tf

from siamese import siamese

WEIGHTS_PATH = 'siamese/weights.h5'
IMAGE_SIZE = 125


def get_model():
    model = siamese.gen_siamese(IMAGE_SIZE)
    model.load_weights(WEIGHTS_PATH)
    return model


def preprocess_image(imgFile):
    image = tf.io.decode_jpeg(imgFile)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, [125, 125])
    return image
