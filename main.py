# Andy Caceres

# This project creates a HashTable that stores package data for delivery on 3 trucks
#  and uses the nearest neighbor to find the shortest distance between packages to 
#  deliver all packages before the deadline. 

import package
import HashTable
import Truck
import csv

#Create the HashTable
h = HashTable.HashTable()

# Loads package data and inserts it into the Hashtable
def loadPackageData(filename):
    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=',')
        next(package_data)
        next(package_data)
        next(package_data)
        next(package_data)
        next(package_data)

        for x in package_data:
            package_id = x[0]
            address = x[1]
            city = x[2]
            zip = x[4]
            deadline = x[5]
            mass = x[6]

            package_to_insert = package.Package(package_id, address, city, zip, deadline, mass)
            h.insert(package_id, package_to_insert)
        
# Load package, address, and distance date
loadPackageData('Package_Data.csv')
Truck.loadAddressData('Distance Table.csv')
Truck.loadDistanceData('Distance Table.csv')
 
# Initializes truck objects
t1 = Truck.Truck(8, 0)
t2 = Truck.Truck(8, 0)
t3 = Truck.Truck(10, 0)

# Manually load trucks with package data from the Hashtable
# Delivery addresses were sorted by grouping closest addresses together
def loadTrucks():
    i = 1
    for x in h.table:
        if(i == 13 or i == 14 or i == 15 or i == 16 or i == 19 or i == 20 or i == 1 or i == 40 or i == 34 or i == 39):
            t1.packages.append(h.search(i))
            h.search(i).delivery_status = "At the hub"
        if(i == 3 or i == 31 or i == 38 or i == 37 or i == 30 or i == 29 or i == 7 or i == 2 or i == 33 or i == 5 or i == 8 or i == 10 or i == 18 or i == 11 or i == 36):
            t2.packages.append(h.search(i))
            h.search(i).delivery_status = "At the hub"
        if(i == 25 or i == 26 or i == 17 or i == 12 or i == 32 or i == 4 or i == 21 or i == 28 or i == 24 or i == 22 or i == 23 or i == 27 or i == 35 or i == 6 or i == 11):
            t3.packages.append(h.search(i))
            h.search(i).delivery_status = "At the hub"
        if(i == 9):
            # Fixes incorrect address
            h.search(i).address = "410 S State St"
            t3.packages.append(h.search(i))
            h.search(i).delivery_status = "At the hub"
        i+=1

loadTrucks()

# Truck 2: 3, 18, 36, 38
# Together: 13, 14, 15, 16, 19, 20
# Delayed on flight: 6, 25, 28, 32
print("Packages loaded onto trucks based on requirements")
print("Truck 1 has packages 13, 14, 15, 16, 19, 20 that must be delivered together:")
#for packages in t1.packages:
    #print(packages.id)
#print("Truck 2 has packages 3, 18, 36, 38 that can only be delivered on truck 2:")
#for packages in t2.packages:
    #print(packages.id)
print("Truck 3 has the packages that will arrive late at 9:05 AM")
print(f"Truck 3 departure time: {t3.current_h}:0{t3.current_m}")
print("All packages delivered according to the delivery requirements.")

# Finds the distance between two given addresses
def distanceBetweenAddresses(address1, address2):
    index1 = 0
    index2 = 0
    
    #finds the address index for distance table
    for x in Truck.address_list:
        #corrects address spelling
        if("3575 W Valley Central" in address1):
            address1 = "3575 W Valley Central Sta bus Loop" 
        if(address1 in x.address):
            break
        index1+=1
    for x in Truck.address_list:
        #corrects address spelling
        if("3575 W Valley Central" in address2):
            address2 = "3575 W Valley Central Sta bus Loop"
        if(address2 in x.address):
            break
        index2+=1
    
    if(index2 > index1):
        distance_between = Truck.distance_data[index2][index1]
    if(index2 < index1):
        distance_between = Truck.distance_data[index1][index2]
    if(index2 == index1):
        distance_between = Truck.distance_data[index2][index1]

    return distance_between
 
