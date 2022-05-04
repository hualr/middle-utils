from pykafka import KafkaClient


class KafkaTest(object):
    """
    测试kafka常用api
    """

    def __init__(self, host, topic):
        self._client = KafkaClient(hosts=host)
        self._topic = self._client.topics[topic.encode()]

    def simple_consumer(self, offset=0):
        """
        消费者指定消费
        :param offset:偏移量
        :return:
        """
        consumer = self._topic.get_simple_consumer(consumer_group="trademark_info")
        consumer.start()
        for message in consumer:
            if message is not None:
                print(message.offset, message.value)
                # 不commit就始终用不了
                consumer.commit_offsets()
        print("不在消费")


if __name__ == '__main__':
    host = "101.201.67.114:9092"
    topic = "topic1"
    kafka_ins = KafkaTest(host=host, topic=topic)
    kafka_ins.simple_consumer()
