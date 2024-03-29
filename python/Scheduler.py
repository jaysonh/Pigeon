import json
from DeviceHandler import DeviceHandler
from DeviceInHandler import DeviceInHandler
from DeviceOutControl import DeviceOutControl
from DeviceInControl import DeviceInControl
from ActionSet import ActionSet
from ActionRamp import ActionRamp
from ActionRampTarget import *
from ActionSensor import *
from DeviceMQTT import DeviceMQTT
import threading
from apscheduler.schedulers.background import BackgroundScheduler

from ScheduleAction import *
from JsonParams import *
from Event import *

class Scheduler:
    devices = {}        
    scheduleActions = {}    
    def __init__(self, schedule_json : JsonParams, schedule_input_json : JsonParams, devices : DeviceHandler, sensors : DeviceInHandler ):

        logger.info(f"Loading Scheduler")
        self.scheduler = BackgroundScheduler()

        # Event scheduling
        self.updateScheduleEvent = Event()
        self.updateScheduleEvent += self.reloadSchedule

        self.removeScheduleEvent = Event()
        self.removeScheduleEvent += self.removeItem

        self.getNextRunTimesEvent = Event()
        self.getNextRunTimesEvent += self.getNextRunTimes

        self.devicesIn = devices
        for schedule_item in schedule_json.getJson():
            id = schedule_item["id"]
            logger.info(f"creating schedule action for{id}")
            self.scheduleActions[ id ] = self.createScheduleAction( schedule_item )
            self.add_job( schedule_item["time"], self.scheduleActions[ id ], id )

            
        self.devicesOut = sensors
        for schedule_item in schedule_input_json.getJson():
            id = schedule_item["id"]
            logger.info(f"creating schedule action for input{id}")
            self.scheduleActions[ id ] = self.createScheduleActionInput( schedule_item )
            self.add_job( schedule_item["time"], self.scheduleActions[ id ], id )

            
        logger.info(f"Starting scheduler")
        self.scheduler.start()

    def createScheduleActionInput(self, json_data : json) ->ScheduleAction:
        deviceID = json_data["deviceID"]
        if json_data["action"]["type"] == "sensor":
            action = ActionSensor( json_data["action"] )
        else:
            action = None

        if action != None:
            return ScheduleAction( deviceID, self.devicesOut.get( deviceID ), action) #ActionRampTarget( schedule_item["action"]["target"], schedule_item["action"]["duration"], schedule_item["action"]["interval"] )  )
        else:
            raise("ERROR invalid action type") 
        pass

    def createScheduleAction( self, json_data : json) -> ScheduleAction:
        deviceID = json_data["deviceID"]
        
        if json_data["action"]["type"] == "setData":
            action = ActionSet( json_data["action"] )
        elif json_data["action"]["type"] == "setRamp":
            action = ActionRamp( json_data["action"] )
        elif json_data["action"]["type"] == "setRampTarget":
            action = ActionRampTarget( json_data["action"] )
        elif json_data["action"]["type"] == "sensor":
            action = ActionSensor( json_data["action"] )
        else:
            action = None
            logger.error("ERROR invalid action type")

        if action != None:
            return ScheduleAction( deviceID, self.devicesIn.get( deviceID ), action) #ActionRampTarget( schedule_item["action"]["target"], schedule_item["action"]["duration"], schedule_item["action"]["interval"] )  )
        else:
            raise("ERROR invalid action type")   

    def getNextRunTimes(self ) -> []:

        job_list = []
        if self.scheduler.running == True:
            for job in self.scheduler.get_jobs():
                #job_list.append( job.next_run_time() )
                #print(job.next_run_time())
                t=0
        return job_list

    def reloadSchedule( self, cron_time : str, json_data : json ):
        logger.info(f"adding to schedule: {json_data}")
        id = json_data["id"]
        self.scheduleActions[ id ] = self.createScheduleAction( json_data)
        self.add_job( cron_time, self.scheduleActions[ id ], id )
        
    def removeItem( self, id : str):
        logger.info(f"removing job from scheduler: {id} {self.scheduleActions[ id ].getJobID()}")
        self.scheduler.remove_job( id )
        del (self.scheduleActions[ id ] )
        
    def stop(self):
        #logger.info("stopping sheduler")
        self.scheduler.remove_all_jobs()
        self.scheduler.shutdown()

    def add_job( self, cron_time : str, action : ScheduleAction, id : str  ):
        try:
            # all these are numbers represented as strings

            secCron      = cron_time.split(" ")[0]
            minCron      = cron_time.split(" ")[1]
            hourCron     = cron_time.split(" ")[2] 
            dayMonthCron = cron_time.split(" ")[3]
            monthCron    = cron_time.split(" ")[4]
            dayWeekCron  = cron_time.split(" ")[5]

            logger.info(f"Adding job to scheduler {secCron} {minCron} {hourCron} {dayMonthCron} {monthCron} {dayWeekCron} action: {action}")
            self.scheduler.add_job(action.run, 'cron', second=secCron, minute=minCron, hour=hourCron, day_of_week=dayWeekCron, month=monthCron,id= id, )
            
            action.setJobID( id )
        except IndexError:
            logger.error("Error: Invalid cron time format")

    