# Smart House

[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)][PythonRef] [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][BlackRef] [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)][MITRef]

This repo contains code to demonstrate IoT and Smart Home concepts at Sigma Camp 2023 with [Keyestudio KS5009 Smart Home Model Kit][Keyestudio_KS5009]. It also contains project configs for linting with Flake8 and formatting with Black.

[PythonRef]: https://docs.python.org/3.7/
[BlackRef]: https://github.com/ambv/black
[MITRef]: https://opensource.org/licenses/MIT
[Keyestudio_KS5009]: https://wiki.keyestudio.com/KS5009_Keyestudio_Smart_Home

## Folder `examples`

Contains stand-alone modules to demonstrate different aspects of the main Smart House App.

* `day1/main.py` - Graceful WIFI connection
* `wip` - unstructured collection of test modules for Smart Home Kit from Keyestudio

## Folder `iot_hub`

Contains Flask-based implementation of IoT Hub API and UI server to communicate with all registered Smart Home models and manage them remotely.

## Folder `smart_house`

Contains Smart House App providing functionality to support student interactions with the Smart Home model as well as with the Mothership - Command & Control server to manage all Smart Home models connected within the same network.

Implements the following:

* [X] Centralized config with sensitive parameters
* [X] Class to manage the app itself
* [X] Class to manage WIFI connection
  * [X] Check if configured SSID is on the air
  * [X] Graceful connect with connection timeout
  * [X] Graceful disconnect if app encounters exceptions
* [X] Base class for abstract device with state
* [X] App method to register Smart Home model with the IoT Hub
* [X] Class to manage simple LED
* [X] Class to process input from buttons with interrupts
* [ ] App method to update the IoT Hub with data from all available sensors
* [ ] Class to manage addressable RGB LED panel
* [ ] Class to manage PIR sensor
* [X] Class to manage LCD display

To run, upload content to ESP32 and make sure `secrets.py` has correct SSID and password to establish WIFI connection.
