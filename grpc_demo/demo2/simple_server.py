import time
from concurrent import futures

import grpc
from grpc_health.v1.health import HealthServicer
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server

sleep_interval = 60 * 60 * 24
host = 'localhost'
port = '8080'




def server():
    # 定义服务器并设置最大连接数,corcurrent.futures是一个并发库，类似于线程池的概念
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))  # 创建一个服务器

    add_HealthServicer_to_server(HealthServicer(), grpc_server)  # 在服务器中添加派生的接口服务（自己实现了处理函数）
    grpc_server.add_insecure_port(host + ':' + port)  # 添加监听端口
    grpc_server.start()  # 启动服务器
    try:
        while True:
            time.sleep(sleep_interval)
    except KeyboardInterrupt:
        grpc_server.stop(0)  # 关闭服务器


if __name__ == '__main__':
    server()
