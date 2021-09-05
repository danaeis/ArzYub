import requests
from flask import request, jsonify
import json
from bs4 import BeautifulSoup
from arzyab import db
from arzyab.models import Wallex, Nobitex
import pytz
from pytz import timezone
import datetime

try:
    import brotli
except ImportError:
    brotli = None

Data = [
        {
        'NPriceB' : 0.00000,
        'NAmountB' : 0.0,
        'NPriceS' : 0.00000,
        'NAmountS' : 0.0,
        'WPriceB' : 0.00000,
        'WAmountB' : 0.0,
        'WPriceS' : 0.00000,
        'WAmountS' : 0.0
        },
        {
        'NPriceB' : 0.00000,
        'NAmountB' : 0.0,
        'NPriceS' : 0.00000,
        'NAmountS' : 0.0,
        'WPriceB' : 0.00000,
        'WAmountB' : 0.0,
        'WPriceS' : 0.00000,
        'WAmountS' : 0.0
        }
    ]

nobitex_url=[
    'https://api.nobitex.ir/v2/orderbook/BTCIRT',
    'https://api.nobitex.ir/v2/orderbook/ETHIRT'
]
wallex_url = [
    "https://wallex.ir/api/v1/depth/btc-tmn",
    "https://wallex.ir/api/v1/depth/eth-tmn"
]

def getResponce(market, url):
    curcheck = 0
    if market == 'btc' :
        curcheck = 0
    elif market == 'eth':
        curcheck = 1

    resp = requests.get(
                url[curcheck], 
                headers={
                    'Content-Type': 'application/json',
                    }
            )
    # json_resp = json.loads(resp.text)
    # print (type(resp.text.json()))
    return resp


def wallex(market):
    json_resp = getResponce(market, wallex_url)
    print("################################################################")

    # print(type(jsonify(resp.text)))
    global Data
    if json_resp.status_code == 200 :  
        json_resp = json_resp.json()
        # print(type((json_resp)))
        # print(type(json.load(resp.text)))
        # print(type(jsonify(json_resp["asks"])))
        if market=='btc':
            Data[0]['WPriceS'] = int(json_resp["result"]["asks"][0]["price"])
            Data[0]['WAmountS'] = float(json_resp["result"]["asks"][0]["quantity"])
            Data[0]['WPriceB'] = int(json_resp["result"]["bids"][0]["price"])
            Data[0]['WAmountB'] = float(json_resp["result"]["bids"][0]["quantity"])
        elif market=='eth':
            Data[1]['WPriceS'] = int(json_resp["result"]["asks"][0]["price"])
            Data[1]['WAmountS'] = float(json_resp["result"]["asks"][0]["quantity"])
            Data[1]['WPriceB'] = int(json_resp["result"]["bids"][0]["price"])
            Data[1]['WAmountB'] = float(json_resp["result"]["bids"][0]["quantity"])
        return json_resp["result"]['asks'], json_resp["result"]['bids']

    else :
        Data[0]['WAmountB'] = 1
        Data[0]['WPriceB']  = 1
        Data[1]['WAmountB'] = 1
        Data[1]['WPriceB']  = 1
        Data[0]['WAmountS'] = 1
        Data[0]['WPriceS']  = 1
        Data[1]['WAmountS'] = 1
        Data[1]['WPriceS']  = 1
        return "error", "error"


def nobitex(market):
    json_resp = getResponce(market, nobitex_url)
    global Data
    if json_resp.status_code == 200:
        json_resp = json_resp.json()
        if market=='btc':
            Data[0]['NPriceS'] = int(json_resp["asks"][0][0])/10
            Data[0]['NAmountS'] = float(json_resp["asks"][0][1])
            Data[0]['NPriceB'] = int(json_resp["bids"][0][0])/10
            Data[0]['NAmountB'] = float(json_resp["bids"][0][1])
        elif market=='eth':
            Data[1]['NPriceS'] = int(json_resp["asks"][0][0])/10
            Data[1]['NAmountS'] = float(json_resp["asks"][0][1])
            Data[1]['NPriceB'] = int(json_resp["bids"][0][0])/10
            Data[1]['NAmountB'] = float(json_resp["bids"][0][1])

        return json_resp['asks'], json_resp['bids']
    else :
        Data[0]['NAmountB'] = 1
        Data[0]['NPriceB']  = 1
        Data[1]['NAmountB'] = 1
        Data[1]['NPriceB']  = 1
        Data[0]['NAmountS'] = 1
        Data[0]['NPriceS']  = 1
        Data[1]['NAmountS'] = 1
        Data[1]['NPriceS']  = 1
        return "error", "error"


