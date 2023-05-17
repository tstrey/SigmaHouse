from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd
import time
import network #Import network module
import urequests

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

        while True:
            pirValue = PIR.value()
                    
            # Define the JSON data to send
            data = {"key1": "value1", "key2": "value2"}

            # Convert the JSON data to a string
            json_data = json.dumps(data)

            # Set the headers
            headers = {"Content-Type": "application/json"}

            # Send the request
            response = requests.post("http://example.com/api/endpoint", data=json_data, headers=headers)

            # Print the response
            print(response.text)
            btnVal1 = button1.value()  # Reads the value of button 1
            #print("button1 =",btnVal1)  #Print it out in the shell
            if(btnVal1 == 0):
                time.sleep(0.01)
                while(btnVal1 == 0):
                    btnVal1 = button1.value()
                    if(btnVal1 == 1):
                        count = count + 1
                        print(count)
            val = count % 2
            if(val == 1):
                url='http://' + server_ip + '/xyz/standalone/test1.json'
                resp = urequests.get(url)
                print(resp.status_code)
                json_resp = resp.json()
                lcd.move_to(1, 0)
                lcd.putstr(json_resp['data']['hello'])
                lcd.move_to(1, 1)
                lcd.putstr(json_resp['data']['todo'])
                print(resp.json())
                led.value(1)
            else:
                url='http://' + server_ip + '/xyz/standalone/test0.json'
                resp = urequests.get(url)
                print(resp.status_code)
                json_resp = resp.json()
                lcd.move_to(1, 0)
                lcd.putstr(json_resp['data']['hello'])
                lcd.move_to(1, 1)
                lcd.putstr(json_resp['data']['todo'])
                print(resp.json())
                led.value(0)
            time.sleep(0.1) #delay 0.1s
    except:
        print('exception')
        sta_if.disconnect()


DEFAULT_I2C_ADDR = 0x27

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.move_to(1, 0)
lcd.putstr('Hello')
lcd.move_to(1, 1)
lcd.putstr('Jessica & Katya')

try:
    #test()
    STA_Setup(ssidRouter,passwordRouter)
except:
     print('exception')

