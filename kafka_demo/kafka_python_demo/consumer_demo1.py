from kafka import KafkaConsumer, KafkaProducer



def consumer():
    consumer = KafkaConsumer('my_topic', group_id='group2', bootstrap_servers=['101.201.67.114:9092'])
    for msg in consumer:
        print('%s',msg.value)

if __name__ == '__main__':
    consumer()