# def Decder(url):
    # headers={
        # 'Host': 'wallex.ir',
        # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'analytics_campaign={%22source%22:%22direct%22%2C%22medium%22:null}; analytics_token=92e6bc78-e5b9-1ab6-fddd-6a383dde4465; yektanet_session_last_activity=7/18/2021; _yngt=43e8f886-68d54-4ccd0-0af17-7c1235896192a; XSRF-TOKEN=rtjjo6NCjlTxaNgtoCASs7zfc4AgSx8JgtVK6lS6; wallex_session=ehI2Svf4Xrw0pTrkc9oD1DjikFeDxzT8AIYxzOnn; analytics_session_token=f05bd49d-8061-7c13-bac8-d37a07df30de; _yngt_iframe=1',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-User': '?1',
        # 'Sec-GPC': '1',
        # 'Cache-Control': 'max-age=0'
    # }
# 
    # s=requests.Session()
    # try:
        # response = s.get(url, headers=headers)
    # except:
        # return "error"
    # return response
#    if response.status_code == 200:
#       mode = response.headers.get('Content-Encoding')
#        if "," in mode:
#            return response.text
#        if mode == "gzip":
#            return response.text
#        if brotli is not None and mode == "br":
#            data = brotli.decompress(response.content)
#            data1 = data.decode('utf-8')
#            return data1
#        return response.text
#    return "error"


# def wallex(market):
# 
    # global Data
# 
    # curcheck = 0
    # if market == 'btc' :
        # curcheck = 0
    # elif market == 'eth':
        # curcheck = 1
# 
    # 
    # resp_page = Decder(wallex_url[curcheck])
    # if (resp_page == "error"):
        # Data[0]['WAmountB'] = 1
        # Data[0]['WPriceB']  = 1
        # Data[1]['WAmountB'] = 1
        # Data[1]['WPriceB']  = 1
        # Data[0]['WAmountS'] = 1
        # Data[0]['WPriceS']  = 1
        # Data[1]['WAmountS'] = 1
        # Data[1]['WPriceS']  = 1
        # return "error", "error"
#  
    # mode = resp_page.headers.get('Content-Encoding')
    # soup = BeautifulSoup(resp_page.text, "html.parser")
    # resultsS = soup.find(id='buyers-table')
    # resultsB = soup.find(id='sellers-table')
# 
    # if resultsS is None:
        # if brotli is not None and mode == "br":
            # data = brotli.decompress(resp_page.content)
            # data1 = data.decode('utf-8')
            # page = data1
            # soup = BeautifulSoup(page, "html.parser")
            # resultsS = soup.find(id='buyers-table')
            # resultsB = soup.find(id='sellers-table')
            # print(page)
            # print("##############")
            # print(resultsS)
    # 
    # print(resultsS)
    # sellElems=[
        # {
            # 'price':0,
            # 'amount':0
        # },
    # ]
    # buyElems=[
        # {
            # 'price':0,
            # 'amount':0
        # },
    # ]
    # elements = resultsS.find_all('td', class_="value req-buy")
    # print(elements)
    # if market == 'btc' :
        # Data[0]['WAmountS'] = float(elements[0].contents[0][1:-1].replace(',',''))
        # Data[0]['WPriceS'] = int(elements[0].findNext('td').contents[0][1:-1].replace(',',''))
        # sellElems=[{'price':elements[i].findNext('td').contents[0][1:-1].replace(',',''), 'amount':elements[i].contents[0][1:-1].replace(',','')} for i in range (0,len(elements))]
# 
    # elif market=='eth':
        # Data[1]['WAmountS'] = float(elements[0].contents[0][1:-1].replace(',',''))
        # Data[1]['WPriceS'] = int(elements[0].findNext('td').contents[0][1:-1].replace(',',''))
        # sellElems=[{'price':elements[i].findNext('td').contents[0][1:-1].replace(',',''), 'amount':elements[i].contents[0][1:-1].replace(',','')} for i in range (0,len(elements))]
