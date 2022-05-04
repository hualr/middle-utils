import queue
import time

from pykafka import KafkaClient


class KafkaTest(object):
    """
    测试kafka常用api
    """

    def __init__(self, host, topic):
        self._client = KafkaClient(hosts=host)
        self._topic = self._client.topics[topic.encode()]

    def producer_partition(self):
        """
        生产者分区查看，主要查看生产消息时offset的变化
        """
        partitions = self._topic.partitions
        print("查看所有分区:", partitions)

        earliest_offset = self._topic.earliest_available_offsets()
        print("获取最早可用的offset:", earliest_offset)

        last_offset = self._topic.latest_available_offsets()
        print("最近可用的offset:", last_offset)

        # 同步生产消息
        p = self._topic.get_producer(sync=True)
        p.produce(str(time.time()).encode())

        # 查看offset的变化
        last_offset_new = self._topic.latest_available_offsets()
        print("最新最近可用的offset:", last_offset_new)

    def producer_designated_partition(self):
        """
        往指定分区写消息，如果要控制打印到某个分区,
        需要再获取生产者的时候指定选取函数，
        并且再生成消息的时候额外指一个key
        """

        def assign_patition(pid, key):
            """
            指定特定分区，这里测试写入第一个分区(id=0)
            :param: 分区列表
            """
            print("为消息分配分区partition:", pid, key)
            return pid[0]

        # sync ( bool ) – 对生产的调用是否应该在返回之前等待消息发送。
        # 如果为True，则如果交付给 kafka 失败，则会从produce()引发异常
        # partitioner 分区器
        p = self._topic.get_producer(sync=True, partitioner=assign_patition)
        p.produce(str(time.time()).encode(), partition_key=b"partition_key_0")

    def async_produce_message(self):
        """
        异步生产消息，消息会被推到一个队列里面，
        另外一个线程会在队列中消息大小满足一个阈值(min_queued_messages)
        或到达一段时间(linger_ms)后统一发送，默认5s
        :return:
        """
        last_offset = self._topic.latest_available_offsets()
        print("最近的偏移量offse=", last_offset)

        # 记录最初的偏移量
        old_offset = last_offset[0].offset[0]
        p = self._topic.get_producer(sync=False, partitioner=lambda pid, key: pid[0])
        p.produce(str(time.time()).encode())
        s_time = time.time()
        while True:
            last_offset = self._topic.latest_available_offsets()
            print("最近可用的offset=", last_offset)
            if last_offset[0].offset[0] != old_offset:
                e_time = time.time()
                print("cont time = ", e_time - s_time)
                break
            time.sleep(1)

    def get_produce_message_report(self):
        """
        查看异步发送消息报告，默认会等待5秒后才能获得报告
        :return:
        """
        last_offset = self._topic.latest_available_offsets()
        print('最近的偏移量offset=', last_offset)
        # delivery_reports 获取消息的传递确认
        p = self._topic.get_producer(sync=False, delivery_reports=True, partitioner=lambda pid, key: pid[0])
        p.produce(str(time.time()).encode())
        s_time = time.time()
        delivery_report = p.get_delivery_report()  # 必须设置delivery_reports=True才能获取反馈
        e_time = time.time()
        print(f'等待{e_time - s_time}s, 递交报告{delivery_report}')
        last_offset = self._topic.latest_available_offsets
        print('最近的偏移量offset=', last_offset)

    def get_produce_message_report_exc(self):
        message = "test message test message1"
        # 生产环境，为了达到高吞吐量，要采用异步的方式，通过delivery_reports =True来启用队列接口；
        last_offset = self._topic.latest_available_offsets()
        print("最近的偏移量offset=", last_offset)
        producer = self._topic.get_producer(sync=False, delivery_reports=True)
        producer.produce(bytes(message.encode()))
        last_offset = self._topic.latest_available_offsets()
        print("最近的偏移量offset=", last_offset)
        try:
            print("get info,直接运行速度太快，msg无法获取，直接报异常了")
            msg, exc = producer.get_delivery_report(block=False)
            print("msg", msg)
            if exc is not None:
                print(f'Failed to deliver msg {msg.partition_key}: {repr(exc)}')
            else:
                print(f'Successfully delivered msg {msg.partition_key}')

        except queue.Empty:
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    host = "101.201.67.114:9092"
    topic = "topic1"
    kafka_ins = KafkaTest(host=host, topic=topic)
    # kafka_ins.producer_partition()
    # kafka_ins.producer_designated_partition()
    # kafka_ins.async_produce_message()
    # kafka_ins.get_produce_message_report()
    kafka_ins.get_produce_message_report_exc()
