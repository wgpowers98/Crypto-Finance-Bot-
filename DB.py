#Devloper: Will Powers
#Description: Allows Bot to interact with database.
#Version 0.1

import sqlite3
con = sqlite3.connect('UserData.db')
cur = con.cursor()

#----admin stuff----

def userExists(User):
    for row in cur.execute(f'SELECT Username FROM Users where Username = "{User}"'):
        if (row[0]) == User:
            return(True)
        else:
            return(False)

def createUser(User,Balance):
    maxId = 1
    for row in cur.execute('SELECT MAX(Portfolio_ID) FROM Users;'):
        #Finds most recent id
        maxId = row[0] + 1
    #Adds user to users table
    cur.execute(f"insert into Users (Username,Balance,Portfolio_ID) values ('{User}',{Balance},{maxId});")
    #Creates users portfolio table
    maxIdStr = maxId
    cur.execute(f'create table P{maxIdStr} (Symbol varchar(5) PRIMARY KEY,Shares double);')
    con.commit()

def UpdateUserBalance(User,Balance):
    cur.execute(f'Update Users set Balance = {Balance} where Username = "{User}";')
    con.commit()

def UserBalance(User):
    #checks users balance
    for row in cur.execute(f"select balance from Users where Username = '{User}';"):
        return(row[0])

#Returns number of users in table users
def numberOfUsers():
    #creates array to hold users
    Users = []
    #Returns number of rows that exits
    for row in cur.execute(f"select count(Username) from Users;"):
        return(row[0])

#returns list of registered users
def returnAllUsers():
    Users = []
    for row in cur.execute(f"select Username from Users;"):
        Users.append(row[0])
    return(Users)



#----Crypto Library----

def Crypto_AddCurrency(User,Symbol,Shares):
    try:
        UserID = 1
        for row in cur.execute(f'SELECT Portfolio_ID FROM Users where Username = "{User}";'):
            #Finds most recent id
            UserID = row[0]
        cur.execute(f'insert into P{UserID} (Symbol,Shares) values ("{Symbol}",{Shares});')
        con.commit()
    #If user has 0 balance but coin is still in table
    except sqlite3.IntegrityError:
        print('Error on trade, makeing update')
        Crypto_UpdateCurrency(User,Symbol,Shares)
def Crypto_RemoveCurrency(User,Symbol):
    UserID = 1
    for row in cur.execute(f'SELECT Portfolio_ID FROM Users where Username = "{User}";'):
        #Finds most recent id
        UserID = row[0]
    cur.execute(f'Delete from P{UserID} where Symbol = "{Symbol}";')
    con.commit()

def Crypto_UpdateCurrency(User,Symbol,Shares):
    UserID = 1
    #Returns users ID
    for row in cur.execute(f'SELECT Portfolio_ID FROM Users where Username = "{User}";'):
        #Finds most recent id
        UserID = row[0]
    cur.execute(f'update P{UserID} set Shares = {Shares} where Symbol = "{Symbol}";')
    con.commit()



#Edits current portfolio
def Crypto_CheckCurrency(User,Symbol):
    UserID = 'No'
    Shares = 0
    for row in cur.execute(f'SELECT Portfolio_ID FROM Users where Username = "{User}";'):
        #Finds most recent id
        UserID = row[0]
    for row in cur.execute(f'SELECT Shares FROM P{UserID} where Symbol = "{Symbol}";'):
        #Finds most recent id
        Shares = row[0]
    return(float(Shares))

def Crypto_ReturnAllCurrency(User):
    #Gets user ID
    for row in cur.execute(f'SELECT Portfolio_ID FROM Users where Username = "{User}";'):
        #Finds most recent id
        UserID = row[0]
    
    Symbols,Shares = [],[]
    #Gets User Shares value
    for Share in cur.execute(f'Select Shares from P{UserID}'):
        Shares.append(Share[0])
        #Finds most recent id

    for Symbol in cur.execute(f'Select Symbol from P{UserID}'):
        Symbols.append(Symbol[0])
    #makes data into formatted array    
    data = {'Symbol':Symbols,'Shares':Shares}
    return(data)




