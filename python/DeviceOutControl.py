import json
from Logging import *

class DeviceValueRange:
    def __init__(self, json_data : json) -> None:
        self.min = json_data["min"]
        self.max = json_data["max"]
        logger.debug("Creating DeviceValueRange {self.min} {self.max}")
        
    def clamp(self, v : float) -> float:
        return max(min(v, self.max), self.min)
    
    def clampArr(self, arr : []) -> []:
        result = []
        for v in arr:
            result.append( max(min(v, self.max), self.min) )
        return result
    
class DeviceOutControl:
    
    value = 0.0

    def __init__(self, json_data : json ):
        self.numChannels = json_data["numChannels"]
        
        self.id = json_data["id"]
        self.range       = DeviceValueRange( json_data["range"] )

    def sendData(self, data = [] ):
        self.vals = data
        pass

    def getValues(self) -> []:
        return self.vals
    
    def getValue(self) -> int:
        return self.value
        
