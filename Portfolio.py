import DB
import CryptoData as Crypto
import datetime
import time

#check the current worth of a users portfolio
def pullUserPortfolioBalance(_user):
    #Formats username as string
    User = str(_user)
    #Pulls users current share amount of the coin
    try:
        data = DB.Crypto_ReturnAllCurrency(User)
        cryptoLenth = len(data['Symbol'])
        conCat = ''
        #Counter
        x = 0
        Total = 0
        #adds all currencys to one string
        while x != cryptoLenth:
            conCat += f"{data['Symbol'][x]}, "
            x = x + 1
        #removes last 2 charaters
        conCat = conCat[:-2]
        #runs multaple prices
        cryptoReturn  = Crypto.getRatesMultiple('USD',conCat)
        x = 0
        while x != cryptoLenth:
            #generates a total (crypto price * Share)
            Total += float(cryptoReturn['Rates'][x]) * float(DB.Crypto_CheckCurrency(User,cryptoReturn['Symbol'][x]))
            x = x + 1
        time.sleep(1)
        #Returns users total value
        return(Total + DB.UserBalance(User))
    except KeyError:
        #if user has no currencies just their USD balance is returned
        return(DB.UserBalance(User))


