---
tags:
  - notes
  - personal
  - semilab:iot
  - sigmacamp:2023
---
# IoT and Smart Home Semilab for Sigma Camp 2023

Curriculum for IoT & Smart Home Semilab for beginners (kids 12-14 years old).

## Registration Page Description

This semilabs series will take you on a journey through the exciting world of Internet of Things (IoT). Our seminar and lab activities would revolve around a versatile model emulating a smart house with an ESP32 microcontroller and a set of sensors, actuators and other cool peripherals like buzzers, LCD displays, buttons and LED lights.

With the help of our smart house model and a bit of simple Python code we will explore different engineering concepts crucial for making efficient, reliable and secure IoT solutions. In a beginner-friendly manner our labs will touch on real-world engineering challenges and solutions spanning the plethora of subjects like Networking, Client-Server Architecture and Web-based User Interfaces as well as some introductory aspects of Cyber Security.

Wait! There's more! While participants are encouraged to write their own beginner-level Python code as part of the labs, all the necessary code excerpts will be provided upon request to allow those at the beginning of their Python journey to follow along. That's not all! In addition to the new knowledge, skills and fun memories our campers will bring home their very own smart house model and associated development environment to continue the IoT journey in their own way.

## Learning Outline

### Day 1 - Overview

[1]: https://en.wikipedia.org/wiki/Internet_of_things
[2]: https://en.wikipedia.org/wiki/OSI_model#Layer_architecture
[3]: https://en.wikipedia.org/wiki/Encapsulation_(networking)
[4]: https://en.wikipedia.org/wiki/Security_through_obscurity
[5]: https://en.wikipedia.org/wiki/Observability

#### Introducing instructors (5 mins)

* Introduce yourself and briefly describe your background.

#### Ice breaker activity (5 mins)

* Play a game with the audience where you are a kitchen robot taking verbal commands to make a peanut butter and jelly sandwich. The goal is to misinterpret vague human language commands and make a fun demonstration that algorithms need to be very detail oriented and different failure modes need to be thought through in advance.

#### What is IoT and why people need it (10 mins)

* Ask the audience if they know what the Internet of things (IoT) is. Ask them to name examples of IoT devices. The goal is to get the audience in the mood for the collaborative discussion and idea generation. Facilitate the discussion with the goal to arrive at the following definition.

  > The Internet of things (IoT) describes physical objects (or groups of such objects) with sensors, processing ability, software and other technologies that connect and exchange data with other devices and systems over the Internet or other communications networks. [1]

* As an example, review with the audience a dusk-to-dawn light bulb. Such device contains a LED and a light sensor packaged together in a form of a lightbulb. It turns on when ambient light is low and turns off when ambient light crosses pre-defined threshold.

* Ask the audience if they think the dusk-to-dawn light bulb is an IoT device.

  * It is not an IoT devices because it does not provide or consume any data over communications network and has no processing capabilities.

  * This **stand-alone device** is very limited in how it could be used. E.g.:
    * With all other things being equal, you could not turn it on 15 or 20 minutes before the sun down.
    * If you install it in a tinted or frosted glass fixture or indoors, it will distort light sensor's function

* Now, review an example of a **smart device** like a light bulb that can change color and brightness. To be useful for consumers it has to be a device with some sort of connectivity supported to **communicate** with it and processing capabilities to change the bulb's **state** (color and brightness).

* Ask the audience if now they have an understanding why people invented IoT devices to replace their stand-alone cousins?

  * IoT devices allow to **integrate** products from different vendors into more complex systems like Smart Buildings or Smart Cities.

  * They offer flexibility allowing to achieve higher levels of control and hence efficiency and overall quality of life not available with regular stand-alone devices.

#### How most IoTs communicate [10 mins]

* As a recap, summarize that all IoT devices have a **state** and a capability to **send** that state or change it based on some input **received** through a **communications channel**.

* IoT devices receive and (sometimes) send **data** using different means of **encoding** and **transport** mechanisms. OSI model is a good foundation to structure understanding of all the different ways interconnected systems rely on to communicate data.

