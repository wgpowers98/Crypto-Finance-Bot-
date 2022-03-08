import requests
from time import sleep

api = ''
def getRates(baseCurrency, assets):
    url = 'https://api.nomics.com/v1/currencies/ticker'
    payload = {'key':api,'convert':baseCurrency,'ids':assets,'interval':'1d'}
    response  = requests.get(url,params=payload)
    data = response.json()
    cryptoCurrency, cryptoPrice, cryptoTimestap = [],[],[]
    
    for assets in data:
        cryptoCurrency.append(assets['currency'])
        cryptoPrice.append(assets['price'])
        cryptoTimestap.append(assets['price_timestamp'])
    return(float(cryptoPrice[0])) #get all data


#returns multaple currencies
def getRatesMultiple(baseCurrency, assets):
    
    url = 'https://api.nomics.com/v1/currencies/ticker'
    payload = {'key':api,'convert':baseCurrency,'ids':assets,'interval':'1d'}
    response  = requests.get(url,params=payload)
    data = response.json()
    cryptoCurrency, cryptoPrice, cryptoTimestap = [],[],[]
    
    for assets in data:
        cryptoCurrency.append(assets['currency'])
        cryptoPrice.append(assets['price'])
        cryptoTimestap.append(assets['price_timestamp'])
    returnData = {'Symbol':cryptoCurrency,'Rates':cryptoPrice}
    return(returnData) #get all data