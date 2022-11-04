import redis
import time
import os
import pyotp
import robin_stocks.robinhood as r
robin_username='restanford97@gmail.com'
robin_password='57m&MDTR%fGm'
robin_mfa='SHEP3N43QJ6W2X3S'
tokenQuan=10
robin_smb ='DOGE'
localtime = time.asctime( time.localtime(time.time()) )
redisClient = redis.Redis(host='10.0.0.16', port=6379, db=0)
def get_price():
    redisClient.sadd('buy_log', 0.0001)
    while(redisClient.scard('current_price') > 0):
        data = str('{}'.format(redisClient.spop('current_price')))
        global filtered_data
        filtered_data = float(data.replace("b", "").translate({ord("""'"""): None}))
    return float(filtered_data)
avgList = []
def get_average():
    data = str('{}'.format(redisClient.spop('buy_log')))
    avgList.append(float(data.replace("b", "").translate({ord("""'"""): None})))
    buyAvg = sum(avgList) / len(avgList)
    return float(buyAvg)
def rhauth():
    totp = pyotp.TOTP(robin_mfa).now()
    r.login(robin_username,robin_password, store_session=False, mfa_code=totp)
    accountInfo0 = r.load_crypto_profile(info='user_id')
    print('User Id:', accountInfo0)
def limitBuy():
    r.order_buy_crypto_by_quantity(robin_smb, tokenQuan, jsonify=True)
    print('~ buy order sent', '|', localtime, '|', 'price:', get_price(), '~')
def limitSell():
    r.order_sell_crypto_by_quantity(robin_smb, tokenQuan, jsonify=True)
    print('~ sell order sent', '|', localtime, '|', 'price:', get_price(), '~')
def autotrade():
    try:
        if float(get_price()) * 10.2 < float(r.load_account_profile(info='buying_power')):
            print('Buy @', float(get_price()) * 10)
            limitBuy()
            redisClient.sadd('buy_log', float(get_price()))
            pass
        elif float(get_price()) < float(get_average()):
            print('Sell @', float(get_average()))
            limitSell()
            redisClient.sadd('sell_log', float(get_price()))
            while(avgList.length() > 0):
                for x in avgList:
                    avgList.pop(0)
            pass
        else:
            print(get_price())
            pass
    except:
        pass
rhauth()
while True:
    autotrade()
    time.sleep(60)