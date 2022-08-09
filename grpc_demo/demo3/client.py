from __future__ import print_function

import logging
import time

import grpc
import demo_pb2
import demo_pb2_grpc


def guide_list_features(stub):
    num = 10
    req = demo_pb2.Number(number=num)
    # 相当于我调用他一次 然后他处理批量 我这边慢慢接收
    features = stub.ListFeatures(req)  # request

    for feature in features:  # 流式返回的结果
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        print('time:', now_time)
        print('receive', feature.reply)


def build_req(nums):
    for num in nums:
        yield demo_pb2.Number(number=num)


def guide_list_features2(stub):
    # 相当于我调用他一次 然后他处理批量 我这边慢慢接收
    features = stub.ListFeatures2(build_req([10,9,8]))  # request

    for feature in features:  # 流式返回的结果
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        print('time:', now_time)
        print('receive', feature.reply)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.Test_StreamStub(channel)
        # print("-------------- GetFeature --------------")
        # guide_get_feature(stub)
        print("-------------- ListFeatures --------------")

        # print("-------------- RecordRoute --------------")
        # guide_record_route(stub)
        # print("-------------- RouteChat --------------")
        # guide_route_chat(stub)

        # guide_list_features(stub)
        guide_list_features2(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
