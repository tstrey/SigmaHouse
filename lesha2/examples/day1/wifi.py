# -*- coding: utf-8 -*-
"""Stand-alone module to demo WiFi network connectivity."""
from binascii import hexlify
from time import sleep

import network

try:
    # Get wifi config from secrets.py
    from secrets import secret_config
except ImportError:
    print("ERROR: Configuration not defined")
    raise RuntimeError("No secrets.py to import")

print("WIFI: Initiating")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

wifi_connect_success = True
wifi_ssid = secret_config["wifi_ssid"]
wifi_pass = secret_config["wifi_pass"]

print("WIFI: Scanning")
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
        f"WIFI: Detected SSID: {wifi_ap_ssid:<30} |",
        f"BSSID: {wifi_ap_bssid} |",
        f"CH: {wifi_ap_channel:0>2} |",
        f"RSSI: {wifi_ap_rssi} |",
        f"AUTH: {wifi_ap_authmode} |",
        f"HID: {wifi_ap_hidden}",
    ]
    print(" ".join(wifi_ap_msg))

if wifi_ssid not in wifi_ssid_list:
    print(f"WIFI: SSID: '{wifi_ssid}' not detected")
    raise RuntimeError("Configured WIFI network not available")

if not wlan.isconnected():
    print(f"WIFI: Using SSID: {wifi_ssid}")
    print(f"WIFI: Using PASS: {wifi_pass}")
    wlan.connect(wifi_ssid, wifi_pass)

    wifi_connect_timeout = 10
    print(f"WIFI: Using TOUT: {wifi_connect_timeout}")

    while not wlan.isconnected():
        if wlan.status() == network.STAT_CONNECTING:
            print(f"WIFI: Connecting [timeout: {wifi_connect_timeout:0>2}s]")
        else:
            print(f"WIFI: Connecting with unexpected status: {wlan.status()}")

        sleep(1)  # wait 1 sec

        wifi_connect_timeout -= 1

        if wifi_connect_timeout == 0:
            wifi_connect_success = False
            break

if not wifi_connect_success:
    print(f"WIFI: Could not connect to SSID: {wifi_ssid}")
    raise RuntimeError("WIFI connection failed")
else:
    wifi_ip_address = wlan.ifconfig()[0]
    wifi_mac_address = hexlify(wlan.config("mac"), ":").decode("utf-8").upper()
    print(f"WIFI: Connected to SSID: {wifi_ssid}")
    print(f"WIFI: IP Address: {wifi_ip_address}")
    print(f"WIFI: MAC Address: {wifi_mac_address}")

print("WIFI: Disconnecting")
wlan.disconnect()
