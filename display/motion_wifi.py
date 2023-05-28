from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd
import time
import network #Import network module
import urequests
import json
import sys

#Enter correct router name and password
ssidRouter     = 'TP-Link_3E52' #Enter the router name
passwordRouter = '37424916' #'21filk' #Enter the router password 37424916
server_ip = '192.168.0.100'
#ssidRouter = 'NETGEAR03'
#passwordRouter = 'crispygiant525'


def STA_Setup(ssidRouter,passwordRouter):
    print("Setup start")
    try:
        sta_if = network.WLAN(network.STA_IF) #Set ESP32 in Station mode
        print("got  sta_if")
        if not sta_if.isconnected():
            print('connecting to',ssidRouter)
    #Activate ESP32’s Station mode, initiate a connection request to the router
    #and enter the password to connect.
            sta_if.active(True)
            sta_if.connect(ssidRouter,passwordRouter)
            print("still connecting")
    #Wait for ESP32 to connect to router until they connect to each other successfully.
            while not sta_if.isconnected():
                pass
        print('Connected, IP address:', sta_if.ifconfig())
        urlRegister = 'http://' + server_ip + '/registerHouse'
        resp = urequests.get(urlRegister)
        print(resp.status_code)
        json_resp = resp.json()
        print(resp.json())
        print("Setup End")
        button1 = Pin(16, Pin.IN, Pin.PULL_UP)
        led = Pin(12, Pin.OUT)
        PIR = Pin(14, Pin.IN)
        count = 0
        
        localIp = sta_if.ifconfig()[0]
        print(localIp)
        while True:
            print("in True")
            pirValue = PIR.value()
            print(pirValue)
            if pirValue == 1:
                led.value(1)# turn on led
                 # send alaram to the server
                print('before data ' + localIp)
                data = {"ip": localIp, "alarm": "motion"}
                print('data defined')
                print(data)
                # Convert the JSON data to a string
                json_data = json.dumps(data)
                print(json_data)

                # Set the headers
                headers = {"Content-Type": "application/json"}
                
                print('about to send request')

                # Send the request
                response = urequests.post("http://" + server_ip + "/updateHouseState", data=json_data, headers=headers)

                # Print the response
                print(response.status_code)
                print(response.json())
                json_resp = response.json()
                print('alarm on')

            else:
                led.value(0)
                print('before data led 0 ' + localIp)
                data = {"ip": localIp, "alarm": "off"}
                print('data defined')
                print(data)
                # Convert the JSON data to a string
                json_data = json.dumps(data)
                print(json_data)

                # Set the headers
                headers = {"Content-Type": "application/json"}
                
                print('about to send request')

                # Send the request
                response = urequests.post("http://" + server_ip + "/updateHouseState", data=json_data, headers=headers)

                # Print the response
                print(response.status_code)
                print(response.json())
                json_resp = response.json()              
                print('alarm off')
            time.sleep(0.1)
                    

    except Exception as e:
        print('exception')
        sys.print_exception(e)
        sta_if.disconnect()


DEFAULT_I2C_ADDR = 0x27

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.move_to(1, 0)
lcd.putstr('Test')
lcd.move_to(1, 1)
lcd.putstr('Jessica & Katya')

try:
    #test()
    STA_Setup(ssidRouter,passwordRouter)
except:
     print('exception')

