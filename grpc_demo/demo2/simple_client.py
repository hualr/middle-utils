import grpc

from grpc_health.v1.health_pb2 import HealthCheckRequest
from grpc_health.v1.health_pb2_grpc import HealthStub

host = 'localhost'
port = '8080'


def run():
    conn = grpc.insecure_channel(host + ':' + port)  # 监听频道
    client = HealthStub(channel=conn)
    response_result = client.Check(HealthCheckRequest(service=""))
    print(response_result.status)


if __name__ == '__main__':
    run()