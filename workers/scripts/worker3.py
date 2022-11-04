import redis
import random
import time

redisClient = redis.StrictRedis(host='10.0.0.16', port=6379, db=0)
def generate_price():
    while True:
        data = range(0, 101)
        for x in data:
            values = str(x) + '.' + str(random.uniform(0, 9))[2:5]
            print(values)
            redisClient.sadd('price', values)
            time.sleep(0.2)
generate_price()