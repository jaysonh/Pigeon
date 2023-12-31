import json
from DeviceHandler import DeviceHandler
from DeviceInHandler import DeviceInHandler
from DeviceOutControl import DeviceOutControl
from DeviceInControl import DeviceInControl
from ActionSet import ActionSet
from ActionRamp import ActionRamp
from ActionRampTarget import *
from DeviceMQTT import DeviceMQTT
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from ScheduleAction import *
from JsonParams import *

class Scheduler:
    devices = {}        
    scheduleActions = {}    
    def __init__(self, schedule_json : JsonParams, devices : DeviceHandler, sensors : DeviceInControl ):

        print("starting scheduler")
        self.scheduler = BackgroundScheduler()
        for schedule_item in schedule_json.getJson():
            id = schedule_item["id"]
            deviceID = schedule_item["deviceID"]
            
            if schedule_item["action"]["type"] == "setData":
                action = ActionSet( schedule_item["action"] )
            elif schedule_item["action"]["type"] == "setRamp":
                action = ActionRamp( schedule_item["action"] )
            elif schedule_item["action"]["type"] == "setRampTarget":
                action = ActionRampTarget( schedule_item["action"] )
            else:
                action = None
                print("ERROR invalid action type")
            if action != None:
                self.scheduleActions[ id ] = ScheduleAction( schedule_item["deviceID"], devices.get( deviceID ), action) #ActionRampTarget( schedule_item["action"]["target"], schedule_item["action"]["duration"], schedule_item["action"]["interval"] )  )
            
            self.parse_cron( schedule_item["time"], self.scheduleActions[ id ].run )

        self.scheduler.start()

    def parse_cron( self, cron_time : str, action : ScheduleAction ):
        try:
            # all these are numbers represented as strings

            secCron  = cron_time.split(" ")[0]
            minCron  = cron_time.split(" ")[1]
            hourCron = cron_time.split(" ")[2] 
            dayMonthCron = cron_time.split(" ")[3]
            monthCron = cron_time.split(" ")[4]
            dayWeekCron = cron_time.split(" ")[5]

            self.scheduler.add_job(action, 'cron', second=secCron, minute=minCron, hour=hourCron, day_of_week=dayWeekCron, month=monthCron )

        except IndexError:
            print("Error: Invalid cron time format")

    