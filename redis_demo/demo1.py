import redis

if __name__ == '__main__':

    pool = redis.ConnectionPool(host='101.201.67.114', password='12345678',port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值
    r.zadd("key1",{"a":1})
    r.zadd("key1",{"b":2})
    r.zadd("key1",{"c":3})
    r.zadd("key1",{"d":1})
    print(r.zrange("key1", 0, -1))
    print(r.zrange("key1", 0, -1,withscores=True))

    for key, scores in r.zrange("key1", 0, -1, withscores=True):
        if scores < 2:
            r.zrem("key1", key)

    print(r.zrange("key1", 0, -1, withscores=True))