# Loops through the package list calling distanceBetweenAddresses() to find the smallest distance
def findMinDistance(truck_input):#input truck
    #distance of current and first
    current_location = truck_input.current_address
    first_package_location = truck_input.packages[0].address
    distance2 = distanceBetweenAddresses(current_location, first_package_location)
    closest_address = first_package_location

    #Loop through list to find smallest distance
    for address in truck_input.packages:
        temp_distance = distanceBetweenAddresses(current_location, address.address)
        if(temp_distance < distance2):
            distance2 = temp_distance
            closest_address = address.address
   
    distance_address = [distance2, closest_address]
    return distance_address

# Algorithm uses Nearest Neighbor approach
# Loops through the package list and delivers the packages 
def deliverPackages(deliveries):
    min_distance_address = findMinDistance(deliveries)
    closest_location = min_distance_address[1]
    distance = min_distance_address[0]

    #Delivers these addresses first to meet deadline
    for x in deliveries.packages:
        if (x.address in "5383 South 900 East #104"):
            closest_location = "5383 South 900 East #104"
    for x in deliveries.packages:
        if (x.address in "3060 Lester St"):
            closest_location = "3060 Lester St"
    
    for package in deliveries.packages:
        if(closest_location in package.address):
            deliveries.packages.remove(package)
            package.delivery_status = "Delivered"
            
            current_hour = deliveries.current_h
            current_min = deliveries.current_m
            current_sec = deliveries.current_s

            # Get the time passes in seconds then go from seconds to minutes and hours
            time_passed_sec = round(distance / 0.005, 5) #0.005 mi/sec = 18mi/hr
            time_passed_hour = 0
            time_passed_min = 0

            while(time_passed_sec > 59):
                time_passed_min += 1
                time_passed_sec -= 60
            while(time_passed_min > 59):
                time_passed_hour += 1
                time_passed_min -= 60

            delivered_hour = current_hour + time_passed_hour
            delivered_min = current_min + time_passed_min
            delivered_sec = current_sec + time_passed_sec

            while(delivered_sec > 59):
                delivered_min += 1
                delivered_sec -= 60
            while(delivered_min > 59):
                delivered_hour += 1
                delivered_min -= 60

            # Set package delivery time and format the time
            if(delivered_hour < 10 and delivered_min < 10):
                package.time_delivered = f"0{delivered_hour}:0{round(delivered_min)}"
            if(delivered_hour < 10 and delivered_min >= 10):
                package.time_delivered = f"0{delivered_hour}:{round(delivered_min)}"
            if(delivered_hour >= 10 and delivered_min < 10):
                package.time_delivered = f"{delivered_hour}:0{round(delivered_min)}"
            if(delivered_hour >= 10 and delivered_min >= 10):
                package.time_delivered = f"{delivered_hour}:{round(delivered_min)}"

            deliveries.current_h = delivered_hour
            deliveries.current_m = delivered_min
            deliveries.current_s = delivered_sec

    deliveries.current_address = closest_location
    deliveries.miles_traveled = round(distance + deliveries.miles_traveled, 2)

# Calls distanceBetweenAddresses() to get ditance and finds time for the truck given
# Used to find the Trucks current time after delivering final package and returning to base
def getCurrentTime(truck):
    distance = distanceBetweenAddresses(truck.current_address, "4001 South 700 East")
    current_hour = truck.current_h
    current_min = truck.current_m
    time_passed_min = round(distance / 0.3, 5) #0.3 mi/m = 18mi/h
    time_passed_hour = 0

    while(time_passed_min > 59):
        time_passed_hour += 1
        time_passed_min -= 60

    delivered_hour = current_hour + time_passed_hour
    delivered_min = int(current_min + time_passed_min)

    while(delivered_min > 59):
        delivered_hour += 1
        delivered_min -= 60

    truck.current_h = int(delivered_hour)
    truck.current_m = int(delivered_min)

# Get input to check delivery status for all packages at that time
print("Enter a time after 8:00 to check package delivery status (time must be in military time ex. 0100)")
time_input = input("Enter time: ")
time_input_h = time_input[0] + time_input[1]
time_input_m = time_input[2] + time_input[3]

# If the input time is greater than trucks departure time the packages are en route
if(int(time_input_h) >= 8):
    for packages in t1.packages:
        packages.delivery_status = "En route"
    for packages in t2.packages:
        packages.delivery_status = "En route"
if(int(time_input_h) >= 10):
    for packages in t3.packages:
        packages.delivery_status = "En route"

