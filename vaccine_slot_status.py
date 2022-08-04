#importing requests : it is module which allows us to make HTTP requests.
import requests 

#tried process till user enters valid PINCODE
PINCODE = "0"
while len(PINCODE) != 6:
    PINCODE = input("Enter the PINCODE : ")
    if len(PINCODE) < 6:
        print (f"{PINCODE} is shorter than the actual length")
    elif len(PINCODE) > 6:
        print (f"{PINCODE} is longer than the actual length")
    
DATE = input ("Enter the Date (Date format: DD-MM-YYYY) : ")

#requesting API link provided in CO-WIN API portal
request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={DATE}"
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
response = requests.get(request_link, headers = header)
response_json = response.json()

# for printing all the available centers
# num_centers = len(response_json['centers'])
# for i in range(num_centers):
#     print(response_json['centers'][i]["name"])

Total_centers = len(response_json['centers'])
print ()
print ("                        *>>>>>>    RESULTS   <<<<<<<*                                ")
print ("-------------------------------------------------------------------------------------")
print (f"Date: {DATE} | Pincode: {PINCODE} ")

if Total_centers != 0:
    print (f"Total centers in your area is: {Total_centers}" )
else:
    print (f"Unfortunately !! Seems like no center in this area / Kindly re-check the Pincode" )

print ("------------------------------------------------------------------------------------")
print ()

for cent in range(Total_centers):
    # iterating in all available centers  
    # And printing the relavent information
    fee_val = response_json['centers'][cent]['fee_type']
    print ()
    print (f"[{cent+1}] Center Name:", response_json['centers'][cent]['name'])
    print ("------------------------------------------------------------")
    print ("   Date      Vaccine Type      Vaccine Fee     Minimum Age    Available ")
    print ("  ------     -------------     ------------    ------------   ----------")
    this_session = response_json['centers'][cent]['sessions']
    
    # now iterating through sessions avilable in the specific center and printing relavent stuff 
    for val in range(len(this_session)):
        print ( "{0:^12} {1:^12} {2:^13} {3:^14} {4:^16}".format(this_session[val]['date'], this_session[val]['vaccine'], fee_val,this_session[val]['min_age_limit'], this_session[val]['available_capacity']))