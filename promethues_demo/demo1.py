import os
import time

from prometheus_client import Counter, CollectorRegistry, Gauge
from prometheus_client import generate_latest

registry = CollectorRegistry()
os.environ['PROMETHEUS_DISABLE_CREATED_SERIES'] = 'True'
counter = Counter("test", "test document1", ['a', 'b'], registry=registry)
counter1 = Counter("test1", "test document2", ['a', 'b'], registry=registry)
guage1 = Gauge("test3", "test document2", ['a', 'b'], registry=registry)


@guage1.labels(a='1', b='7').track_inprogress()
@guage1.labels(a='1', b='7').time()
def test():
    time.sleep(1)

if __name__ == '__main__':
    counter.labels(a='1', b='1').inc()
    counter.labels(a='1', b='1').inc()
    counter1.labels(a='1', b='1').inc()
    counter1.labels(a='1', b='1').inc()



    # 计算老老实实使用guage统计时间把
    guage1.labels(a='a',b='b').set(2)
    guage1.labels(a='a',b='c').set(1)
    guage1.labels(a='a',b='b').set(3)
    data = str(generate_latest(registry)).split('\\n')
    for i in data:
        print(i)