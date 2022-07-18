import json

from kafka import KafkaConsumer, KafkaProducer


def producer():
    producer = KafkaProducer(bootstrap_servers=['101.201.67.114:9092'],value_serializer=(lambda v: json.dumps(v).encode('utf-8')))
    message = {
        "天空的蓝色": 'blue'
    }
    bytesDict = bytes('{}'.format(message), 'utf-8')
    # future = producer.send('my_topic', key='my_key', value=message, partition=0,)

    # result = future.get(timeout=10)
    # print(result)
    producer.send('fizzbuzz', {'foo': 'bar'})


if __name__ == '__main__':
    producer()