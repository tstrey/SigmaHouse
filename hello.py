import machine
pin12 = machine.Pin(12, machine.Pin.OUT)
pin12.value(1)
print("hello")
pin13 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
print(pin13.value())