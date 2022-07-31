from kafka import KafkaConsumer, KafkaProducer


def consumer():
    consumer = KafkaConsumer('my_topic', group_id='group2', bootstrap_servers=['101.201.67.114:9092'])

    while True:
        msg = consumer.poll(timeout_ms=1000)
        if not msg or not msg.values():
            print('暂时没有消息')
        else:
            print(msg.values())


if __name__ == '__main__':
    consumer()
