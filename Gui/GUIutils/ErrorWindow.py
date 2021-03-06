'''
  ResultsWindow.py
  brief                 Window for showing the error messages
  author                Kai Wei
  version               0.1
  date                  09/24/20
  Support:              email to wei.856@osu.edu
'''

import tkinter as tk

class ErrorWindow(tk.Toplevel):
	def __init__(self, parent, text):
		tk.Toplevel.__init__(self, parent.root)
		self.master = parent.root
		self.title("ERROR")
		self.geometry("600x50")
		error_label = tk.Label(master=self, text=text, font=("Helvetica", 15, "bold"))
		error_label.pack(expand=True, fill=tk.BOTH)