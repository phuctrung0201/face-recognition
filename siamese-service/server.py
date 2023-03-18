import grpc
import logging
import tensorflow as tf
import os

from concurrent import futures
from protocol import gozo_pb2, gozo_pb2_grpc
from siamese import utils


class SiameseService(gozo_pb2_grpc.SiameseServicer):
    def __init__(self):
        super(SiameseService).__init__()
        self.model = utils.get_model()

    def StoreFace(self, request, context):
        f = open('people_support_set/' + request.name + '.jpeg', 'wb')
        f.write(request.file)
        f.close()
        return gozo_pb2.StoreFaceReply(success=True)

    def Predict(self, request, context):
        labels = []
        i1s = []
        i2s = []

        i1 = utils.preprocess_image(request.file)

        l_r = {}

        ranked_res = []

        for label in os.listdir('people_support_set'):
            for _ in range(2):
                i1 = tf.image.flip_left_right(i1)
                for _ in range(4):
                    i1 = tf.image.rot90(i1)
                    f2 = 'people_support_set/' + label
                    i2 = tf.io.read_file(f2)
                    i2 = utils.preprocess_image(i2)

                    labels.append(label)
                    i1s.append(i1)
                    i2s.append(i2)

        def sort_res(r):
            return r['accuracy']

        res = self.model.predict_on_batch([tf.Variable(i1s), tf.Variable(i2s)])

        # for l, v in zip(labels, res):
        #     l_r[l] = l_r.get(l, 0) + v[0] * 10000 // 1 / 100

        # for l in l_r:
        #     ranked_res.append({'label': l.split('.')[0], 'accuracy': l_r[l]/8})

        for l, v in zip(labels, res):
            ranked_res.append({'label': l.split('.')[0], 'accuracy': v})

        ranked_res.sort(key=sort_res, reverse=True)

        return gozo_pb2.PredictReply(name=ranked_res[0]['label'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gozo_pb2_grpc.add_SiameseServicer_to_server(
        SiameseService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
