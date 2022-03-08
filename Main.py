#Devloper: Will Powers
#Description: Main file that recieves Discord commands and send out the data.
#Version 1.3
#Server Startup Message
Message = """
***Happy New Year!***
The Finance Game has now been updated to version 1.3. 
---Changes---
* With the update the user can now enter .Buy [symbol] All to have their entire USD balance placed into that currency at current exchange rate price.
--RoadMap--
* The next update will focus on visual improvements and the implementation of user created crypto mutual funds which players will be able to join. More to come soon!
"""

import discord
from discord.ext import commands
import DB
import CryptoData as Crypto
import datetime
import time
import Portfolio

client = commands.Bot(command_prefix = '.')


@client.command()
async def News(ctx):
    formatted = f""" ```apache
    {Message}
    ```"""
    #Startup Message
    await ctx.send(f"Server: {formatted}")

#Allows user to create their account
@client.command()
async def Register(ctx):
    if (DB.userExists(ctx.message.author)):
        await ctx.send(f"{ctx.message.author} you already have an account")
    else:
        DB.createUser(str(ctx.message.author),1000)
        await ctx.send(f"you are now registered {ctx.message.author}")

#await ctx.send("")
#Places buy on users account
#@client.command()
#async def SendDM(ctx):
#    user = ctx.message.author
#    await user.send('data')



@client.command()
async def Buy(ctx,*,Data):
    try:
        #pulls Discord username unformatted
        _user = ctx.message.author
        #Formats username as string
        User = str(_user)
        #splits context into price and symbol
        splitData = Data.split(' ')
        Symbol = splitData[0]
        
        Shares = splitData[1]
        
        #1. Check if user exists
        if DB.userExists(User):
        #2. Pull trade price
            print(Shares)
            tradePrice = Crypto.getRates('USD',Symbol)
            #3. Check user's balance
            userBalance = DB.UserBalance(User)
            
            if Shares == 'All' or Shares == 'all':
                #Divides balance by currency
                ajShare = userBalance / tradePrice
                #Set veriable to new price
                Shares = float(ajShare)
                print(Shares)
            #Makes sure shares request are more than 0
            if Shares > 0:
            #4. Check if user can afford the requested trade
                if userBalance >= tradePrice * Shares:
                    #5. Remove balance from user's account
                    newBalance = userBalance - tradePrice * Shares
                    DB.UpdateUserBalance(User,newBalance)
                    #6 Check if user has currency
                    if DB.Crypto_CheckCurrency(User,Symbol) != 0:
                        #here if user already has currency
                        #1.1. Pull current shares
                        currentShares = DB.Crypto_CheckCurrency(User,Symbol) 
                        #1.2. Add new shares 
                        DB.Crypto_UpdateCurrency(User,Symbol,currentShares + Shares)
                        await ctx.send('Trade Placed: Please check DM for confirmation')

                        Confirmation = (f"""
                        --------------------------Trade Confirmation------------------------------
                        Time Stamp: {datetime.datetime.now()}
                        Shares Bought: {Shares}
                        New Share Amount: {currentShares + Shares}
                        Previous Balance USD: ${userBalance}
                        Trade Cost USD : $ {tradePrice * Shares}
                        New Balance USD: ${newBalance}
                        """)
                        
                        await _user.send(Confirmation)
                        #sleep 
                        time.sleep(1)
                    else:    
                        DB.Crypto_AddCurrency(User,Symbol,Shares)
                        await ctx.send('Trade Placed: Please check DM for confirmation')
                        Confirmation = (f"""
                        --------------------------Trade Confirmation------------------------------
                        Time Stamp: {datetime.datetime.now()}
                        Shares Bought: {Shares}
                        New Share Amount: {Shares}
                        Previous Balance USD: ${userBalance}
                        Trade Cost USD : $ {tradePrice * Shares}
                        New Balance USD: ${newBalance}
                        """)
                        await _user.send(Confirmation)
                        #sleep 
                        time.sleep(1)
                    #6. add the trade to users portfolio
                #Trade is more than users balance
                else:
                    await ctx.send("This trade exceeeds your balance")
            else:
                await ctx.send("Amount must be greater than 0")
            #User does not exist        
        else:
            await ctx.send("You must create an account to use this feture. Type .Register to create an account")
    #General error catcher
    except Exception:
        print('Error')
        #await ctx.send("For any ajustments please message GasPoweredCoconut#7593")



