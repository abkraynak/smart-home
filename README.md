# Smart Home Remote-Access System
Client-server solution to access & control smart home devices remotely using TCP
***
## Table of Contents
* [Features](#features)
* [Setup](#setup)
* [Technologies](#technologies)
***
## Features
The system supports three classes of devices:
* Alarm
* Lights
* Locks
### Alarm
The alarm can be enabled or disabled by providing the PIN. The PIN can be changed by the homeowner.
### Lights
Lights are grouped into rooms. The system can support an unlimited number of rooms of lights. In each room, the light can be turned on or off, dimmed, or set to any color desired. All lights can be turned on or off at once.
### Locks
The system can support an unlimited number of locks. Each lock can be locked or unlocked by providing the PIN. The PINs can be changed by the homeowner.
***
## Setup
A technician is needed to configure the client, server, and connect the smart home devices to them. Once configured, the homeowner will be able to use all of the available features to make use of the device. The server is assumed to always be running. The client will connect and authenicate with the homeowner's credentials.
***
## Technologies 
This project was completed using Python. Client-server communication relies on TCP for transport. A custom application protocol is used to send and interpret messages between devices. This system follows a thin-client architecture model, where most of the business logic is done on the server-side. The client only takes the user's input to send a request to the server, and display the result to the user. 
