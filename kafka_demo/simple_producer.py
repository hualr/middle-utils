from pykafka import KafkaClient


class KafkaProducer(object):
    """
    最基础的API使用
    """

    def __init__(self, host, topic):
        self._client = KafkaClient(hosts=host)
        self._topic = self._client.topics[topic.encode()]

    def producer_partition(self):
        with self._topic.get_sync_producer() as producer:
            for i in range(4):
                producer.produce(bytes(f"test message{str(i ** 2)}", encoding='utf-8'))
        print("finish send")


if __name__ == '__main__':
    host = "101.201.67.114:9092"
    topic = "topic1"
    kafka_ins = KafkaProducer(host=host, topic=topic)
    kafka_ins.producer_partition()
