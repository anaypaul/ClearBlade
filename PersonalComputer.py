from clearblade.ClearBladeCore import System, Query, Developer
import psutil
import json
import time
def addNewSystem(SystemKey, SystemSecret):
    mySystem = System(SystemKey, SystemSecret, safe=True)
    return mySystem

def authenticateUser(mySystem, email, password):
    return mySystem.User(email, password)

def connectToDevice(mySystem, deviceName, deviceActiveKey):
    return mySystem.Device(device_name, device_active_key)
def getDeviceDetailsByName(mySystem, myUserName,  deviceName):
    return mySystem.getDevice(myUserName, deviceName)
    # return mySystem.DEVgetDevice()

def collectDeviceInfo():
    processes = []
    data = {}
    
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'memory_percent']):
        processes.append(proc.info)

    for each in processes:
        print(each['username'], each["pid"], each["name"], each['memory_percent'])
    return processes

#connecting to system.
SystemKey = "86e0fac90bcedcd5b09dcaaa8e77"
SystemSecret = "86E0FAC90BB0CB99FDC09ED0F5ED01"
mySystem = addNewSystem(SystemKey, SystemSecret)

#authenticating a user by connecting
email = "anay.paul2@gmail.com"
password = "***********"
anay = authenticateUser(mySystem,email, password)
# print anay


#authenticating device

device_active_key = "1K2LMNT8rnn12c9MqSJ6k629RIVdn"
device_name = "MyMacbookPro"

mydevice = connectToDevice(mySystem,device_name, device_active_key)

#updating device info
mydevice.update({"state":"ON"})
mydevice.update({"description":"My Macbook Pro"})


#geting device details by name 
# print "Details of device: {0}".format(device_name)
dev_anay = Developer(email, password)
deviceDetails = getDeviceDetailsByName(mySystem, dev_anay, device_name)
# print(deviceDetails)



#collecting all running process info
runningProcessData = collectDeviceInfo()
# print runningProcessData

#reading from the collection 
myCol = mySystem.Collection(anay, collectionName="testCollection")
rows = myCol.getItems()

# for each in rows:
    # print each




#MQTT messaging

mqtt = mySystem.Messaging(anay)
def on_connect(client, userdata, flags, rc):
    # When we connect to the broker, start publishing our data to the keelhauled channel
    for i in range(20):
        if i%2==0:
            payload = "hi"
        else:
            payload = "bye"
        client.publish("mytestchannel", payload)
        time.sleep(1)


def on_message(client, userdata, message):
    # When we receive a message, print it out
    print "Received message '" + message.payload + "' on topic '" + message.topic + "'"


mqtt.on_connect = on_connect
mqtt.on_message = on_message

# Connect and wait for messages
mqtt.connect()
time.sleep(1)
mqtt.disconnect()


code = mySystem.Service("mycodeservice")

for each in runningProcessData:
    each['username'] = str(each['username'])
    each['name'] = str(each['name'])
    each['memory_percent'] = str(each['memory_percent'])
    x = code.execute(anay, each)
    print(x)


