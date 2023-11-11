from Configuration import Configuration
from DeviceHandler import DeviceHandler
from Scheduler import Scheduler
import schedule
import time


version = "0.0.1"
if __name__ == "__main__":
    print(f"Pigeon version {version}")

    configuration = Configuration( ["../data/config/devicesOut.json", "../data/config/devicesIn.json", "../data/config/schedule.json"] )
    device_handler = DeviceHandler( configuration.get("devicesOut"), configuration.get("devicesIn") )
    scheduler      = Scheduler( configuration.get("schedule"))
    
    while True:
        schedule.run_pending()
        time.sleep(1)
   