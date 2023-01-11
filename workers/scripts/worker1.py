import os
import time
import redis
import pyotp
import random
import robin_stocks.robinhood as r


robin_username = ''
robin_password = ''
robin_mfa = ''
localtime = time.asctime(time.localtime(time.time()))
redisClient = redis.StrictRedis(host='10.0.0.44', port=6379, db=0)
print('Crypto:')
symb = str(input())
redisClient.sadd('symb', symb)

def rhauth():
    totp = pyotp.TOTP(robin_mfa).now()
    print(totp)
    r. login(robin_username, robin_password,
             store_session=False, mfa_code=totp)
    print('Authenticated')
def generate_price():
    try:
        data = range(0, ++1)
        for x in data:
            values = str(x) + '.' + str(random.uniform(0, 9))[2:5]
            print(localtime,':', values)
            redisClient.sadd('current_price', values)
    except:
        pass


def rh_markprice():
    try:
        y = range(0, ++1)
        for x in y:
            data = r.get_crypto_quote(symb, info='ask_price')
            redisClient.sadd('current_price', data[:6])
            print(localtime,':', data[:6])
    except:
        pass

rhauth()
#generate_price()
rh_markprice()
while True:
    rh_markprice()
#    generate_price()
    time.sleep(45)
