from time import sleep_ms, ticks_ms
from machine import I2C, Pin, PWM
from i2c_lcd import I2cLcd
import time
import network #Import network module
import urequests
import json
import sys
from time import sleep

#Enter correct router name and password
ssidRouter     = 'TP-Link_3E52' #Enter the router name
passwordRouter = '37424916' #'21filk' #Enter the router password 37424916
server_ip = '192.168.0.100'
localIp = ''


def STA_Setup(ssidRouter,passwordRouter):
    print("Setup start")
    try:
        sta_if = network.WLAN(network.STA_IF) #Set ESP32 in Station mode
        print("music_alert got sta_if")
        if not sta_if.isconnected():
            print('connecting to',ssidRouter)
            sta_if.active(True)
            sta_if.connect(ssidRouter,passwordRouter)
            print("still connecting")
            while not sta_if.isconnected():
                pass
        print('Connected, IP address:', sta_if.ifconfig())
        urlRegister = 'http://' + server_ip + '/registerHouse'
        resp = urequests.get(urlRegister)
        print(resp.status_code)
        json_resp = resp.json()
        print(resp.json())
        print("Setup End")
        
        localIp = sta_if.ifconfig()[0]
        print(localIp)

    except Exception as e:
        print('exception')
        sys.print_exception(e)
        sta_if.disconnect()



# Define the function to poll the server for changes
def poll_server():
    # Send a GET request to the server
    print('before data ' + localIp)
    # Set the headers
    headers = {"Content-Type": "application/json"}

    print('about to send request')


    urlUpdate = 'http://' + server_ip + '/checkAlarmStatus'
    resp = urequests.get(urlUpdate)
    print(resp.status_code)
    json_resp = resp.json()
    print(json_resp)
    # Decode the response JSON
    alarmSate = json_resp['alarm']
    # Check if the hashmap has changed
    if alarmSate == 'on':
        # Handle the change
        
        buzzer = PWM(Pin(25))
        buzzer.duty(1000)
        buzzer.freq(294)
        sleep(0.25)
        
    else:
        buzzer = PWM(Pin(25))
        buzzer.duty(0)
   
try:
#test()
    STA_Setup(ssidRouter,passwordRouter)
except:
     print('exception')

# Poll the server for changes periodically
while True:
    poll_server()
    time.sleep(5)  # Poll every 5 seconds