# Deliver packages while trucks time is less than the input time
while(len(t1.packages) > 0):
    if(t1.current_h < int(time_input_h)):
        deliverPackages(t1)
    if(t1.current_h == int(time_input_h) and t1.current_m <= int(time_input_m)):
        deliverPackages(t1)
    if(t1.current_h > int(time_input_h)):
        break
    if(t1.current_h == int(time_input_h) and t1.current_m > int(time_input_m)):
        break
while(len(t2.packages) > 0): #5
    if(t2.current_h < int(time_input_h)):
        deliverPackages(t2)
    if(t2.current_h == int(time_input_h) and t2.current_m <= int(time_input_m)):
        deliverPackages(t2)
    if(t2.current_h > int(time_input_h)):
        break
    if(t2.current_h == int(time_input_h) and t2.current_m > int(time_input_m)):
        break
while(len(t3.packages) > 0): #5
    if(t3.current_h < int(time_input_h)):
        deliverPackages(t3)
    if(t3.current_h == int(time_input_h) and t3.current_m <= int(time_input_m)):
        deliverPackages(t3)
    if(t3.current_h > int(time_input_h)):
        break
    if(t3.current_h == int(time_input_h) and t3.current_m > int(time_input_m)):
        break

# Display packages delivered in the time frame from the input time
for packages in h.table:
    if(packages[0][1].delivery_status == "Delivered"):
        print("Package: ", packages[0][1].id, "Delivered at: ", packages[0][1].time_delivered)
    else:
        print("Package: ", packages[0][1].id, " ", packages[0][1].delivery_status)

# Prints truck mileage up to the input time
print("\n")
print("Truck 1 Miles traveled: ", t1.miles_traveled)
print("Truck 2 Miles traveled: ", t2.miles_traveled)
print("Truck 3 Miles traveled: ", t3.miles_traveled)
    

print("\nFinishing deliveries...\n")

# Finish the rest of the deliveries on the trucks
while(len(t1.packages) >0):
    deliverPackages(t1)
if(len(t1.packages) == 0):
    t1.miles_traveled += distanceBetweenAddresses(t1.current_address, "4001 South 700 East")
    getCurrentTime(t1)
while(len(t2.packages) >0):
    deliverPackages(t2)
if(len(t2.packages) == 0):
    t2.miles_traveled += distanceBetweenAddresses(t2.current_address, "4001 South 700 East")
    getCurrentTime(t2)
while(len(t3.packages) >0):
    deliverPackages(t3)
if(len(t3.packages) == 0):
    t3.miles_traveled += distanceBetweenAddresses(t3.current_address, "4001 South 700 East")
    getCurrentTime(t3)

# Print Delivery status with deadlines
print("\nPackages delivered with EOD deadline")
for packages in h.table:
    id = int(packages[0][0])
    if (id == 1 or id == 13 or id == 14 or id == 16 or id == 20 or id == 25 or id == 29 or id == 30 or id == 31 or id == 34 or id == 37 or id == 40 or id == 15):
        continue
    else:
        print(f"ID: {id} Delivered on time:  {packages[0][1].time_delivered}")

# Deliveries with 10:30 deadline: 1, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40
print("\nPackages with 10:30 AM deadline:")
for packages in h.table:
    id = int(packages[0][0])
    if (id == 1 or id == 13 or id == 14 or id == 16 or id == 20 or id == 25 or id == 29 or id == 30 or id == 31 or id == 34 or id == 37 or id == 40):
        print(f"ID: {id} Delivered on time:  {packages[0][1].time_delivered}")
# Package with 9:00 deadline: id 15
print("\nPackage with 9:00 AM deadline")
print(f"ID: {15} Delivered on time:  {h.search(15).time_delivered}")

# Print the total miles for each truck and combined       
print("\n")
print(f"Truck 1 Total miles: {t1.miles_traveled}    End Time: 0{t1.current_h}:{t1.current_m}")
print(f"Truck 2 Total miles: {t2.miles_traveled}    End Time: {t2.current_h}:0{t2.current_m}")
print(f"Truck 3 Total miles: {t3.miles_traveled}    End Time: {t3.current_h}:{t3.current_m}")
print("Total miles: ", round(t1.miles_traveled + t2.miles_traveled + t3.miles_traveled))
print("\n")