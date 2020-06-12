'''
  config.py
  \brief                 Global config file for gui
  \author                Brandon Manley
  \version               0.1
  \date                  06/08/20
  Support:               email to manley.329@osu.edu
'''

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
from PIL import ImageTk, Image

phase2_repo_dir = '/home/bmanley/Ph2_ACF/'
database = "testGui.db"

root = tk.Tk()
current_user = ''

# currently reviewing module info
review_best_plot = ''
review_latest_plot = ''
review_module_id = -1
review_sort_attr = tk.StringVar(root)
review_sort_attr.set('date')
review_sort_dir = tk.StringVar(root)
review_sort_dir.set('increasing')

review_filter_attr = tk.StringVar(root)
review_filter_attr.set('user')
review_filter_eq = tk.StringVar(root)
review_filter_eq.set('=')

module_results = []

# currently viewing result info
result_module_id = -1
result_row_id = -1

# currently testing module info
current_test_name = tk.StringVar(root)
current_test_name.set('pixelalive')
current_module_id = -1
current_test_num = -1
current_test_grade = -1
current_test_plot = ''
current_test_plot_location = ''

# testing
buttonStyle = ttk.Style()
buttonStyle.configure('Test.TButton', font=('Helvetica', 15), fg='blue')