
from tkinter import *
from tkinter import ttk
import tkinter as tk
import json


class GUIDisplayDevice:

    def __init__(self, root : Tk, json_data : json ):

        f = ttk.Frame(root)
        f['padding'] = (5,5,100,5)

        self.labelName = Label( root, text=str("Name: " + json_data["name"]), relief=RAISED )
        self.labelID = Label( root, text=str("ID:   " + json_data["id"]),   relief=RAISED )
        self.labelType = Label( root, text=str("Type:   " + json_data["id"]),   relief=RAISED )
        self.labelNumChannels = Label( root, text=str("NumChannels: " + str(json_data["numChannels"])),   relief=RAISED )
        self.labelName.pack()
        self.labelID.pack()
        self.labelType.pack()
        self.labelNumChannels.pack()

        pass

    def destroy(self):
        self.labelName.destroy()
        self.labelID.destroy()
        self.labelType.destroy()
        self.labelNumChannels.destroy()
        