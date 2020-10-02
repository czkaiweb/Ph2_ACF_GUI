'''
  ResultsWindow.py
  brief                 Window for continuing the test
  author                Kai Wei
  version               0.1
  date                  09/24/20
  Support:              email to wei.856@osu.edu
'''


import tkinter as tk

from tkinter import ttk

from Gui.GUIutils.RunWindow import *
from Gui.GUIutils.DBConnection import *
from Gui.GUIutils.ErrorWindow import *

class ContinueWindow(tk.Toplevel):
	def __init__(self, parent, dbconnection):
		tk.Toplevel.__init__(self, parent.root)
		self.parent = parent

		if self.parent.current_user == '':
			ErrorWindow(self.parent, "Error: Please login")
			return
		if not dbconnection:
			ErrorWindow(self.parent, "Error: No DB connection ")
			return
		self.dbconnection = dbconnection

		self.master = self.parent.root
		self.title('Continue testing')
		self.geometry("500x200")

		for row in range(1,5):
			self.rowconfigure(row, weight=1, minsize=40)

		self.rowconfigure(0, weight=1, minsize=20)
		self.rowconfigure(5, weight=1, minsize=20)
		self.columnconfigure(1, weight=1, minsize=200)
		self.columnconfigure(2, weight=1, minsize=200)
		self.columnconfigure(0, weight=1, minsize=50)
		self.columnconfigure(3, weight=1, minsize=50)

		self.start_label = tk.Label(master = self, text = "Start a new test", font=("Helvetica", 20, 'bold'))
		self.start_label.grid(row=1, column=1, columnspan=2, sticky="wen")

		self.moduleID_label = tk.Label(master = self, text = "Module ID", font=("Helvetica", 15))
		self.moduleID_label.grid(row=2, column=1, sticky='w')

		self.moduleID_entry = tk.Entry(master = self)
		self.moduleID_entry.grid(row=2, column=2, sticky='e')
		self.moduleID_entry.insert(0, str(self.parent.current_module_id))

		self.test_mode_label = tk.Label(master = self, text = "Test mode", font=("Helvetica", 15))
		self.test_mode_label.grid(row=3, column=1, sticky='w')

		#currentModes = []
		#for mode in list(database.retrieveAllModes()):
		#	currentModes.append(mode[1])
		current_calibrations = []
		for calibration in list(retrieveAllCalibrations(self.dbconnection)):
			current_calibrations.append(calibration[0])

		self.mode_menu = tk.OptionMenu(self, self.parent.current_test_name, current_calibrations)
		self.mode_menu.grid(row=3, column=2, sticky='e')

		self.start_button = ttk.Button(
			master = self,
			text = "Start test", 
			command = self.open_self
		)
		self.start_button.grid(row=4, column=1, columnspan=2)

	def open_self(self):
		try:
			self.parent.current_module_id = int(self.moduleID_entry.get())
		except:
			ErrorWindow(self.parent, "Error: Please enter valid module ID")
			return
		RunWindow(self.parent)
		self.destroy()
