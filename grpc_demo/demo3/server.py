from concurrent import futures
import logging
import time

import grpc
import demo_pb2
import demo_pb2_grpc

print('################################################')


class TestStreamServicer(demo_pb2_grpc.Test_StreamServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.time_sleep = 3

    def ListFeatures(self, request, context):
        loop_n = request.number  # 客户端request的数据
        i = 0
        while True:
            feature = demo_pb2.Reply(reply=str(i))
            # process()
            time.sleep(self.time_sleep)
            now = time.localtime()
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
            print('time:', now_time)
            print('send:', i)
            i += 1
            yield feature  # 以迭代器的方式返回处理的结果
            if (i == loop_n):
                break

        i = loop_n * 2
        time.sleep(self.time_sleep)
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        print('time:', now_time)
        print('send:', i)
        feature = demo_pb2.Reply(reply=str(i))
        yield feature  # 以迭代器的方式返回处理的结果

    def ListFeatures2(self, request_iter, context):
        for i in request_iter:
            yield demo_pb2.Reply(reply=str(i))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))  # 以多线程的方式监听
    demo_pb2_grpc.add_Test_StreamServicer_to_server(TestStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    print('-----------server start------------------')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
