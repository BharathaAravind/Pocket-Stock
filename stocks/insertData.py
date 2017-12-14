import json
import requests
from datetime import datetime
s = '2016-02-01'
s = s + ' 00:00:00'
datetime_object = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
print datetime_object
'''
respons = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=2NWT4MKPZ594L2GF')
ll = json.loads(respons.text)
ll = ll['Time Series (Daily)']
for i in ll.keys():
    print i
'''

respons = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=2NWT4MKPZ594L2GF')
ll = json.loads(respons.text)
ll = ll['Time Series (Daily)']
for i in ll.keys():
    s = i
    s = s + ' 00:00:00'
    datetime_object = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    print ll[i]['2. high']
    #s = StockStatusModel(whichStock='Apple Inc', date=datetime_object, highPrice=ll['2. high'], lowPrice=ll['3. low'],
     #                    currentPrice=ll['4. close'])
