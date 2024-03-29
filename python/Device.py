import json
from MQTTHandler import *
from DeviceDMXFTDI import DeviceDMXFTDI
from DeviceRebble import DeviceRebble
from DeviceMQTT import *
from DeviceOSC import *
from DeviceKKC import *
from DeviceCommandLine import *
from DeviceArtnet import *
from Logging import *

class Device:
    
    value = 0

    def __init__(self, json_data : json ):
        
        self.id          = json_data["id"]
        self.name        = json_data["name"]
        self.numChannels = json_data["numChannels"]
        self.type        = json_data["type"]

        logger.info(f"Creating device {self.id} {self.name} {self.type}")

        # select the device type
        if( self.type == "dmxftdi"):
            self.outputDevice = DeviceDMXFTDI(json_data  )
        elif( self.type == "artnet"):
            self.outputDevice = DeviceArtnet( json_data  )
        elif( self.type == "rebble"):
            self.outputDevice = DeviceRebble( json_data  )
        elif( self.type == "mqtt"):
            self.outputDevice = DeviceMQTT( json_data )   
        elif( self.type == "osc"):
            self.outputDevice = DeviceOSC( json_data  )  
        elif( self.type == "kkc"):
            self.outputDevice = DeviceKKC( json_data  )   
        elif( self.type == "command_line"):
            self.outputDevice = DeviceCommandLine( json_data )   
        else:
            raise  Exception(f"Invalid device type: {self.type}")
    
    def stopThread(self):
        self.outputDevice.stop()
        
    def stop(self):
        self.outputDevice.stop()
        
    def sendData(self, data = [] ):
        logger.debug(f"sending data {data}")
        self.outputDevice.sendData( data )
        
    def getValue(self) -> int:
        return self.outputDevice.getValue()
    
    def getValues(self) -> []:
        return self.outputDevice.getValues()
