import json
import paho.mqtt.client as mqtt 
from MQTTHandler import MQTTHandler
from DeviceOutControl import DeviceOutControl
from Logging import *

class DeviceKKC(DeviceOutControl):
    
    def __init__(self, json_data : json):
        super().__init__( json_data )
        logger.info("Creating device MQTT")
        
        m = MQTTHandler.getInstance()
        self.topic = json_data["topic"]
        self.mqtt = m.add_broker( json_data["broker"]  )

    def sendData(self, data = []):
        
        self.vals = data
        
        idata = []
        for x in data:
            idata.append(hex(int(x)))

        send_arr = ['0xa5', '0x01'] + idata
        byte_arr = bytes([int(x,0) for x in send_arr])

        logger.debug(f"sendData KKC MQTT: {data} as bye array: {byte_arr} to {self.topic}")
        self.mqtt.send_msg( self.topic, byte_arr )
    
    def stop(self):
        self.mqtt.disconnect()
        pass

    def getValues(self):
        return self.vals