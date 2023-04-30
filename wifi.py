import time
import network #Import network module
import urequests

#Enter correct router name and password
#ssidRouter     = 'TP-Link_3E52' #Enter the router name
#passwordRouter = '37424916' #'21filk' #Enter the router password 37424916
#ssidRouter = 'NETGEAR03' 
#passwordRouter = 'crispygiant525'

ssidRouter = 'NETGEAR00'
passwordRouter = 'ancientpineapple224'

def test():
    wlan = network.WLAN(network.STA_IF)
    nets = wlan.scan()
    print(nets)
    for net in nets:
        print(net.ssid)
        

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
    #    url='http://192.168.0.101/mdds/standalone/config.json'
        url ='http://192.168.0.13/mdds/standalone/test.json'   
        resp = urequests.get(url)
        print(resp.status_code)
        print(resp.json())
        #http://192.168.0.101/mdds/standalone/config.json
        print("Setup End")
    except:
        print('exception')
        sta_if.disconnect()

try:
    #test()
    STA_Setup(ssidRouter,passwordRouter)
except:
     print('exception')
