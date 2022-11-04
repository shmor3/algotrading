import redis
import time

redisClient = redis.StrictRedis(host='10.0.0.16', port=6379, db=0)
def get_price():
    while(redisClient.scard('price') > 0):
        data = str('{}'.format(redisClient.spop('price')))
        global filtered_data
        filtered_data = float(data.replace("b", "").translate({ord("""'"""): None}))
    return float(filtered_data)
def autotrade():
    if get_price() < 30.00:
        print('Buy')
        autotrade()
        time.sleep(0.2)
    elif get_price() > 70.00:
        print('Sell')
        autotrade()
        time.sleep(0.2)
    else:
        print(get_price())
        autotrade()
autotrade()