@client.command()
async def Sell(ctx,*,Data):
    try:
        #pulls Discord username unformatted
        _user = ctx.message.author
        #Formats username as string
        User = str(_user)
        #splits context into price and symbol
        splitData = Data.split(' ')
        Symbol = splitData[0]
        SellShares = float(splitData[1])
        #Check if user exists
        if DB.userExists(User):
            #Pull current amount of shares
            shareAmount = DB.Crypto_CheckCurrency(User,Symbol)
            #Check user has enough shares #4. Check if user already has currency
            if SellShares < shareAmount and SellShares > 0:
                #Run Share price
                sharePrice = Crypto.getRates('USD',Symbol)
                #get share value USD
                shareValue = sharePrice * SellShares
                #Pull users current balance
                userBalance  = DB.UserBalance(User)
                #Add balance to user's account
                DB.UpdateUserBalance(User,userBalance + shareValue)
                #7. remove the trade from users portfolio
                DB.Crypto_UpdateCurrency(User,Symbol,shareAmount-SellShares)
                await ctx.send('Trade Placed: Please check DM for confirmation')
                Confirmation = (f"""
                        --------------------------Sell Trade Confirmation------------------------------
                        Time Stamp: {datetime.datetime.now()}
                        Shares Sold: {SellShares}
                        New Share Amount: {shareAmount - SellShares}
                        Previous Balance USD: ${userBalance}
                        Value Added USD: $ {shareValue}
                        New Balance USD: ${userBalance + shareValue}
                        """)
                        
                await _user.send(Confirmation)
                #sleep 
                time.sleep(1)



            #If user plans to sell all coins
            elif  SellShares == shareAmount:
                #Run Share price
                sharePrice = Crypto.getRates('USD',Symbol)
                #get share value USD
                shareValue = sharePrice * SellShares
                #Pull users current balance
                userBalance  = DB.UserBalance(User)
                #Add balance to user's account
                DB.UpdateUserBalance(User,userBalance + shareValue)
                #7. remove the currency from users portfolio
                DB.Crypto_RemoveCurrency(User,Symbol)
                await ctx.send('Trade Placed: Please check DM for confirmation')
                Confirmation = (f"""
                        --------------------------Sell Trade Confirmation------------------------------
                        Time Stamp: {datetime.datetime.now()}
                        Shares Sold: {SellShares}
                        New Share Amount: 0
                        Previous Balance USD: ${userBalance}
                        Value Added USD: $ {shareValue}
                        New Balance USD: ${userBalance + shareValue}
                        """)
                await _user.send(Confirmation)
                #sleep 
                time.sleep(1)


            #user tries to sell negative shares
            elif SellShares < 0:
                await ctx.send("You cannot enter a negative amount")
            #User tries to sell more shares than they own
            else:
                await ctx.send("You do not own this many shares")
        #User does not have an account
        else:
            await ctx.send('You must create an account to use this feture. Type .Register to create an account')
    #General error catcher
    except Exception:
        await ctx.send("Oops an error occured. For any ajustments please message GasPoweredCoconut#7593") 



@client.command()
async def checkValue(ctx,*,Symbol):
    try:
        #pulls Discord username
        User = str(ctx.message.author)
        #Check if user exists
        if DB.userExists(User):
            #Pulls users current share amount of the coin
            userShares = DB.Crypto_CheckCurrency(User,Symbol)
            if userShares != 0:
                #Check Currency value
                currencyValue = Crypto.getRates('USD',Symbol)
                await ctx.send(f"{User} Your USD balance of {Symbol} is currently ${userShares * currencyValue}")
            else:
                await ctx.send("This currency is not in your portfolio")
        else:
            await ctx.send('You must create an account to use this feture. Type .Register to create an account')
    #General error catcher
    except Exception:
        await ctx.send("Oops an error occured. For any ajustments please message GasPoweredCoconut#7593")     


@client.command()
async def Report(ctx):
    try:
        #Pulls unformatted discord username
        _user = ctx.message.author
        #Formats username as string
        User = str(_user)
        #Check if user exists
        if DB.userExists(User):
            #Pulls users current share amount of the coin
            data = DB.Crypto_ReturnAllCurrency(User)
            cryptoLenth = len(data['Symbol'])
            conCat = ''
            #Counter
            x = 0
            Total = 0
            #sets up portfolio string
            Portfolio = f"------Portfolio------\n|Time Stamp: {datetime.datetime.now()}\n|---Symbol---Coins---Price-USD---\n"
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
                #Finds cost of current currency * shares owned
                Cost = float(cryptoReturn['Rates'][x]) * float(DB.Crypto_CheckCurrency(User,cryptoReturn['Symbol'][x]))
                
                
                
                #Adds to portfolio message
                Portfolio += (f"|{(cryptoReturn['Symbol'][x])}   {DB.Crypto_CheckCurrency(User,cryptoReturn['Symbol'][x])}   ${Cost}\n")
                x = x + 1
            await ctx.send("Your current portfolio has been sent to you via DM")
            #find overtall user crypto value
            Portfolio += f"|Total Crypto Currency-USD ${Total}\n"
            #finds user balance + crypto value
            Portfolio += f"|Overall-USD and Crypto ${Total + DB.UserBalance(User)}"
            #Send DM of current portfolio
            await _user.send(Portfolio)
            time.sleep(1)
        else:
            await ctx.send('You must create an account to use this feture. Type .Register to create an account')
    #General error catcher
    except Exception:
        print("Error") 




@client.command()
async def Balance(ctx):
    _user = ctx.message.author
    User = str(_user)
    await ctx.send("Your current balance has been sent to you via DM")
    Message = f"----Balance----\nTime Stamp: {datetime.datetime.now()}\nCurrent Balance USD: ${DB.UserBalance(User)}\n---------------"
    await _user.send(Message)

@client.command()
async def Leaders(ctx):
    #resets counter
    x = 0
    #array to hold leader value
    Leaders = []
    #gets list of all active users
    userList = DB.returnAllUsers()
    #runs though user list
    while x < len(userList):
        #gets name of user
        name = userList[x]
        #adds user and portfolio value to array
        Leaders.append([name,Portfolio.pullUserPortfolioBalance(name)])
        #increments incrementer
        x = x + 1
    Leaders = sorted(Leaders,key=lambda Leaders: Leaders[1],reverse=True)
    #message to send back
    Message = ""#"{}\n".format('Current Rankings')
    Message += '{:<34}{:<34} {}\n'.format('Rank','User','USD Value')
    #Increment
    x = 0
    #Displays all users in order of portfolio value
    for user in Leaders:
        Message += '{:<34}{:<34} ${:,}\n'.format(x+1,Leaders[x][0],Leaders[x][1])
        x = x + 1
    await ctx.send(Message)
    
    

@client.event
async def on_ready():
    print("Bot Online")

client.run('') #Discord Key

