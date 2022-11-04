import redis
import random
import time
import robin_stocks.robinhood as r
import pyotp
symb = 'DOGE'
robin_username='restanford97@gmail.com'
robin_password='57m&MDTR%fGm'
robin_mfa='SHEP3N43QJ6W2X3S'
redisClient = redis.StrictRedis(host='10.0.0.16', port=6379, db=0)
def rhauth():
    totp = pyotp.TOTP(robin_mfa).now()
    r. login(robin_username,robin_password, store_session=False, mfa_code=totp)
    accountInfo0 = r.load_crypto_profile(info='user_id')
    accountInfo1 = r.load_account_profile(info='buying_power')
    print('User Id:', accountInfo0)
# rhauth()
def generate_price():
    try:
        data = range(0, ++1)
        for x in data:
            values = str(x) + '.' + str(random.uniform(0, 9))[2:5]
            print(values)
            redisClient.sadd('current_price', values)
            time.sleep(0.1)
    except:
        pass
def rh_markprice():
    try:
        y = range(0, ++1)
        for x in y:
            data = r.get_crypto_quote(symb, info='mark_price')
            redisClient.sadd('current_price', data[:6])
            print(data[:6])
            time.sleep(30)
    except:
        pass
rhauth()
while True:
    rh_markprice()
    generate_price()