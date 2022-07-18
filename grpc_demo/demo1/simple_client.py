import grpc

from grpc_demo.demo1.hello_pb2 import request
from grpc_demo.demo1.hello_pb2_grpc import HelloWorldStub

host = 'localhost'
port = '8080'


def run():
    conn = grpc.insecure_channel(host + ':' + port)  # 监听频道
    client = HelloWorldStub(channel=conn)

    response_result = client.Test(request(text="hello world"))
    print("get "+response_result.text)


if __name__ == '__main__':
    run()