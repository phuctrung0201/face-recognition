from operator import mod
from tensorflow.keras import Model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Input, Conv2D, Add, AveragePooling2D, Flatten, MaxPool2D


def gen_res_block(inputLayer, kernels, size, ifHaveAddLayer=True):
    if not ifHaveAddLayer:
        conv_1 = Conv2D(kernels, size//3, strides=2)(inputLayer)
        conv_2 = Conv2D(kernels, size, padding="same")(conv_1)
        conv_3 = Conv2D(kernels*4, size//3, padding="same")(conv_2)
        return conv_3
    conv_1 = Conv2D(kernels, size//3, padding="same")(inputLayer)
    conv_2 = Conv2D(kernels, size, padding="same")(conv_1)
    conv_3 = Conv2D(kernels*4, size//3, padding="same")(conv_2)
    add = Add()([conv_3, inputLayer])
    return add


def gen_conv2(inputLayer, ifHaveAddLayer=True):
    kernels = 64
    size = 3
    conv_1 = Conv2D(kernels, size//3, padding="same")(inputLayer)
    conv_2 = Conv2D(kernels, size, padding="same")(conv_1)
    conv_3 = Conv2D(kernels*4, size//3, padding="same")(conv_2)
    if not ifHaveAddLayer:
        return conv_3
    add = Add()([conv_3, inputLayer])
    return add


def gen_conv3(inputLayer, ifHaveAddLayer=True):
    kernels = 128
    size = 3
    return gen_res_block(inputLayer, kernels, size, ifHaveAddLayer)


def gen_conv4(inputLayer, ifHaveAddLayer=True):
    kernels = 256
    size = 3
    return gen_res_block(inputLayer, kernels, size, ifHaveAddLayer)


def gen_conv5(inputLayer, ifHaveAddLayer=True):
    kernels = 512
    size = 3
    return gen_res_block(inputLayer, kernels, size, ifHaveAddLayer)


def gen_resnet(image_size):
    input_1 = Input(shape=(image_size, image_size, 3))
    conv1_1 = Conv2D(64, 7, strides=2)(input_1)
    conv1_2 = MaxPool2D(pool_size=(3, 3), strides=2)(conv1_1)

    conv2_1 = gen_conv2(conv1_2, False)
    conv2_2 = gen_conv2(conv2_1)
    conv2_3 = gen_conv2(conv2_2)

    conv3_1 = gen_conv3(conv2_3, False)
    conv3_2 = gen_conv3(conv3_1)
    conv3_3 = gen_conv3(conv3_2)
    conv3_4 = gen_conv3(conv3_3)

    conv4_1 = gen_conv4(conv3_4, False)
    conv4_2 = gen_conv4(conv4_1)
    conv4_3 = gen_conv4(conv4_2)
    conv4_4 = gen_conv4(conv4_3)
    conv4_5 = gen_conv4(conv4_4)
    conv4_6 = gen_conv4(conv4_5)

    conv5_1 = gen_conv5(conv4_6, False)
    conv5_2 = gen_conv5(conv5_1)
    conv5_3 = gen_conv5(conv5_2)

    avg_pool = AveragePooling2D()(conv5_3)
    flatten = Flatten()(avg_pool)
    fc1000 = Dense(1000)(flatten)
    fc = Dense(10, activation='softmax')(fc1000)

    model = Model(input_1, fc)

    return model


def gen_compiled_model(**kwargs):
    # Begin hyper params
    loss = kwargs.get('loss', 'categorical_crossentropy')
    learning_rate = kwargs.get('learning_rate', 0.001)
    optimizer = kwargs.get('optimizer', SGD(learning_rate=learning_rate))
    weights_path = kwargs.get('weights_path')
    metrics = ['accuracy']
    image_size = kwargs.get('image_size', 125)
    # End hyper params

    model = gen_resnet(image_size)
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    model.summary()

    if weights_path != None:
        model.load_weights(weights_path)

    return model
