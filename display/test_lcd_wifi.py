from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd
import time
import network #Import network module
import urequests

#Enter correct router name and password
ssidRouter     = 'TP-Link_3E52' #Enter the router name
passwordRouter = '37424916' #'21filk' #Enter the router password 37424916
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
    #Print the IP address assigned to ESP32 in “Shell”.
        print('Connected, IP address:', sta_if.ifconfig())
 #       url='http://192.168.0.100/mdds/standalone/test.json'
        url='http://192.168.0.100/xyz/standalone/test.json'
        resp = urequests.get(url)
        print(resp.status_code)
        json_resp = resp.json()
        lcd.move_to(1, 0)
        lcd.putstr(json_resp['data']['hello'])
        lcd.move_to(1, 1)
        lcd.putstr(json_resp['data']['todo'])
        print(resp.json())
        #http://192.168.0.101/mdds/standalone/config.json
        print("Setup End")
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

# The following line of code should be tested
# using the REPL:

# 1. To print a string to the LCD:
#    lcd.putstr('Hello world')
# 2. To clear the display:
#lcd.clear()
# 3. To control the cursor position:
# lcd.move_to(2, 1)
# 4. To show the cursor:
# lcd.show_cursor()
# 5. To hide the cursor:
#lcd.hide_cursor()
# 6. To set the cursor to blink:
#lcd.blink_cursor_on()
# 7. To stop the cursor on blinking:
#lcd.blink_cursor_off()
# 8. To hide the currently displayed character:
#lcd.display_off()
# 9. To show the currently hidden character:
#lcd.display_on()
# 10. To turn off the backlight:
#lcd.backlight_off()
# 11. To turn ON the backlight:
#lcd.backlight_on()
# 12. To print a single character:
#lcd.putchar('x')
# 13. To print a custom character:
#happy_face = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x11, 0x0E, 0x00])
#lcd.custom_char(0, happy_face)
#lcd.putchar(chr(0))