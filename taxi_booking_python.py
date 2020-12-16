import uuid 

# Zoho Taxi Booking
print("Welcome")

class Taxi:
    def __init__(self,taxiId,taxiEarning,raidDetails,state,stationed,raidEndsAt):
        self.taxiId = taxiId
        self.taxiEarning = taxiEarning
        self.raidDetails = raidDetails
        self.state = state
        self.stationed = stationed
        self.raidEndsAt = raidEndsAt

class TripDetails:
    def __init__(self,bookingId,custId,startPoint,endPoint,fair,timeTaken,
                 startTime,endTime):
        self.bookingId = bookingId
        self.custId = custId
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.fair = fair
        self.timeTaken = timeTaken
        self.startTime =startTime
        self.endTime = endTime

def fair(AvailablePoints,pickupPoint,dropPoint,pickupTime,taxi,custId):
    #Calculate Total Fair for Raid
    AvailablePoints.sort()
    pointDistance = abs(AvailablePoints.index(pickupPoint) -
                   AvailablePoints.index(dropPoint))
    distanceInKM =  pointDistance * 15
    travelTime = pointDistance

    if(int(pickupTime) == 23):
        dropTime = int(pickupTime) + travelTime
        dropTime = dropTime - 24
    else:
        dropTime = int(pickupTime) + travelTime
        
    #Bare Minimum for First Five Kms
    miniFairRate = 100
    subDistance = distanceInKM -5
    #Fair for Next Kms 
    FairRate = miniFairRate + (subDistance * 10)
    print("pickupTime : ",pickupTime)
    print("dropTime : ",dropTime)
    print("distanceInKM :",distanceInKM)
    print("FairRate :",FairRate)
    #Updating Taxi Earning
    taxi.taxiEarning += FairRate
    taxi.raidEndsAt = dropTime
    print(taxi.taxiEarning)
    #Update Trip Detail to Taxi
    trip = TripDetails(uuid.uuid1(),custId,pickupPoint,dropPoint,FairRate,travelTime,
                       pickupTime,dropTime)

    taxi.raidDetails.append(trip)
    

def booking():
    print("Please Enter the Customer Id :",end=" ")
    custId = input()
    print("Please Enter the Pickup Point from Available Points:",end=" ")
    AvailablePoints = ['A','B','C','D','E','F']
    print(" ".join(map(str,AvailablePoints)))
    pickPoint = input()
    if(pickPoint not in AvailablePoints):
        print("Please select a Location Available!")
    else:
        AvailablePoints.remove(pickPoint)
        print("Please Enter the Drop Point from Available Points:",end=" ")
        print(" ".join(map(str,AvailablePoints)))
        dropPoint = input()
        if(dropPoint not in AvailablePoints):
            print("Please select a Location Available!")
        else:
            AvailablePoints.append(pickPoint)
            print("Please Enter the Pickup Time from 0 - 23 in 24 HRS Format:"
                  ,end=" ")
            pickupTime = input()
            if(int(pickupTime) >=0 and int(pickupTime)<=23):
                
                #Finding Free Taxi near the pickup Point

                #List of Free taxi's
                taxiList = []
                for taxi in taxiDatabase:
                    if(taxi.state == "Free" or taxi.raidEndsAt < int(pickupTime)):
                        taxiList.append(taxi)

                #Find Nearest Free taxi at that Time
                nearTaxiList = []
                if(len(taxiList) == 0):
                    print("No Taxi's are Available at the movement")
                else:
                    picInd = AvailablePoints.index(pickPoint)
                    for i in range(len(taxiList)):
                        taxiIndex = AvailablePoints.index(taxiList[i].stationed)
                        distanceBetween = abs (picInd - taxiIndex)
                        nearTaxiList.append([taxiList[i],distanceBetween])
                    nearTaxiList.sort(key = lambda x: x[1])
                    print("Alloted Taxi Id :",end=" ")
                    print(nearTaxiList[0][0].taxiId)
                    nearTaxiList[0][0].state = "Hired"
                    nearTaxiList[0][0].stationed = dropPoint
                    #Calculating Fair
                    fair(AvailablePoints,pickPoint,dropPoint,pickupTime,
                         nearTaxiList[0][0],custId)
            else:
                print("Please Enter a Valid Pickup Time")

        
def displayTaxi():

    for taxi in taxiDatabase: 
        print("taxiId : ",taxi.taxiId)
        print("taxiEarning :",taxi.taxiEarning)
        print("Raid Details : ")
        for raid in taxi.raidDetails:
            print(" BookingId : ",raid.bookingId)
            print(" CustomerId : ",raid.custId)
            print(" StartPoint: ",raid.startPoint)
            print(" EndPoint : ",raid.endPoint)
            print(" fair : ",raid.fair)
            print(" TimeTaken : ",raid.timeTaken)
            print(" StartTime : ",raid.startTime)
            print(" EndTime : ",raid.endTime)
            print()
    

#Adding Taxi Details
t1 = Taxi("1",0,[],"Free","A",0)
t2 = Taxi("2",0,[],"Free","A",0)
t3 = Taxi("3",0,[],"Free","A",0)
t4 = Taxi("4",0,[],"Free","A",0)

#Taxi Database
taxiDatabase = [t1,t2,t3,t4]

while(1):

    print("Press 1 for Taxi Booking")
    
    print("Press 2 for Taxi Details")

    print("Press 3 for Exit")

    
    choice = int(input())

    if(choice == 1):
        booking()
    elif(choice ==2):
        displayTaxi()
    elif(choice ==3):
        break
    else:
        print("Please Enter a valid Choice")
