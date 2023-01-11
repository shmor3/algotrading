import redis
import time
import os
import pyotp
import robin_stocks.robinhood as r

robin_username = ''
robin_password = ''
robin_mfa = ''
localtime = time.asctime(time.localtime(time.time()))
redisClient = redis.Redis(host='10.0.0.44', port=6379, db=0)

def rhauth():
    totp = pyotp.TOTP(robin_mfa).now()
    r.login(robin_username, robin_password, store_session=False, mfa_code=totp)
    global robin_smb
    robin_smb = str('{}'.format(redisClient.spop('symb'))).replace("b", "").translate({ord("""'"""): None})
    global tokenQuan
    tokenQuan = int((float(r.load_account_profile(info='buying_power')) * 0.90))
def get_price():
    while (redisClient.scard('current_price') > 0):
        data = str('{}'.format(redisClient.spop('current_price')))
        global filtered_data
        filtered_data = float(data.replace(
            "b", "").translate({ord("""'"""): None}))
    return float(filtered_data)
avgList = []
global lastBuy
lastBuy = ''
def get_average():
    while (redisClient.scard('buy_log') > 0):
        data = str('{}'.format(redisClient.spop('buy_log')))
        avgList.append(
            float(data.replace("b", "").translate({ord("""'"""): None})))
        buyAvg = sum(avgList) / len(avgList)
        redisClient.sadd('buy_Avg', float(str(buyAvg)[:6]))
        global lastBuy
        lastBuy = float((str(buyAvg)[:5]))
def limitBuy():
    global robin_smb
    global tokenQuan
    r.order_buy_crypto_by_quantity(robin_smb, tokenQuan, jsonify=True)
    print('Buy :', tokenQuan, '|', localtime)
def limitSell():
    global robin_smb
    global tokenQuan
    r.order_sell_crypto_by_quantity(robin_smb, tokenQuan, jsonify=True)
    print('Sell:', tokenQuan, '|', localtime)
def autotrade():
    global lastBuy
    global tokenQuan
    try:
        if (redisClient.scard('buy_Avg') == 0):
            if True:
                limitBuy()
                redisClient.sadd('buy_log', float(get_price()))
                get_average()
                pass
            else:
                pass
        elif float(r.get_crypto_quote(symb, info='bid_price')) > (lastBuy + 0.003):
            limitSell()
            redisClient.spop('buy_Avg')
            while (avgList.length() > 0):
                for x in avgList:
                    avgList.pop(0)
            pass
        else:
            pass
    except:
        pass
rhauth()
while True:
    autotrade()
    time.sleep(60)