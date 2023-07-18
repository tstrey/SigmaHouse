# -*- coding: utf-8 -*-
"""Provides main application object."""
from binascii import hexlify
from collections import deque
from time import ticks_ms

from core.menu import TextMenu
from core.wifi import NetworkWiFi

from devices.button import Button
from devices.motion import Motion
from devices.buzzer import Buzzer
from devices.device import Device

from devices.lcd_i2c import I2cLcd
from devices.led import LED

from machine import Pin, SoftI2C, Timer, unique_id

from micropython import schedule

from uasyncio import get_event_loop, sleep_ms

from ujson import dumps as json_dumps

from urequests import get as get_url, post as post_url, put as put_url


class App(Device):
    """Implements Smart House."""

    def __init__(self, name="/app", config=None, debug=False):
        """Initiate application."""
        super().__init__(name=name, debug=debug)

        self.event_queue = deque((), 10)
        self.unique_id = hexlify(unique_id()).decode("utf-8").upper()

        self._log(f"Running on board ID: {self.unique_id}")

        self.exit_code = 0

        self.config = {}
        self.config["wifi_ssid"] = config.get("wifi_ssid", "DefaultSmartHouseSSID")
        self.config["wifi_pass"] = config.get("wifi_pass", "DefaultSecretPassword")
        self.config["api_endpoint"] = config.get("api_endpoint", "http:/192.168.0.1/")
        self.config["update_interval_ms"] = config.get("update_interval_ms", 1000)

        self._log("Setting up core components")

        self._log("* LCD")
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
        self.lcd = I2cLcd(i2c, 0x27, 2, 16)
        self.lcd.clear()

        self._log("* Event Loop")
        self.loop = get_event_loop()

        self._log("* IoT Hub Update Timer")
        self._iot_hub_update_flag = False
        self._iot_hub_timer = Timer(0)
        self._iot_hub_timer.init(
            period=self.config["update_interval_ms"],
            mode=Timer.PERIODIC,
            callback=self._iot_hub_timer_callback,
        )

        self._log("Setting up peripheral devices")

        self.wlan = NetworkWiFi(
            wifi_ssid=self.config["wifi_ssid"],
            wifi_pass=self.config["wifi_pass"],
            wifi_timeout=5,
            debug=self._DEBUG,
        )

        self.button_a = Button(
            name="/in/button_a",
            pin_num=16,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )
        self.button_b = Button(
            name="/in/button_b",
            pin_num=25,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )

        self.led = LED(
            pin_num=12,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )
        self.motion = Motion(
            pin_num=14,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )

        self.buzzer = Buzzer(
            pin_num=26,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )
        
        self._buzzer_turn_on() 

        self._state = {
            "alarm": False,
            "motion" : self.motion._state,
            "led": self.led._state,
            "wall_msg": f"ID:{self.unique_id}",
        }

        self.menu = TextMenu(event_queue=self.event_queue, debug=self._DEBUG)
        self.menu.add_item("LED: ON         ", action=self._led_turn_on)
        self.menu.add_item("LED: OFF        ", action=self._led_turn_off)
        self.menu.add_item("FAN: ON         ", action=None)
        self.menu.add_item("FAN: OFF        ", action=None)
        self.menu.add_item("RGB: ON         ", action=None)
        self.menu.add_item("RGB: OFF        ", action=None)
        self.menu.add_item("ALARM: ON       ", action=None)
        self.menu.add_item("ALARM: OFF      ", action=None)

    def __enter__(self):
        """Return class instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Gracefully exit by disconnecting from network and resetting I/O devices."""
        self._log("Exiting")

        if isinstance(self._iot_hub_timer, Timer):
            self._iot_hub_timer.deinit()

        if isinstance(self.wlan, NetworkWiFi):
            self.wlan.disconnect()

        if isinstance(self.button_a, Button):
            self.button_a.finalize()

        if isinstance(self.button_b, Button):
            self.button_b.finalize()
            
            
        if isinstance(self.buzzer, Buzzer):
            self.buzzer.turn_off()

    def _iot_hub_register(self):
        """Check in with IoT Hub and provide initial state."""
        reg_url = f"{self.config.get('api_endpoint')}/houses"

        reg_info = {
            "unique_id": self.unique_id,
            "ip_address": self.wlan.ip_address,
            "state": self._state,
        }
        reg_json = json_dumps(reg_info)

        self._log("Register with IoT Hub")
        self._log(f"* POST: {reg_json} -> {reg_url}")
        try:
            response = post_url(  # noqa: S113
                url=reg_url,
                data=reg_json,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code >= 200 and response.status_code <= 299:
                self._log(f"* RESPONSE: {response.json()}")
             #   self._buzzer_turn_on() 
            else:
                self._log(f"ERROR: HTTP {response.status_code}")

            response.close()
        except Exception as e:  # noqa: B902
            self._log(f"ERROR: {e}")
            self._lcd_out("ERROR: HUB REG")
            
            
    def _iot_hub_update(self):
        """Check in with IoT Hub and provide initial state."""
        reg_url = f"{self.config.get('api_endpoint')}/houses/{self.unique_id}"        
        self._log(f"_iot_hub_update: {self._state}")

        reg_info = {
            "unique_id": self.unique_id,
            "ip_address": self.wlan.ip_address,
            "state": self._state,
        }
        
        if self._state["motion"]["motion_alarm"] == True:
            reg_info["alarm"] = True
            reg_info["state"]["alarm"] = True
        
        reg_json = json_dumps(reg_info)

        self._log("Register with IoT Hub")
        self._log(f"* POST: {reg_json} -> {reg_url}")
        try:
            response = put_url(  # noqa: S113
                url=reg_url,
                data=reg_json,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code >= 200 and response.status_code <= 299:
                self._log(f"* RESPONSE: {response.json()}")
            else:
                self._log(f"ERROR: HTTP {response.status_code}")

            response.close()
        except Exception as e:  # noqa: B902
            self._log(f"ERROR: {e}")
            self._lcd_out("ERROR: HUB REG")




    def _iot_hub_timer_callback(self, t):
        """Raise update flag."""
        self._iot_hub_update_flag = True

        self._log("In _iot_hub_timer_callback, _iot_hub_update_flag = True")
        
        #update server and get update back
        reg_url = f"{self.config.get('api_endpoint')}/houses"

        try:
            response = get_url(reg_url)
            if response.status_code >= 200 and response.status_code <= 299:
                houses_from_response = response.json()
                globalAlarm = False
                print(houses_from_response)
                for house in houses_from_response:
                    # Access individual elements in the array
                    self._log("logging house from _iot_hub_timer_callback:")
                    self._log(house)
                    print("from server " + house["unique_id"])
                    if 'alarm' in house:
                        self._log(' alarm in house ' + house["unique_id"])
                        print("buzz", house["unique_id"])
                        self._buzzer_turn_on()
                        globalAlarm = True
                    else:
                       self._log("_iot_hub_timer_callback no alarm in house")
                        

                #if not globalAlarm:
                    # buzz false
                 
                 #print("globalAlarm is false ")
                  #  self._buzzer_turn_off()

                #else:
                    # buzz true
                 #   self._buzzer_turn_on()
                self._log(f"* RESPONSE: {response.json()}")
            else:
                self._log(f"ERROR: HTTP {response.status_code}")

            response.close()

        except Exception as e:  # noqa: B902
            self._log(f"ERROR: {e}")
            self._lcd_out("ERROR: HUB REG")



    def _lcd_out(self, msg="", clear=False, show_id=False):
        """Output message on LCD."""
        if clear:
            self.lcd.clear()

        self.lcd.move_to(0, 0)
        self.lcd.putstr(msg)

        if show_id:
            self.lcd.move_to(0, 1)
            self.lcd.putstr(self._state.get("wall_msg", ""))

    def _led_turn_off(self, _):
        self._log("Turning LED OFF")
        self.led.turn_off()

    def _led_turn_on(self, _):
        self._log("Turning LED ON")
        self.led.turn_on()

    def _buzzer_turn_off(self):
        self._log("Turning Buzzer OFF")
        self.buzzer.turn_off()

    def _buzzer_turn_on(self):
        self._log("Turning Buzzer ON")
        self.buzzer.turn_on()

    async def event_consumer(self):
        """Process events asynchronously."""
        self._log("hello from event_consumer")
        while True:
            if self.event_queue:
                self._log("len(self.event_queue) = ")
                event = self.event_queue.popleft()
                self.event_processor(event)

            if self._iot_hub_update_flag:
                self._log("Time to update IoT Hub")
                self._iot_hub_update_flag = False

            await sleep_ms(100)

    def event_processor(self, event):
        """Process event."""
        self._log(f"Got event: {event}")

        if event["source"] == "/in/motion":
            self._log(f"in motion: {event}")
            self._iot_hub_update()


        if event["source"] == "/in/button_a" and event["state"]["pressed"]:
            self.menu.move_next()
            self._lcd_out(self.menu.get_current_content())

        if event["source"] == "/in/button_b" and event["state"]["pressed"]:
           # self._log("about to toggle led")
           # self.led.toggle()
            menu_content = self.menu.get_current_content()
            menu_action = self.menu.get_current_action()

            if menu_action is not None:
                self._log(f"Execute action for menu item: {menu_content}")
                schedule(menu_action, 0)

    def run(self):
        """Execute main loop of the application."""
        self._lcd_out("Connecting...", clear=True, show_id=True)

        try:
            self.wlan.scan()
            self.wlan.connect()
        except RuntimeError as e:
            self._log(f"ERROR: {e}")
            self._lcd_out("ERROR: WIFI")
            self.exit_code = 1

        if self.exit_code == 0:
            self._iot_hub_register()

            self._lcd_out(self.menu.get_current_content())

            self.loop.create_task(self.event_consumer())

            self._log("Register event consumer")
            self._log("Enter event loop 1")
            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                self._log("Keyboard interrupt detected. Stopping...")

        self._log("Exit event loop")
