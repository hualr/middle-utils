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
        partitions = self._topic.partitions
        print("查看所有分区partitions=", partitions)
        last_offset = self._topic.latest_available_offsets()
        print("最近的偏移量offset=", last_offset)
        consumer = self._topic.get_simple_consumer(consumer_group="trademark_info",
                                                   partitions=[partitions[0]])  # 选择一个分区进行消费
        offset_list = consumer.held_offsets
        print("当前消费者分区offset情况{}".format(offset_list))  # 消费者拥有的分区offset的情况
        consumer.reset_offsets([(partitions[0], offset)])  # 设置offset偏移值
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        offset = consumer.held_offsets  # 返回从分区 id 到每个分区的持有偏移量的映射
        print("当前消费者分区offset情况{}".format(offset_list))  # 返回从分区 id 到每个分区的持有偏移量的映射

    def balance_consumer(self, offset=0):
        """
        使用balance consumer 去消费 kafka
        :param offset:
        :return:
        """
        # managed=True 设置后，使用新式reblance分区方法，不需要使用zk，
        # 而False是通过zk来实现reblance的需要使用zk
        consumer = self._topic.get_balanced_consumer(consumer_group="trademark_info", managed=True)
        partitions = self._topic.partitions
        print("分区 {}".format(partitions))
        earliest_offsets = self._topic.earliest_available_offsets()
        print("最早可用offset {}".format(earliest_offsets))
        last_offsets = self._topic.latest_available_offsets()
        print("最近可用offset {}".format(last_offsets))
        offset = consumer.held_offsets
        print("当前消费者分区offset情况{}".format(offset))
        while True:
            msg = consumer.consume()
            offset = consumer.held_offsets
            print("{}, 当前消费者分区offset情况{}".format(msg.value.decode(), offset))


if __name__ == '__main__':
    host = "101.201.67.114:9092"
    topic = "topic1"
    kafka_ins = KafkaTest(host=host, topic=topic)
    kafka_ins.simple_consumer()
