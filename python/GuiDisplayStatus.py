from Scheduler import Scheduler
import tkinter as tk
from tkinter import ttk
from tkinter import *
import json
from Logging import *
from Event import *
import threading
import time
from MQTTHandler import *
import logging

class GuiDisplayStatus:
    deviceID = ""
    
    def __init__(self, root : tk ):
        self.start_time = time.time()

        logger.info("Initialising GuiStatusDisplay")
        self.parent = root
        
        # current time label
        frame_name_input = Frame(self.parent, bg="gray71")
        frame_name_input.pack(pady=2)
        self.current_time_label = tk.Label( frame_name_input, text="Current Time: ")
        self.current_time_label.grid(row=0, column=1)

        # uptime label
        frame_name_input = Frame(self.parent, bg="gray71")
        frame_name_input.pack(pady=2)
        self.uptime_label = tk.Label( frame_name_input, text="Uptime: ")
        self.uptime_label.grid(row=0, column=1)
        

        self.listbox = ttk.Treeview(root, columns=3,  show=["headings"], selectmode="browse")
        self.listbox["columns"]=("paramAddr","paramPort","paramConnStatus")
        self.listbox.pack(side="top", fill="both", expand=True)

        self.listbox.column("paramAddr", width=100 )
        self.listbox.column("paramPort", width=100 )
        self.listbox.column("paramConnStatus", width=100)
        self.listbox.heading("paramAddr", text="Address")
        self.listbox.heading("paramPort", text="Port")
        self.listbox.heading("paramConnStatus", text="Connection Status")


        self.bottomframe = Frame(root)
        self.bottomframe.pack( side = BOTTOM )

        #self.addButton = Button(self.bottomframe, text ="close", command = self.exitApp)
        #self.addButton.pack(side="right", fill="none", expand=False)

        
        m = MQTTHandler.getInstance()
        self.update_broker_info( m.get_broker_json() )

        self.uptimeThread = threading.Thread(target=self.updateUpTime)
        self.runningUptime = True
        self.uptimeThread.start()
        
        self.currentTimeThread = threading.Thread(target=self.updateCurrentTime)
        self.runningCurrentTime = True
        self.currentTimeThread.start()

    def stopThreads(self):
        self.runningUptime = False
        self.runningCurrentTime = False
        self.currentTimeThread.join()
        self.uptimeThread.join()

        
    def update_broker_info(self, broker_list : [] ):

        for broker in broker_list:
            broker_json = json.loads( broker )
            self.listbox.insert("", "end", text=broker_json["address"], values=(broker_json["address"], broker_json["port"], "connected" if broker_json["connection_status"] == True else "disconnected" ))
        
    def getUpTime(self)->str:
        elapsed_time = time.time() - self.start_time
        secs = int(elapsed_time) % 60
        min  = int(int(elapsed_time) / 60)% 60
        hour  = int(int(elapsed_time) /3600)% 24

        padding_lambda = lambda x,length: str(x) if x >= length else f"0{x}"

        timeStr = padding_lambda(hour,10) + ":" + padding_lambda(min,10) + ":" + padding_lambda(secs,10)
        return timeStr
    def updateUpTime(self):
        while self.runningUptime:
            # Code to be executed in the thread
            new_label = "Uptime: " + self.getUpTime()
            self.uptime_label.config(text=new_label)
            time.sleep(1)
            logger.debug("running up time thread")
        logger.debug("ending up time thread")

    def updateCurrentTime(self):
        while self.runningCurrentTime:
            # Code to be executed in the thread
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            self.current_time_label.config(text=current_time)      
            logger.debug("running current time thread")     
            time.sleep(1)
        logger.debug("ending current time thread")
        