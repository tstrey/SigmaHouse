# -*- coding: utf-8 -*-
"""Stand-alone module fading LED in and out with PWM."""

from time import sleep_ms

from machine import PWM, Pin

led_pin = Pin(12, Pin.OUT, value=0)
led_pwm = PWM(led_pin, 5000, 0)

try:
    while True:
        for duty in range(0, 1023):
            led_pwm.duty(duty)
            sleep_ms(1)

        sleep_ms(500)

        for duty in range(1023, 0, -1):
            led_pwm.duty(duty)
            sleep_ms(1)

        sleep_ms(500)

        print(".", end="")

finally:
    led_pwm.deinit()