* Go through the [OSI diagram][2] and describe different levels with examples. Note that many communication protocols encompass more than one layer of OSI. Two most common physical layers are:
  * Wires
    * Local Area Network - LAN
      * Ethernet is a good example of a LAN protocol ubiquitous for schools and offices to connect computers, printers and many other stationary devices like CCTV cameras.
    * Controller Area Network - CAN
      * Vehicle bus standard designed to allow devices like microcontrollers to communicate with each other without a host computer.

  * Radio waves
    * Wi-Fi - Used to get wireless LAN equivalent using 2.4 and 5 GHz frequency
    * Bluetooth/LE - Short-range wireless technology standard that is used for exchanging data between low-powered fixed and mobile devices over short distances

* Note that the most important aspect of the OSI model is the data **encapsulation principle**. [3]

  * **Encapsulation** is the process of concatenating layer-specific headers or tailers with a payload (data) from higher layer for transmission/processing on lower layer.

  * **De-encapsulation** is the reverse process for receiving information; it removes previously concatenated header or tailer that an underlying communications layer transmitted.

  * **Encapsulation** and **de-encapsulation** allow the design of modular communication protocols so to logically separate the function of each communications layer, and **abstract** the structure of the communicated information over the other communications layers.

  * It should be mentioned that encapsulation/de-encapsulation processes can also serve as malicious features like in the tunneling protocols (hiding one protocol in another).

* Our Lab activities will built on the following network protocols:

  * **Internet Protocol (IP)** - Network layer protocol for Structuring and managing a multi-node network, including addressing, routing and traffic control.

  * **Transmission Control Protocol (TCP)** - Transport layer protocol for reliable transmission of data segments between points on a network, including segmentation, acknowledgement and multiplexing.

  * **Hypertext Transfer Protocol (HTTP)** - Application layer protocol in the Internet protocol suite model for distributed, collaborative, hypermedia information systems

#### Lab 1 - Local WIFI connectivity (30 mins)

* Local WIFI network supplies connectivity for all other lab activities. So this lab ensures that audience has the connectivity on their laptops and can do basic troubleshooting. It also demonstrates more of the inner working of an IP-based network.

* Start with connecting each laptop to the lab WIFI. Explain what is the WIFI SSID and why commonly used cybersecurity recommendation to configure WIFI Access Ponts (APs) to "hide" SSID advertisement is inefficient. Explain that in general [security through obscurity][4] strategy never works and most of the times leads to failure in security engineering.

* Show how to open the OS command line prompt and check the details of the WIFI connection including the MAC address of the physical radio interface and IP address assigned by the network.

* Show the first step of troubleshooting any IP-based connectivity with **ping** and **traceroute** tools.

#### Lab 2 - ESP32 WIFI + HTTP (30 mins)

This lab ensures that smart home models can reach the Command and Control (C2) aka Mothership server through the lab WIFI. It also introduces the DEV environment and a way to work with ESP32 microcontroller board.

* Review the Thonny IDE and especially the concept of **serial interface** and how to use it in Thonny. Connect ESP32 board over USB to a laptop and show example of REPL programming to turn an LED on/off.

* Review the code that makes WIFI connection. Stop to explain the **observability** in application to IoT in general and our smart house model specifically.
  * **Observability** is a measure of how well internal states of a system can be inferred from knowledge of its external outputs. [5]

  * Point out the places where code checks for failure states (e.g. no SSID present, wrong password, etc.) and how outcomes are communicated to the world (printing status on LCD, blinking LED, etc).

* Review the code making a registration to the Mothership. Discuss how secrets should be handled in code and why.

### Day 2

* sensor exploration: buttons / led, button / vent, motion sensor, buzzer, display, etc?
* [OK] (theory): hardware principal for each sensor
* [LF] (theory): TBD

### Day 3

* server turns vent (Lilia - code server to accept POST / GET requests and communicate back TODO command based on the button pressed on the web page (i.e. - turn the light on, turn the fan on, buzz; Lesha - code esp32 to accept json and act on),
* Task for kids: add one more end-point in a similar format
* All examples will be pre-coded for kids

### Day 4

* kids assemble houses, Jessica / Alyssa and TA's will be actively helping

### Day 5

* test assembled houses communication with the server, bonus: enable house-to-house communication (motion server on one house will activate alarm on all via the server - Lilia), Lesha will talk about security aspect of iOT communication, Q & A .. curtains :)