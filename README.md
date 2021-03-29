# Smart Home Remote-Access System
Client-server solution to access & control smart home devices remotely using TCP

## Setup
A technician is needed to configure the client, server, and connect the smart home devices to them. Once configured, the homeowner will be able to use all of the available features to make use of the device.

## Features
The system supports three classes of devices:
- Alarm
- Lights
- Locks

### Alarm
The alarm can be enabled or disabled by providing the PIN. The PIN can be changed by the homeowner.

### Lights
Lights are grouped into rooms. The system can support an unlimited number of rooms of lights. In each room, the light can be turned on or off, dimmed, or set to any color desired. All lights can be turned on or off at once.

### Locks
The system can support an unlimited number of locks. Each lock can be locked or unlocked by providing the PIN. The PINs can be changed by the homeowner.

The server is assumed to always be running. The client will connect and authenicate with the homeowner's credentials.