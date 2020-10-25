from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QStyleFactory, QTableView, QTableWidget, QTabWidget, QTextEdit, QHBoxLayout,
		QVBoxLayout, QWidget, QMainWindow, QMessageBox, QSplitter)

import sys
import os
import subprocess
from subprocess import Popen, PIPE

from Gui.GUIutils.DBConnection import *
from Gui.GUIutils.guiUtils import *
from Gui.QtGUIutils.QtStartWindow import *
from Gui.QtGUIutils.QtTableWidget import *

class QtModuleReviewWindow(QWidget):
	def __init__(self,master, info):
		super(QtModuleReviewWindow,self).__init__()
		self.master = master
		self.info = info
		self.connection = self.master.connection
		self.GroupBoxSeg = [1, 10,  1]
		#Fixme: QTimer to be added to update the page automatically

		self.mainLayout = QGridLayout()
		self.setLayout(self.mainLayout)

		self.setLoginUI()
		self.createHeadLine()
		self.createMain()
		self.createApp()

	def setLoginUI(self):
		self.setGeometry(200, 200, 1000, 1600)  
		self.setWindowTitle('Module Review Page')  
		self.show()

	def createHeadLine(self):
		self.HeadBox = QGroupBox()

		self.HeadLayout = QHBoxLayout()

		HeadLabel = QLabel('<font size="4"> Module: {0} </font>'.format(self.info))
		HeadLabel.setMaximumHeight(30)

		statusString, colorString = checkDBConnection(self.connection)
		StatusLabel = QLabel()
		StatusLabel.setText(statusString)
		StatusLabel.setStyleSheet(colorString)

		self.ConnectButton = QPushButton("&Connect to DB")
		self.ConnectButton.clicked.connect(self.connectDB)

		self.HeadLayout.addWidget(HeadLabel)
		self.HeadLayout.addStretch(1)
		self.HeadLayout.addWidget(StatusLabel)
		self.HeadLayout.addWidget(self.ConnectButton)

		self.HeadBox.setLayout(self.HeadLayout)

		self.mainLayout.addWidget(self.HeadBox, 0, 0, self.GroupBoxSeg[0], 1)

	def destroyHeadLine(self):
		self.HeadBox.deleteLater()
		self.mainLayout.removeWidget(self.HeadBox)
	
	def createMain(self):
		self.MainBodyBox = QGroupBox()

		mainbodylayout = QHBoxLayout()

		#Group Box for history
		HistoryBox = QGroupBox("&Record")

		HistoryLayout = QGridLayout()
		dataList = getLocalRemoteTests(self.connection, self.info)

		self.proxy = QtTableWidget(dataList)

		self.lineEdit       = QLineEdit()
		self.lineEdit.textChanged.connect(self.proxy.on_lineEdit_textChanged)
		self.view           = QTableView()
		self.view.setSortingEnabled(True)
		self.comboBox       = QComboBox()
		self.comboBox.addItems(["{0}".format(x) for x in dataList[0]])
		self.comboBox.currentIndexChanged.connect(self.proxy.on_comboBox_currentIndexChanged)
		self.label          = QLabel()
		self.label.setText("Regex Filter")

		self.view.setModel(self.proxy)
		self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.view.setSelectionMode(QAbstractItemView.MultiSelection)
		self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)

		HistoryLayout = QGridLayout()
		HistoryLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
		HistoryLayout.addWidget(self.view, 1, 0, 1, 3)
		HistoryLayout.addWidget(self.comboBox, 0, 2, 1, 1)
		HistoryLayout.addWidget(self.label, 0, 0, 1, 1)

		HistoryBox.setLayout(HistoryLayout)

		mainbodylayout.addWidget(HistoryBox)

		self.MainBodyBox.setLayout(mainbodylayout)
		self.mainLayout.addWidget(self.MainBodyBox, sum(self.GroupBoxSeg[0:1]), 0, self.GroupBoxSeg[1], 1)

	def destroyMain(self):
		self.MainBodyBox.deleteLater()
		self.mainLayout.removeWidget(self.MainBodyBox)

	def createApp(self):
		self.AppOption = QGroupBox()
		self.StartLayout = QHBoxLayout()

		self.SyncButton = QPushButton("&Sync to DB")
		self.SyncButton.clicked.connect(self.syncDB)

		self.ResetButton = QPushButton("&Reset")
		self.ResetButton.clicked.connect(self.destroyMain)
		self.ResetButton.clicked.connect(self.createMain)

		self.FinishButton = QPushButton("&Finish")
		self.FinishButton.setDefault(True)
		self.FinishButton.clicked.connect(self.closeWindow)

		self.StartLayout.addStretch(1)
		self.StartLayout.addWidget(self.SyncButton)
		self.StartLayout.addWidget(self.ResetButton)
		self.StartLayout.addWidget(self.FinishButton)
		self.AppOption.setLayout(self.StartLayout)

		self.mainLayout.addWidget(self.AppOption, sum(self.GroupBoxSeg[0:2]), 0, self.GroupBoxSeg[2], 1)

	def destroyApp(self):
		self.AppOption.deleteLater()
		self.mainLayout.removeWidget(self.AppOption)

	def closeWindow(self):
		self.close()

	def sendBackSignal(self):
		self.backSignal = True

	def connectDB(self):
		pass

	def syncDB(self):
		selectedrows = self.view.selectionModel().selectedRows()
		for index in selectedrows:
			rowNumber = index.row()
			print(self.proxy.data(self.proxy.index(rowNumber, 3)))
