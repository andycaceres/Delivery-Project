import csv
import datetime

class Truck:
    def __init__(self, hour, min):
        self.packages = list()
        self.miles_traveled = 0.0
        self.current_address = "4001 South 700 East"
        self.current_h = hour
        self.current_m = min
        self.current_s = 0
        self.start_time = datetime.timedelta(hours=int(8), minutes=int(0), seconds=int(0))
        

class Address:
    def __init__(self, name, address, zip):
        self.name = name
        self.address = address
        self.zip = zip

address_list = list()

# Big O(N) 
# Loops through address data and adds to the list
def loadAddressData(filename):
    with open(filename) as addresses:
        address_data = csv.reader(addresses, delimiter=',')
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)

        for x in address_data:
            #split the string into name and address
            temp = x[0].split("\n")
            name = temp[0]
            address = temp[1]
            #split the address and zip
            temp2 = x[1].split("\n")
            if (len(temp2) == 2):
                zip = temp2[1][1:-1]
            if (name == 'Western Governors University'):
                zip = 84107
            else:
                zip = None
            
            a = Address(name, address, zip)
            address_list.append(a)

class Distance():
    pass

distance_data = list()

# Big O(N^2) 
# Loops through distance data and adds to the list  
def loadDistanceData(filename):
    with open(filename) as distances:
        address_data = csv.reader(distances, delimiter=',')
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
        next(address_data)
       
        for x in address_data:
            index = 2
            index3 = 0
            temp = x[0].split("\n")
            #name = temp[0]
            temp_list = list()

            while(index < len(x)):
                if(x[index]):
                    temp_list.append(float(x[index]))
                    index3+=1
                index+=1
        
            distance_data.append(temp_list)