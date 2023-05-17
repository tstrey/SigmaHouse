from machine import Pin, PWM
from time import sleep
from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd
import time
import network #Import network module
import urequests

ssidRouter     = 'TP-Link_3E52' #Enter the router name
passwordRouter = '37424916' #'21filk' #Enter the router password 37424916
server_ip = '192.168.0.100'
buzzer = PWM(Pin(25))

buzzer.duty(1000) 

# Define the function to poll the server for changes
def poll_server():
    # Send a GET request to the server
    response = requests.get(f'{SERVER_URL}/hashmap/{HASHMAP_KEY}')

    # Decode the response JSON
    data = json.loads(response.text)

    # Check if the hashmap has changed
    if data.get('changed'):
        # Handle the change
        buzzer.freq(294)
        sleep(0.25)
        handle_hashmap_change(data['value'])

# Define the function to handle a hashmap change
def handle_hashmap_change(value):
    # Do something with the new hashmap value
    print(f'The hashmap value has changed to: {value}')

# Poll the server for changes periodically
while True:
    poll_server()
    time.sleep(5)  # Poll every 5 seconds


