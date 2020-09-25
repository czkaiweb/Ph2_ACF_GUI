'''
  LoginFrame.py
  brief                 Login page for GUI
  author                Kai
  version               0.1
  date                  18/09/20
  Support:              email to wei.856@osu.edu
'''

import config
import database
import sys
import tkinter as tk
import os
import re
import operator
import math
import hashlib
from queue import Queue, Empty
from threading import Thread
from tkinter import ttk
from datetime import datetime
from subprocess import Popen, PIPE
from itertools import islice
from textwrap import dedent
from PIL import ImageTk, Image
from functools import partial
from tkinter import scrolledtext 

from Gui.GUIutils.ANSIColorText import *
from Gui.GUIutils.OptionFrame import *
from Gui.GUIutils.ErrorWindow import *

class LoginFrame(tk.Frame):
	def __init__(self):
		tk.Frame.__init__(self)

		self.cms_img = Image.open('icons/cmsicon.png')
		self.cms_img = self.cms_img.resize((70, 70), Image.ANTIALIAS)
		self.cms_photo = ImageTk.PhotoImage(self.cms_img)
		self.osu_img = Image.open('icons/osuicon.png')
		self.osu_img = self.osu_img.resize((160, 70), Image.ANTIALIAS)
		self.osu_photo = ImageTk.PhotoImage(self.osu_img)

		self.master = config.root
		self.config(width=600, height=300)

		self.grid(row=1, column=0, columnspan=2, sticky="nsew")
		self.rowconfigure(0, weight=1, minsize=35)
		self.rowconfigure(1, weight=1, minsize=25)
		self.rowconfigure(2, weight=1, minsize=40)
		self.rowconfigure(3, weight=1, minsize=30)
		self.rowconfigure(4, weight=1, minsize=65)
		self.rowconfigure(5, weight=1, minsize=55)
		self.columnconfigure(0, weight=1, minsize=300)
		self.columnconfigure(1, weight=1, minsize=300)
		self.grid_propagate(False)

		self.login_label = tk.Label(master = self, text = "Please login", font=("Helvetica", 20, 'bold'))
		self.login_label.grid(row=1, column=0, columnspan=2, sticky="n")

		self.username_label = tk.Label(master = self, text = "Username", font=("Helvetica", 15))
		self.username_label.grid(row=2, column=0, sticky='e')

		self.username_entry = tk.Entry(master = self, text='')
		self.username_entry.grid(row=2, column=1, sticky='w')

		self.password_label = tk.Label(master = self, text = "Password", font=("Helvetica", 15))
		self.password_label.grid(row=3, column=0, sticky='e')

		self.password_entry = tk.Entry(master = self, text='', show = "*")
		self.password_entry.grid(row=3, column=1, sticky='w')

		self.osu_label = tk.Label(master=self, image=self.osu_photo)
		self.osu_label.grid(row=5, column=0, sticky='ewns')

		self.cms_label = tk.Label(master=self, image=self.cms_photo)
		self.cms_label.grid(row=5, column=1, sticky='ewns')

		self.login_button = ttk.Button(
			master = self, 
			text = "Log in", 
			command = self.login_user
		)
		self.login_button.grid(row=4, column=0, columnspan=2)

		self.logout_button = ttk.Button(
			master = self, 
			text = "Log out", 
			command = self.logout_user
		)

		self.options_frame = OptionsFrame()


	def login_user(self):
		if self.username_entry.get() == '':
			ErrorWindow("Error: Please enter a valid username")
			return
		TryUsername = self.username_entry.get()
		TryPassword = self.password_entry.get()
		# Checking login info in encrypted way to be added

		config.current_user = self.username_entry.get()

		self.login_label['text'] = 'Welcome {0}'.format(config.current_user)
		self.login_label['font'] = ('Helvetica', 20, 'bold')

		self.username_label.grid_remove()
		self.username_entry.grid_remove()
		self.login_button.grid_remove()
		self.logout_button.grid(row=2, column=0, columnspan=2)
		self.options_frame.grid(row=1, column=1, sticky="es") #FIXME
		self.grid(row=1, column=0,  sticky="ws")
		self['width'] = 300
		self.columnconfigure(0, weight=1, minsize=150)
		self.columnconfigure(1, weight=1, minsize=150)


	def logout_user(self):
		config.current_user = ''

		self.login_label['text'] = 'Please login'
		self.login_label['font'] = ('Helvetica', 20, 'bold')
		self.username_label.grid()
		self.username_entry.grid()
		self.login_button.grid()
		
		self.logout_button.grid_remove()
		self.options_frame.grid_remove()
		self.grid(row=1, column=0,  sticky="news")
		self['width'] = 600
		self.columnconfigure(0, weight=1, minsize=300)
		self.columnconfigure(1, weight=1, minsize=300)


