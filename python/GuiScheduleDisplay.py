from Scheduler import Scheduler
import tkinter as tk
from tkinter import ttk
from tkinter import *
import json

class GuiScheduleDisplay:
    deviceID = ""
    
    def __init__(self, root : tk , json_data : json , addJsonFunc = None, saveJsonFunc = None):

        self.parent = root
        self.addJsonFunc = addJsonFunc
        self.schedule = json_data
        self.listbox = ttk.Treeview(root, columns=("Column1", "Column2", "Column3", "Column4", "Column5"))
        self.listbox.pack(side="top", fill="both", expand=True)

        #self.listbox.insert("", "end", text=f"Name:", values=(json_data["name"] ))
        #self.listbox.insert("", "end", text=f"ID: ", values=(json_data["id"],  ))
        #self.listbox.insert("", "end", text=f"Type: ", values=(json_data["type"] ))
        #self.listbox.insert("", "end", text=f"Num Channels: ", values=(json_data["numChannels"] ))

        for job in json_data:
            self.listbox.insert("", "end", text=job["id"], values=( job["time"], job["deviceID"], job["address"], "next run:", job["action"] ))
            print(job)

                
        self.bottomframe = Frame(root)
        self.bottomframe.pack( side = BOTTOM )

        self.addButton = Button(self.bottomframe, text ="add", command = self.openAddScheduleDialog)
        self.addButton.pack(side="right", fill="none", expand=False)

        
        self.removeButton = Button(self.bottomframe, text ="remove", command = self.removeScheduleItem)
        self.removeButton.pack(side="left", fill="none", expand=False)

        self.saveButton = Button(self.bottomframe, text ="save", command = saveJsonFunc)
        self.saveButton.pack(side="left", fill="none", expand=False)

        pass
        #self.schedule = schedule

    def replaceDevicesListBox(self, items : json):
        
        # clear treeview
        self.listbox.delete(*self.listbox.get_children())

        # add data to the treeview
        for job in items:
            print( "job[id]: " + job["id"])
            self.listbox.insert("", "end", text=job["id"], values=( job["time"], job["deviceID"], job["address"], "next run:", job["action"] ))          
        pass

    def closeDialog(self):
        self.pop.destroy()
        self.pop.update()

    def get_action(self, selection : str) -> json:
        action_json = {""}
        if selection == "ActionRamp":
            
            action_json = { "type"     : "setRamp",
                            "start"    : self.get_elements(self.action_ramp_start_input.get("1.0", "end-1c")),
                            "end"      : self.get_elements(self.action_ramp_end_input.get("1.0", "end-1c")),
                            "duration" : self.action_ramp_duration_input.get("1.0", "end-1c"),
                            "interval" : self.action_ramp_interval_input.get("1.0", "end-1c") } 
                      
            
        elif selection == "ActionRampTarget":
            
            action_json = { "type"  : "setRampTarget",
                            "target"   : self.get_elements(self.action_ramp_end_input.get("1.0", "end-1c")),
                            "duration" : self.action_ramp_duration_input.get("1.0", "end-1c"),
                            "interval" : self.action_ramp_interval_input.get("1.0", "end-1c") } 
            
            
        elif selection == "ActionSet":
            
            action_json = { "type"  : "setData",
                            "value" : self.get_elements( self.action_set_input.get("1.0", "end-1c")) } 
        
        print(f"action_json: {action_json}")
        return action_json
    
    def get_elements(self, input : str):
        value = 0
        valueStr = input #self.action_set_input.get("1.0", "end-1c")
        numElements = len(valueStr.split(',') )
        if numElements == 1:
            value = int(valueStr)
        else:
            value = valueStr.split(',')
            value = [int(x) for x in value]
        return value 
        
        pass
    def okDialog(self):
        json_data = { "name" : self.name_input.get("1.0", 'end-1c'), 
                       "id" : self.name_input.get("1.0", 'end-1c'),
                       "time" : "* * * * ",
                       "deviceID" : self.device_id_input.get("1.0", 'end-1c'),
                       "address" : self.address_input.get("1.0", 'end-1c'),
                       "next run" : "",
                       #"action" : self.action_input.get("1.0", 'end-1c')
                       "action" : self.get_action(self.action_str.get())
                       }
        
        
        self.addJsonFunc( json_data )
        #print("close dialog: " + self.cron_day_week_var.get())
        cron_str = self.cron_day_week_var .get() + " " + self.cron_month_var.get() + " " + self.cron_day_var.get() + " " + self.cron_hour_var.get() + " " + self.cron_minute_var.get() + " " + self.cron_second_var.get()
        self.add_schedule( cron_str )
        self.replaceDevicesListBox( self.schedule)
        self.pop.destroy()
        self.pop.update()

    def add_schedule( self, cron_str ):

        print("adding schedule: " + cron_str)
        pass

    def openAddScheduleDialog(self):
        #global pop
        self.pop = Toplevel(self.parent)
        self.pop.title("Add Schedule Item")
        self.pop.geometry("450x250")
        self.pop.config(bg="white")
        
        # schedule id input
        frame_id_input = Frame(self.pop, bg="gray71")
        frame_id_input.pack(pady=2)
        id_label = tk.Label( frame_id_input, text="id")
        id_label.grid(row=0, column=1)
        self.id_input = tk.Text(frame_id_input, 
                   height = 1, 
                   width = 20) 
        self.id_input.grid(row=0, column=2)

        # schedule name input
        frame_name_input = Frame(self.pop, bg="gray71")
        frame_name_input.pack(pady=2)
        name_label = tk.Label( frame_id_input, text="id")
        name_label.grid(row=0, column=1)
        self.name_input = tk.Text(frame_id_input, 
                   height = 1, 
                   width = 20) 
        self.name_input.grid(row=0, column=2)
        
        # cron schedule input
        frame_cron_input = Frame(self.pop, bg="gray71")
        frame_cron_input.pack(pady=2)
        cron_label = tk.Label( frame_cron_input, text="schedule time")
        cron_label.grid(row=0, column=1)

        cron_second_label = tk.Label( frame_cron_input, text="sec")
        cron_second_label.grid(row=0, column=2)
        self.cron_second_var = tk.StringVar() 
        cron_second = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_second_var)
        cron_second['values'] = ('*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59' ) 
        cron_second.current(0)
        cron_second.grid(row = 0, column = 3) 
        
        cron_minute_label = tk.Label( frame_cron_input, text="min")
        cron_minute_label.grid(row=0, column=4)
        self.cron_minute_var = tk.StringVar() 
        cron_minute = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_minute_var)
        cron_minute['values'] = ('*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59') 
        cron_minute.current(0)
        cron_minute.grid(row = 0, column = 5) 
     
        cron_hour_label = tk.Label( frame_cron_input, text="hour")
        cron_hour_label.grid(row=0, column=5)
        self.cron_hour_var = tk.StringVar() 
        cron_hour = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_hour_var)
        cron_hour['values'] = ( '*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24' ) 
        cron_hour.current(0)
        cron_hour.grid(row = 0, column = 6) 
        
        cron_day_label = tk.Label( frame_cron_input, text="day")
        cron_day_label.grid(row=0, column=7)
        self.cron_day_var = tk.StringVar() 
        cron_day = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_day_var)
        cron_day['values'] = ('*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31') 
        cron_day.current(0)
        cron_day.grid(row = 0, column = 8) 

        cron_month_label = tk.Label( frame_cron_input, text="month")
        cron_month_label.grid(row=0, column=9)
        self.cron_month_var = tk.StringVar() 
        cron_month = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_month_var)
        cron_month['values'] = ('*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12') 
        cron_month.current(0)
        cron_month.grid(row = 0, column = 10) 
        
        cron_day_week_label = tk.Label( frame_cron_input, text="day_week")
        cron_day_week_label.grid(row=0, column=11)
        self.cron_day_week_var = tk.StringVar() 
        cron_day_week = ttk.Combobox(frame_cron_input, width = 2, textvariable = self.cron_day_week_var)
        cron_day_week['values'] = ('*', '1', '2', '3', '4', '5', '6', '7') 
        cron_day_week.current(0)
        cron_day_week.grid(row = 0, column = 12) 


        # device id input
        frame_device_id_input = Frame(self.pop, bg="gray71")
        frame_device_id_input.pack(pady=2)
        device_id_label = tk.Label( frame_device_id_input, text="device id")
        device_id_label.grid(row=0, column=1)
        self.device_id_input = tk.Text(frame_device_id_input, 
                   height = 1, 
                   width = 20) 
        self.device_id_input.grid(row=0, column=2)

        # address input
        frame_address_input = Frame(self.pop, bg="gray71")
        frame_address_input.pack(pady=2)
        address_label = tk.Label( frame_address_input, text="address")
        address_label.grid(row=0, column=1)
        self.address_input = tk.Text(frame_address_input, 
                   height = 1, 
                   width = 20) 
        self.address_input.grid(row=0, column=2)

        # action input
        frame_action_input = Frame(self.pop, bg="gray71")
        frame_action_input.pack(pady=2)
        action_label = tk.Label( frame_action_input, text="action")
        action_label.grid(row=0, column=1)
        #self.action_input = tk.Text(frame_action_input, 
        #           height = 5, 
        #           width = 20) 
        #self.action_input.grid(row=0, column=2)
        self.action_str = tk.StringVar() 
        action_select = ttk.Combobox(frame_action_input, width = 20, textvariable = self.action_str)
        action_select['values'] = ('ActionSet', 'ActionRamp', 'ActionRampTarget') 
        action_select.current(0)
        action_select.grid(row = 0, column = 12) 
        action_select.bind('<<ComboboxSelected>>', self.action_select_change)

        self.action_set_frame = Frame(self.pop, bg="gray71")
        self.action_set_frame.pack(pady=2)


        # Add a Frame
        self.frameBtns = Frame(self.pop, bg="gray71")
        self.frameBtns.pack(pady=10)
        # Add Button for making selection
        self.button1 = Button(self.frameBtns, text="add", command=self.okDialog, bg="grey", fg="white")
        self.button1.grid(row=0, column=1)
        self.button2 = Button(self.frameBtns, text="cancel", command= self.closeDialog, bg="grey", fg="white")
        self.button2.grid(row=0, column=2)

        self.change_action("ActionSet")
        pass

    def action_select_change(self, event):
        print(f"action selected {self.action_str.get()}")
        selection = self.action_str.get()
        self.change_action(self.action_str.get())
        
        
    def change_action(self, selection):
        if selection == "ActionRamp":
            self.action_set_frame.destroy()
            self.action_set_frame.update()
            self.action_set_frame = Frame(self.pop, bg="gray71")
            self.action_set_frame.pack(pady=2)
            action_ramp_start_label = tk.Label( self.action_set_frame, text="Start Value")
            action_ramp_start_label.grid(row=0, column=1)
            self.action_ramp_start_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_start_input.grid(row=0, column=2)
            action_ramp_end_label = tk.Label( self.action_set_frame, text="End Value")
            action_ramp_end_label.grid(row=1, column=1)
            self.action_ramp_end_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_end_input.grid(row=1, column=2)
            action_ramp_duration_label = tk.Label( self.action_set_frame, text="Duration")
            action_ramp_duration_label.grid(row=2, column=1)
            self.action_ramp_duration_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_duration_input.grid(row=2, column=2)
            action_ramp_interval_label = tk.Label( self.action_set_frame, text="Interval")
            action_ramp_interval_label.grid(row=3, column=1)
            self.action_ramp_interval_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_interval_input.grid(row=3, column=2)
            num_channels_label = tk.Label( self.action_set_frame, text="Num Channels")
            num_channels_label.grid(row=4, column=1)
            self.num_channels_str = tk.StringVar() 
            num_channels_select = ttk.Combobox(self.action_set_frame, width = 4, textvariable = self.num_channels_str)
            num_channels_select['values'] = ( '1', '2', '3', '4', '5', '6', '7', '8', '9', '10') 
            num_channels_select.current(0)
            num_channels_select.grid(row = 4, column = 2) 
            num_channels_select.bind('<<ComboboxSelected>>', self.action_set_num_channels)
            
        elif selection == "ActionRampTarget":
            self.action_set_frame.destroy()
            self.action_set_frame.update()
            self.action_set_frame = Frame(self.pop, bg="gray71")
            self.action_set_frame.pack(pady=2)
            action_ramp_end_label = tk.Label( self.action_set_frame, text="End Value")
            action_ramp_end_label.grid(row=0, column=1)
            self.action_ramp_target_end_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_target_end_input.grid(row=0, column=2)
            action_ramp_target_duration_input = tk.Label( self.action_set_frame, text="Duration")
            action_ramp_target_duration_input.grid(row=1, column=1)
            self.action_ramp_target_duration_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramp_target_duration_input.grid(row=1, column=2)
            action_ramp_target_interval_label = tk.Label( self.action_set_frame, text="Interval")
            action_ramp_target_interval_label.grid(row=2, column=1)
            self.action_ramptarget_interval_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_ramptarget_interval_input.grid(row=2, column=2)
            num_channels_label = tk.Label( self.action_set_frame, text="Num Channels")
            num_channels_label.grid(row=3, column=1)
            self.num_channels_str = tk.StringVar() 
            num_channels_select = ttk.Combobox(self.action_set_frame, width = 4, textvariable = self.num_channels_str)
            num_channels_select['values'] = ( '1', '2', '3', '4', '5', '6', '7', '8', '9', '10') 
            num_channels_select.current(0)
            num_channels_select.grid(row = 3, column = 2) 
            num_channels_select.bind('<<ComboboxSelected>>', self.action_set_num_channels)
            
        elif selection == "ActionSet":
            self.action_set_frame.destroy()
            self.action_set_frame.update()
            self.action_set_frame = Frame(self.pop, bg="gray71")
            self.action_set_frame.pack(pady=2)
            action_set_label = tk.Label( self.action_set_frame, text="Values(seperate with a comma)")
            action_set_label.grid(row=0, column=1)
            self.action_set_input = tk.Text(self.action_set_frame, height = 1, width = 20) 
            self.action_set_input.grid(row=0, column=2)
            num_channels_label = tk.Label( self.action_set_frame, text="Num Channels")
            num_channels_label.grid(row=1, column=1)
            self.num_channels_str = tk.StringVar() 
            num_channels_select = ttk.Combobox(self.action_set_frame, width = 4, textvariable = self.num_channels_str)
            num_channels_select['values'] = ( '1', '2', '3', '4', '5', '6', '7', '8', '9', '10') 
            num_channels_select.current(0)
            num_channels_select.grid(row = 1, column = 2) 
            num_channels_select.bind('<<ComboboxSelected>>', self.action_set_num_channels)
            
        # Add Button for making selection
        self.frameBtns.destroy()
        self.frameBtns.update()
        self.frameBtns = Frame(self.pop, bg="gray71")
        self.frameBtns.pack(pady=10)
        self.button1 = Button(self.frameBtns, text="add", command=self.okDialog, bg="grey", fg="white")
        self.button1.grid(row=4, column=1)
        self.button2 = Button(self.frameBtns, text="cancel", command= self.closeDialog, bg="grey", fg="white")
        self.button2.grid(row=4, column=2)

    def action_set_num_channels(self, event):
        pass

    def fromJson(self, json_data : json):   
        pass        

    def removeScheduleItem(self):
        selected = self.listbox.selection()
        current_idx = self.listbox.index(selected)
        self.listbox.delete(selected)
        pass