from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp
from config import  *

api_key = apikey
username = username
pwd = pwd
smartApi = SmartConnect(api_key)
token = token
totp=pyotp.TOTP(token).now()
correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)
# print(data)
authToken = data['data']['jwtToken']
refreshToken = data['data']['refreshToken']
feedToken = smartApi.getfeedToken()
# print("Feed-Token :", feedToken)
res = smartApi.getProfile(refreshToken)
# print("Res:", res)
smartApi.generateToken(refreshToken)
res=res['data']['exchanges']


# orderparams = {
#     "variety": "NORMAL",
#     "tradingsymbol": "SBIN-EQ",
#     "symboltoken": "26000",
#     "transactiontype": "BUY",
#     "exchange": "NSE",
#     "ordertype": "LIMIT",
#     "producttype": "INTRADAY",
#     "duration": "DAY",
#     "price": "19500",
#     "squareoff": "0",
#     "stoploss": "0",
#     "quantity": "1"
# }
# orderid = smartApi.placeOrder(orderparams)
# print("PlaceOrder", orderid)

# modifyparams = {
#     "variety": "NORMAL",
#     "orderid": orderid,
#     "ordertype": "LIMIT",
#     "producttype": "INTRADAY",
#     "duration": "DAY",
#     "price": "19500",
#     "quantity": "1",
#     "tradingsymbol": "SBIN-EQ",
#     "symboltoken": "26000",
#     "exchange": "NSE"
# }
# smartApi.modifyOrder(modifyparams)
# print("Modify Orders:",modifyparams)

# smartApi.cancelOrder(orderid, "NORMAL")

orderbook=smartApi.orderBook()

tradebook=smartApi.tradeBook()

rmslimit=smartApi.rmsLimit()

pos=smartApi.position()

holdings=smartApi.holding()

allholdings=smartApi.allholding()

exchange = "NSE"
tradingsymbol = "Nifty Bank"
symboltoken = 99926009
ltp=smartApi.ltpData("NSE", "Nifty Bank", "99926009")

mode="FULL"
exchangeTokens= {
 "NSE": [
 "99926009"
 ]
 }
marketData=smartApi.getMarketData(mode, exchangeTokens)
# print("111: ", marketData)

exchange = "NSE"
searchscrip = "Nifty Bank"
searchScripData = smartApi.searchScrip(exchange, searchscrip)
# print("222: ", searchScripData)

# params = {
#     "exchange": "NSE",
#     "oldproducttype": "DELIVERY",
#     "newproducttype": "MARGIN",
#     "tradingsymbol": "SBIN-EQ",
#     "transactiontype": "BUY",
#     "quantity": 1,
#     "type": "DAY"

# }

# convertposition=smartApi.convertPosition(params)

# gttCreateParams = {
#     "tradingsymbol": "SBIN-EQ",
#     "symboltoken": "26000",
#     "exchange": "NSE",
#     "producttype": "MARGIN",
#     "transactiontype": "BUY",
#     "price": 100000,
#     "qty": 10,
#     "disclosedqty": 10,
#     "triggerprice": 200000,
#     "timeperiod": 365
# }
# rule_id = smartApi.gttCreateRule(gttCreateParams)

# gttModifyParams = {
#     "id": rule_id,
#     "symboltoken": "26000",
#     "exchange": "NSE",
#     "price": 19500,
#     "quantity": 10,
#     "triggerprice": 200000,
#     "disclosedqty": 10,
#     "timeperiod": 365
# }
# modified_id = smartApi.gttModifyRule(gttModifyParams)

# cancelParams = {
#     "id": rule_id,
#     "symboltoken": "26000",
#     "exchange": "NSE"
# }

# cancelled_id = smartApi.gttCancelRule(cancelParams)

# gttdetails=smartApi.gttDetails(rule_id)

# smartApi.gttLists('List of status', '<page>', '<count>')

candleParams={
     "exchange": "NSE",
     "symboltoken": "99926009",
     "interval": "FIFTEEN_MINUTE",
     "fromdate": "2023-11-24 14:15",
     "todate": "2023-11-24 15:30"
}
candledetails = smartApi.getCandleData(candleParams)
# print("333: ", candledetails['data'])
for data in candledetails['data']:
    print(data)


# qParam ="your uniqueorderid"
# data = smartApi.individual_order_details(qParam)

# params = {
#     "positions": [{
#         "exchange": "NSE",
#         "qty": 1500,
#         "price": 0,
#         "productType": "CARRYFORWARD",
#         "token": "154388",
#         "tradeType": "SELL"
#     }]
# }
# # margin_api_result=smartApi.getmarginApi(params)
# # print(margin_api_result)

# terminate=smartApi.terminateSession('Your client code')

# # Websocket Programming

from SmartApi.smartWebSocketV2 import SmartWebSocketV2

AUTH_TOKEN = authToken
API_KEY = api_key
CLIENT_CODE = username
FEED_TOKEN = feedToken
# correlation_id = "abc123"
action = 1
mode = 1

token_list = [
    {
        "exchangeType": 1,
        "tokens": ["26000","1594"]
    }
]
token_list1 = [
    {
        "action": 0,
        "exchangeType": 1,
        "tokens": ["26000"]
    }
]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

def on_data(wsapp, message):
    logger.iNSE("Ticks: {}".format(message))
    close_connection()

def on_open(wsapp):
    logger.iNSE("on open")
    some_error_condition = False
    if some_error_condition:
        error_message = "Simulated error"
        if hasattr(wsapp, 'on_error'):
            wsapp.on_error("Custom Error Type", error_message)
    else:
        sws.subscribe(correlation_id, mode, token_list)
        # sws.unsubscribe(correlation_id, mode, token_list1)

def on_error(wsapp, error):
    logger.error(error)

def on_close(wsapp):
    logger.iNSE("Close")

def close_connection():
    sws.close_connection()


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()