# ZenServer

This is intended to be the server for light control, acting as a hub for all lights on the local network

## Versions
- 1.0.0 -> Can statically color lights, have a standard communication protocol defined, can recieve device broadcasts

## Light Protocols
### Discovery
Lights will broadcast on the localnetwork at port 1260 a json of format
```json
{
    "name": "Device name",
    "strip": {
        "length": -999
    },
    "communication": {
        "protocols": [0, 1, 2]
    }
}
```
this broadcast will serve as both a heartbeat for the lights, at an interval of once a second

### Communication Protocols
Lights will listen for UDP data on port 1261, with messages formatted as | 1 byte opcode | rest of message  
all following subsections will describe the contents of the rest of data for a given opcode
#### 0
Description: Push the following array of data, formatted in a binary format to the lights
| 00000000 | rgbdata  
RGBdata is formatted as a sequence of 3 bytes representing rgb data
#### 1
Description: Push the following array of data, formatted in a human readable format
| 00000001 | rbdata as string
RGBdata is formatted as a sequence of r,g,b:r,g,b
#### 2
Description: Push the following data to specific indexes of lights
| 00000010 | data as a sequence of index,r,g,b:index,r,g,b

## Server Versions:
1 can display devices on network, as well as push static colors to each device