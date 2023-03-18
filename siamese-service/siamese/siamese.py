from tensorflow.keras import Model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Input, Dot, Dropout, BatchNormalization
from tensorflow.keras.metrics import BinaryAccuracy
from tensorflow.keras.applications.resnet_v2 import ResNet152V2
from siamese import resnet50


def gen_extract_image_model(image_size):
    # resnet = ResNet152V2()
    # input_layer = resnet.get_layer(index=0).output
    # output_layer = resnet.get_layer(index=565).output
    # resnet = resnet34.gen_resnet(image_size)
    # input_layer = resnet.get_layer(index=0).output
    # features = resnet.get_layer(index=50).output
    resnet = resnet50.gen_resnet(image_size)
    input_layer = resnet.get_layer(index=0).output
    features = resnet.get_layer(index=65).output
    output_layer = Dense(1)(features)
    extract_image_model = Model(input_layer, output_layer)

    return extract_image_model


def gen_siamese(image_size):
    extract_image_model = gen_extract_image_model(image_size)

    input_1 = Input(shape=(image_size, image_size, 3))
    features_1 = extract_image_model(input_1)

    input_2 = Input(shape=(image_size, image_size, 3))
    features_2 = extract_image_model(input_2)

    consine_sim = Dot(axes=1)([features_1, features_2])
    fc_1 = Dense(1, activation='sigmoid')(consine_sim)

    siamese = Model([input_1, input_2], fc_1)

    return siamese


def gen_compiled_model(**kwargs):
    # Begin hyper params
    loss = kwargs.get('loss', 'binary_crossentropy')
    learning_rate = kwargs.get('learning_rate', 0.001)
    optimizer = kwargs.get('optimizer', SGD(learning_rate=learning_rate))
    weights_path = kwargs.get('weights_path')
    metrics = [BinaryAccuracy(
        name="binary_accuracy", dtype=None, threshold=0.8
    )]

    image_size = kwargs.get('image_size', 125)
    # End hyper params

    model = gen_siamese(image_size)
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    model.summary()

    if weights_path != None:
        model.load_weights(weights_path)

    return model
