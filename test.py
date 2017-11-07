from pymongo import MongoClient


# name='a'
#client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
#db = client.onlinebank
#now = datetime.datetime.now()
#x = ntplib.NTPClient()
#ctime(fromtimestamp(x.request('europe.pool.ntp.org').tx_time))
#now=datetime.datetime.utcfromtimestamp(x.request('europe.pool.ntp.org').tx_time)
#now.ctime()
#print now.hour

# c = ntplib.NTPClient()
# response = c.request('europe.pool.ntp.org', version=3)
# ctime(response.tx_time)

client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
db = client.onlinebank

cursor = db.withdrawal.find({})

for document in cursor:
    document['Transaction_id']
    document['Account_number']
    document['Description']
    document['Debit']
    document['Time']  #format  Fri Nov  3 06:39:33 2017
    document['Employee_id']


client = MongoClient("mongodb://aviformat:sweswe@ds155634.mlab.com:55634/onlinebank")
db = client.onlinebank

cursor2 = db.deposit.find({})

for document in cursor2:
    document['Transaction_id']
    document['Account_number']
    document['Description']
    document['Debit']
    document['Time']  #format  Fri Nov  3 06:39:33 2017
    document['Employee_id']