import DB
import CryptoData

#Reads Text Data Files
def Read(name):
    try:
        #Opens file and saves as f
        with open(name) as f:
            #Reads data
            data = f.read()
        #Return file contents
        return(data)
    except Exception as e:
        #If error return 0 string
        print(e)
        return('0')
        
#Feature
def autoFill(Username):
    #Load Data
    return(0)