# 
# 
    # elementsB = resultsB.find_all('td', class_="value req-sell")
    # if market == 'btc' :
        # Data[0]['WAmountB'] = float(elementsB[0].contents[0][1:-1].replace(',',''))
        # Data[0]['WPriceB'] = int(elementsB[0].findNext('td').contents[0][1:-1].replace(',',''))
        # buyElems=[{'price':elementsB[i].findNext('td').contents[0][1:-1].replace(',',''), 'amount':elementsB[i].contents[0][1:-1].replace(',','')} for i in range (0,len(elementsB))]
# 
    # elif market=='eth':
        # Data[1]['WAmountB'] = float(elementsB[0].contents[0][1:-1].replace(',',''))
        # Data[1]['WPriceB'] = int(elementsB[0].findNext('td').contents[0][1:-1].replace(',',''))
        # buyElems=[{'price':elementsB[i].findNext('td').contents[0][1:-1].replace(',',''), 'amount':elementsB[i].contents[0][1:-1].replace(',','')} for i in range (0,len(elementsB))]
# 
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", sellElems, "&&&&&&&&&", buyElems)
    # print( Data[0] , "$$$$$$$$", Data[1], market)
    # return sellElems,buyElems
# 

def calculate_profit():
    nobrespES, nobrespEP = nobitex('eth')
    walrespES, walrespEP = wallex('eth')

    nobrespBS, nobrespBP = nobitex('btc')
    walrespBS, walrespBP = wallex('btc')

    # print( walrespES, "@@@@@@@@@", walrespBS)
    if walrespES == "error" or walrespBS == "error":
        return 0,0

    bp1 = ((Data[0]['WPriceS'] - Data[0]['NPriceB'])/Data[0]['NPriceB'])*100
    bp2 = ((Data[0]['NPriceS'] - Data[0]['WPriceB'])/Data[0]['WPriceB'])*100
    ep1 = ((Data[1]['WPriceS'] - Data[1]['NPriceB'])/Data[1]['NPriceB'])*100
    ep2 = ((Data[1]['NPriceS'] - Data[1]['WPriceB'])/Data[1]['WPriceB'])*100

    Etotalp=ep1
    if ep2 > Etotalp:
        Etotalp = ep2

    if Etotalp > 1:
        for i in range(0,5):
            utc_time = datetime.datetime.utcnow()
            tz = timezone('Asia/Tehran')
            pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)

            walcurr = Wallex(curr='eth', Sprice= int(walrespES[i]['price']),Samount= float(walrespES[i]['quantity']), Pprice=int(walrespEP[i]['price']),Pamount=float(walrespEP[i]['quantity']), date_created=utc_time)
            nobcurr = Nobitex(curr='eth', Pprice=int(nobrespEP[i][0])/10,Pamount=float(nobrespEP[i][1]),Sprice=int(nobrespES[i][0])/10,Samount=float(nobrespES[i][1]), date_created=utc_time)

            db.session.add(walcurr)
            db.session.add(nobcurr)
            db.session.commit()

    Btotalp = bp1
    if bp2>Btotalp:
        Btotalp = bp2
    if Btotalp > 1:
        for i in range(0,5):
            utc_time = datetime.datetime.utcnow()
            tz = timezone('Asia/Tehran')
            pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)

            walcurr = Wallex(curr='btc', Sprice= int(walrespBS[i]['price']),
                Samount= float(walrespBS[i]['quantity']), 
                Pprice=int(walrespBP[i]['price']),
                Pamount=float(walrespBP[i]['quantity']), date_created=utc_time)
            nobcurr = Nobitex(curr='btc', Pprice=int(nobrespBP[i][0])/10,
                Pamount=float(nobrespBP[i][1]),
                Sprice=int(nobrespBS[i][0])/10,
                Samount=float(nobrespBS[i][1]), date_created=utc_time)
            db.session.add(walcurr)
            #   db.session.commit()
            db.session.add(nobcurr)
            db.session.commit()

    # print('*******************************************')
    print(Btotalp , '&&&&&&&', Etotalp)
    # print('*******************************************')
    return Btotalp, Etotalp  

def update_data(market):
    nobitex(market)
    wallex(market)
    btc,eth = calculate_profit()
    print('*******************************************')
    print(getResponce(market, nobitex_url), '&&&&&&&', getResponce(market, wallex_url))
    print('*******************************************')
    if market=='eth':
        return float(eth)
    elif market=='btc':
        return float(btc)









# def filter_by_date():