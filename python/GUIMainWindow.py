
from tkinter import *
from tkinter import ttk
import tkinter as tk
import json

from GUIDisplayDeviceOut import *
from GUIDisplayDeviceIn import *
from GuiScheduleDisplay import *
from GuiDisplayLogic import *
from JsonParams import *
from ttkthemes import ThemedTk
from Logging import *

class GuiMainWindow( ):
    #def __init__(self, jsonSettings : json, devicesJson : json, sensorsJson : json , scheduleJson : json, logicJson : json):
    def __init__(self, ui_settings : JsonParams, devicesJson : JsonParams, sensorsJson : JsonParams , scheduleJson : JsonParams, logicJson : JsonParams):
         
        self.root = ThemedTk(theme="clam")

        self.devices = devicesJson
        self.sensors = sensorsJson
        self.logic   = logicJson

        self.tabControl = ttk.Notebook(self.root) 
        self.title  = ui_settings.getJson()[0]["title"]
        self.width  = ui_settings.getJson()[0]["width"]
        self.height = ui_settings.getJson()[0]["height"]
        dimStr = str(self.width) + "x" + str(self.height)
        logger.info(f"Creating window with title {self.title}")

        self.root.title( self.title)
        self.root.geometry( dimStr)

        tabListJson = ui_settings.getJson()[0]["tabs"]
        self.tabList = []
        for tabJson in tabListJson:
            tab = ttk.Frame(self.tabControl)
            self.tabList.append(tab)
            self.tabControl.add(tab, text =tabJson["title"]) 
            logger.info(f"adding tab {tabJson['title']}")
        
        self.tabControl.pack(fill ="both")

        self.deviceTab = GUIDisplayDeviceOut ( self.tabList[0], devicesJson, devicesJson.addWithoutKey, devicesJson.save_file, devicesJson.remove )
        self.sensorTab = GUIDisplayDeviceIn  ( self.tabList[1], sensorsJson, sensorsJson.addWithoutKey, sensorsJson.save_file, sensorsJson.remove )
        self.scheduleTab = GuiScheduleDisplay( self.tabList[2], scheduleJson.getJson(), scheduleJson.addWithoutKey, scheduleJson.save_file, scheduleJson.remove)
        self.logicTab = GuiDisplayLogic      ( self.tabList[3], logicJson, logicJson.addWithoutKey, logicJson.save_file, logicJson.remove)

        logger.debug("starting main GUI loop")
        self.root.mainloop()
