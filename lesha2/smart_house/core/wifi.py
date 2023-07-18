# -*- coding: utf-8 -*-
"""Provides WiFi network connector class."""
from binascii import hexlify
from time import sleep_ms, time

from network import STAT_CONNECTING, STA_IF, WLAN


class NetworkWiFi:
    """Implements network connector for WiFi."""

    DEBUG = False

    ip_address = None
    mac_address = None

    def __init__(
        self,
        name="/net/wifi",
        wifi_ssid=None,
        wifi_pass=None,
        wifi_timeout=10,
        debug=False,
    ):
        """Initiate WiFi network object."""
        self._DEBUG = debug
        self._name = name

        self._log("Initiating")

        wlan = WLAN(STA_IF)
        wlan.active(True)
        wlan.disconnect()

        self._wlan = wlan
        self._wifi_ssid = wifi_ssid
        self._wifi_pass = wifi_pass

        # Defines timeout in seconds for establishing WiFi connection
        self._wifi_connect_timeout = wifi_timeout

    def _log(self, msg):
        """Print debug log to serial console."""
        if self._DEBUG:
            print(f"UPTIME[{time():0>4}s]:/log{self._name}: {msg}")

    def scan(self):
        """Scan WIFI networks to see if configured SSID is present."""
        wlan = self._wlan
        wifi_ssid = self._wifi_ssid

        self._log("Scanning")

        wifi_ap_list = wlan.scan()
        wifi_ssid_list = []

        for (
            wifi_ap_ssid,
            wifi_ap_bssid,
            wifi_ap_channel,
            wifi_ap_rssi,
            wifi_ap_authmode,
            wifi_ap_hidden,
        ) in wifi_ap_list:
            wifi_ap_ssid = wifi_ap_ssid.decode("utf-8")
            wifi_ssid_list.append(wifi_ap_ssid)

            wifi_ap_bssid = hexlify(wifi_ap_bssid, ":").decode("utf-8").upper()
            wifi_ap_msg = [
                f"Detected SSID: {wifi_ap_ssid:<30}",
                f"BSSID: {wifi_ap_bssid}",
                f"CH: {wifi_ap_channel:0>2}",
                f"RSSI: {wifi_ap_rssi}",
                f"AUTH: {wifi_ap_authmode}",
                f"HID: {wifi_ap_hidden}",
            ]

            self._log("|".join(wifi_ap_msg))

        if wifi_ssid not in wifi_ssid_list:
            self._log(f"SSID: '{wifi_ssid}' not detected")
            raise RuntimeError("Configured WIFI network not available")

    def connect(self):
        """Connect to WIFI network."""
        wifi_connect_success = True
        wifi_ssid = self._wifi_ssid
        wifi_pass = self._wifi_pass
        wlan = self._wlan

        if not wlan.isconnected():
            self._log(f"Using SSID: {wifi_ssid}")
            self._log(f"Using PASS: {wifi_pass}")

            wlan.connect(wifi_ssid, wifi_pass)

            wifi_connect_timeout = self._wifi_connect_timeout

            self._log(f"Using TOUT: {wifi_connect_timeout}s")

            while not wlan.isconnected():
                if wlan.status() == STAT_CONNECTING:
                    self._log(f"Connecting [timeout: {wifi_connect_timeout:0>2}s]")
                else:
                    self._log(f"Connecting with unexpected status: {wlan.status()}")

                sleep_ms(1000)

                wifi_connect_timeout -= 1

                if wifi_connect_timeout == 0:
                    wifi_connect_success = False
                    break

        if not wifi_connect_success:
            self._log(f"Could not connect to SSID: {wifi_ssid}")
            raise RuntimeError("WIFI connection failed")
        else:
            self.ip_address = wlan.ifconfig()[0]
            self.mac_address = hexlify(wlan.config("mac"), ":").decode("utf-8").upper()

            self._log(f"Connected to SSID: {wifi_ssid}")
            self._log(f"IP Address: {self.ip_address}")
            self._log(f"MAC Address: {self.mac_address}")

    def disconnect(self):
        """Disconnect from WIFI network."""
        self._log("Disconnecting")

        self._wlan.disconnect()
