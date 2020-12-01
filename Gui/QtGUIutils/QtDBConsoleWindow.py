from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenuBar,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QStyleFactory, QTableView, QTableWidget, QTabWidget, QTextEdit, QHBoxLayout,
		QVBoxLayout, QWidget, QMainWindow, QMessageBox, QSplitter)

import sys
import os
import subprocess
from subprocess import Popen, PIPE

from Gui.GUIutils.DBConnection import *
from Gui.GUIutils.guiUtils import *
from Gui.QtGUIutils.QtDBTableWidget import *

class QtDBConsoleWindow(QMainWindow):
	def __init__(self,master):
		super(QtDBConsoleWindow,self).__init__()
		self.master = master
		self.connection = self.master.connection
		self.GroupBoxSeg = [1,10,1]
		self.processing = []
		#Fixme: QTimer to be added to update the page automatically

		self.mainWidget = QWidget()
		self.mainLayout = QGridLayout()
		self.mainWidget.setLayout(self.mainLayout)
		self.setCentralWidget(self.mainWidget)

		self.occupied()
		self.setLoginUI()
		self.createHeadLine()
		self.createMain()
		self.createApp()

	def setLoginUI(self):
		self.setGeometry(200, 200, 600, 1200)  
		self.setWindowTitle('Database Console') 

		self.menubar =self.menuBar()
		self.menubar.setNativeMenuBar(False)
		self.actionConsole = self.menubar.addMenu("&Database")

		###################################################
		##  User Menu
		###################################################
		self.actionUser = self.menubar.addMenu("&User")

		self.ShowUserAction = QAction("&Show Users",self)
		self.ShowUserAction.triggered.connect(self.displayUsers)
		self.actionUser.addAction(self.ShowUserAction)

		self.AddUserAction = QAction("&Add Users",self)
		self.AddUserAction.triggered.connect(self.addUsers)
		self.actionUser.addAction(self.AddUserAction)

		self.UpdateUserAction = QAction("&Update Profile",self)
		self.UpdateUserAction.triggered.connect(self.updateProfile)
		self.actionUser.addAction(self.UpdateUserAction)

		self.ShowInstAction = QAction("&Show institute",self)
		self.ShowInstAction.triggered.connect(self.displayInstitue)
		self.actionUser.addAction(self.ShowInstAction)

		self.show()

	def activateMenuBar(self):
		self.menubar.setDisabled(False)

	def deactivateMenuBar(self):
		self.menubar.setDisabled(True)

	def enableMenuItem(self,item, enabled):
		item.setEnabled(enabled)

	def createHeadLine(self):
		self.deactivateMenuBar()
		self.HeadBox = QGroupBox()

		self.HeadLayout = QHBoxLayout()

		UsernameLabel = QLabel("Username:")
		self.UsernameEdit = QLineEdit('')
		self.UsernameEdit.setEchoMode(QLineEdit.Normal)
		self.UsernameEdit.setPlaceholderText('Your username')
		self.UsernameEdit.setMinimumWidth(150)
		self.UsernameEdit.setMaximumHeight(20)

		PasswordLabel = QLabel("Password:")
		self.PasswordEdit = QLineEdit('')
		self.PasswordEdit.setEchoMode(QLineEdit.Password)
		self.PasswordEdit.setPlaceholderText('Your password')
		self.PasswordEdit.setMinimumWidth(150)
		self.PasswordEdit.setMaximumHeight(20)

		HostLabel = QLabel("HostName:")
		self.HostName = QComboBox()
		self.HostName.addItems(DBServerIP.keys())
		self.HostName.currentIndexChanged.connect(self.changeDBList)
		HostLabel.setBuddy(self.HostName)

		DatabaseLabel = QLabel("Database:")
		self.DatabaseCombo = QComboBox()
		self.DBNames = DBNames['All']
		self.DatabaseCombo.addItems(self.DBNames)
		self.DatabaseCombo.setCurrentIndex(0)
		
		self.ConnectButton = QPushButton("&Connect to DB")
		self.ConnectButton.clicked.connect(self.connectDB)

		self.HeadLayout.addWidget(UsernameLabel)
		self.HeadLayout.addWidget(self.UsernameEdit)
		self.HeadLayout.addWidget(PasswordLabel)
		self.HeadLayout.addWidget(self.PasswordEdit)
		self.HeadLayout.addWidget(HostLabel)
		self.HeadLayout.addWidget(self.HostName)
		self.HeadLayout.addWidget(DatabaseLabel)
		self.HeadLayout.addWidget(self.DatabaseCombo)
		self.HeadLayout.addWidget(self.ConnectButton)

		self.HeadBox.setLayout(self.HeadLayout)

		self.mainLayout.addWidget(self.HeadBox, 0, 0, self.GroupBoxSeg[0], 1)

	def destroyHeadLine(self):
		self.HeadBox.deleteLater()
		self.mainLayout.removeWidget(self.HeadBox)

	def connectedHeadLine(self):
		self.activateMenuBar()
		self.HeadBox.deleteLater()
		self.mainLayout.removeWidget(self.HeadBox)

		self.HeadBox = QGroupBox()
		self.HeadLayout = QHBoxLayout()

		WelcomeLabel = QLabel("Hello,{}!".format(self.TryUsername))

		statusString, colorString = checkDBConnection(self.connection)		
		DBStatusLabel = QLabel()
		DBStatusLabel.setText("Database:{}/{}".format(str(self.HostName.currentText()),str(self.DatabaseCombo.currentText())))
		DBStatusValue = QLabel()
		DBStatusValue.setText(statusString)
		DBStatusValue.setStyleSheet(colorString)

		self.SwitchButton = QPushButton("&Switch DB")
		self.SwitchButton.clicked.connect(self.destroyHeadLine)
		self.SwitchButton.clicked.connect(self.createHeadLine)

		self.HeadLayout.addWidget(WelcomeLabel)
		self.HeadLayout.addStretch(1)
		self.HeadLayout.addWidget(DBStatusLabel)
		self.HeadLayout.addWidget(DBStatusValue)
		self.HeadLayout.addWidget(self.SwitchButton)

		self.HeadBox.setLayout(self.HeadLayout)

		self.HeadBox.setLayout(self.HeadLayout)
		self.mainLayout.addWidget(self.HeadBox, 0, 0, self.GroupBoxSeg[0], 1)

	def displayUsers(self):
		self.processing.append("UserDisplay")
		UserDisplayTab = QWidget()
		
		# Add tabs
		self.MainTabs.addTab(UserDisplayTab,"User List")

		UserDisplayTab.layout = QGridLayout()

		dataList = ([describeTable(self.connection, "people")]+retrieveGenericTable(self.connection,"people"))

		proxy = QtDBTableWidget(dataList,1)

		lineEdit       = QLineEdit()
		lineEdit.textChanged.connect(proxy.on_lineEdit_textChanged)
		view           = QTableView()
		view.setSortingEnabled(True)
		comboBox       = QComboBox()
		comboBox.addItems(["{0}".format(x) for x in dataList[0]])
		comboBox.currentIndexChanged.connect(proxy.on_comboBox_currentIndexChanged)
		label          = QLabel()
		label.setText("Regex Filter")

		view.setModel(proxy)
		view.setSelectionBehavior(QAbstractItemView.SelectRows)
		view.setSelectionMode(QAbstractItemView.MultiSelection)
		view.setEditTriggers(QAbstractItemView.NoEditTriggers)

		UserDisplayTab.layout.addWidget(lineEdit, 0, 1, 1, 1)
		UserDisplayTab.layout.addWidget(view, 1, 0, 1, 3)
		UserDisplayTab.layout.addWidget(comboBox, 0, 2, 1, 1)
		UserDisplayTab.layout.addWidget(label, 0, 0, 1, 1)

		UserDisplayTab.setLayout(UserDisplayTab.layout)

	##########################################################################
	##  Functions for Managing Users
	##########################################################################

	def addUsers(self):
		## Fixme: disable the menu when tab exists, relieaze the menu when closed.
		self.processing.append("AddUser")
		AddingUserTab = QWidget()
		
		# Add tabs
		self.MainTabs.addTab(AddingUserTab,"Adding User")
		AddingUserTab.layout = QGridLayout(self)
		AddUserLabel = QLabel('<font size="12"> Creating new user: </font>')
		AddUserLabel.setMaximumHeight(60)

		self.AUNewUsernameLabel = QLabel('username')
		self.AUNewUsernameEdit = QLineEdit('')
		self.AUNewUsernameEdit.setEchoMode(QLineEdit.Normal)
		self.AUNewUsernameEdit.setPlaceholderText('new username')

		self.AUPasswordLabel = QLabel('password')
		self.AUPasswordEdit = QLineEdit('')
		self.AUPasswordEdit.setEchoMode(QLineEdit.Password)
		self.AUPasswordEdit.setPlaceholderText('new password')

		self.AURePasswordLabel = QLabel('re-password')
		self.AURePasswordEdit = QLineEdit('')
		self.AURePasswordEdit.setEchoMode(QLineEdit.Password)
		self.AURePasswordEdit.setPlaceholderText('verify password')

		self.AUNameLabel = QLabel('*name')
		self.AUNameEdit = QLineEdit('')
		self.AUNameEdit.setEchoMode(QLineEdit.Normal)
		self.AUNameEdit.setPlaceholderText('short name')

		self.AUFullNameLabel = QLabel('*full name')
		self.AUFullNameEdit = QLineEdit('')
		self.AUFullNameEdit.setEchoMode(QLineEdit.Normal)
		self.AUFullNameEdit.setPlaceholderText('full name')

		self.AUEmailLabel = QLabel('e-mail')
		self.AUEmailEdit = QLineEdit('')
		self.AUEmailEdit.setEchoMode(QLineEdit.Normal)
		self.AUEmailEdit.setPlaceholderText('your_email@host.name')

		self.AUInstLabel = QLabel('institute')
		self.AUInstComboBox       = QComboBox()
		siteList = getByColumnName("description",describeInstitute(self.connection),retrieveAllInstitute(self.connection))
		self.AUInstComboBox.addItems(["{0}".format(x) for x in siteList])

		self.AUFeedBackLabel = QLabel()

		self.AUSubmitButton = QPushButton('Submit')
		self.AUSubmitButton.clicked.connect(self.submitAURequest)

		AddingUserTab.layout.addWidget(AddUserLabel,0,0,1,4)
		AddingUserTab.layout.addWidget(self.AUNewUsernameLabel,1,0,1,1)
		AddingUserTab.layout.addWidget(self.AUNewUsernameEdit,1,1,1,1)
		AddingUserTab.layout.addWidget(self.AUPasswordLabel,2,0,1,1)
		AddingUserTab.layout.addWidget(self.AUPasswordEdit,2,1,1,1)
		AddingUserTab.layout.addWidget(self.AURePasswordLabel,3,0,1,1)
		AddingUserTab.layout.addWidget(self.AURePasswordEdit,3,1,1,1)
		AddingUserTab.layout.addWidget(self.AUNameLabel,4,0,1,1)
		AddingUserTab.layout.addWidget(self.AUNameEdit,4,1,1,1)
		AddingUserTab.layout.addWidget(self.AUFullNameLabel,4,2,1,1)
		AddingUserTab.layout.addWidget(self.AUFullNameEdit,4,3,1,1)
		AddingUserTab.layout.addWidget(self.AUEmailLabel,5,0,1,1)
		AddingUserTab.layout.addWidget(self.AUEmailEdit,5,1,1,1)
		AddingUserTab.layout.addWidget(self.AUInstLabel,5,2,1,1)
		AddingUserTab.layout.addWidget(self.AUInstComboBox,5,3,1,1)
		AddingUserTab.layout.addWidget(self.AUFeedBackLabel,6,0,1,3)
		AddingUserTab.layout.addWidget(self.AUSubmitButton,6,3,1,1)

		AddingUserTab.setLayout(AddingUserTab.layout)

		#self.enableMenuItem(self.AddingUserTab, False)
	
	def submitAURequest(self):
		# check the password consistency
		if self.AUNewUsernameEdit.text() == "" or self.AUNameEdit.text() == "" or self.AUFullNameEdit.text() ==  "":
			self.AUFeedBackLabel.setText("key blank is empty")
			return
		if self.AUPasswordEdit.text() != self.AURePasswordEdit.text():
			self.AUFeedBackLabel.setText("passwords are inconsistent")
			self.AUPasswordEdit.setText("")
			self.AURePasswordEdit.setText("")
			return

		try:
			InstituteInfo = retrieveWithConstraint(self.connection, "institute", description = str(self.AUInstComboBox.currentText()))
			InstName = getByColumnName("institute",describeTable(self.connection,"institute"),InstituteInfo)
			TimeZone = getByColumnName("timezone",describeTable(self.connection,"institute"),InstituteInfo)
		except:
			self.AUFeedBackLabel.setText("Failed to extract institute info, try to reconnect to DB")
		Args =  describeTable(self.connection, "people")
		Data = []
		Data.append(self.AUNewUsernameEdit.text())
		Data.append(self.AUNameEdit.text())
		Data.append(self.AUFullNameEdit.text())
		Data.append(self.AUEmailEdit.text())
		Data.append(InstName[0])
		Data.append(self.AUPasswordEdit.text())
		Data.append(TimeZone[0])
		Data.append(0)
		print(Data)
		try:
			createNewUser(self.connection, Args, Data)
			self.AUFeedBackLabel.setText("Query submitted")
			self.AUFeedBackLabel.setStyleSheet("color:green")
			return 
		except:
			print("submitFailed")
			return


	def updateProfile(self):
		pass

	##########################################################################
	##  Functions for Adding Users (END)
	##########################################################################
	
	##########################################################################
	##  Functions for Institutes display
	##########################################################################
	def displayInstitue(self):
		self.processing.append("InstituteDisplay")

		displayInstiTab = QWidget()
		
		# Add tabs
		self.MainTabs.addTab(displayInstiTab,"Institutes")

		displayInstiTab.layout = QGridLayout(self)

		dataList = ([describeInstitute(self.connection)]+retrieveAllInstitute(self.connection))

		proxy = QtDBTableWidget(dataList,1)

		lineEdit       = QLineEdit()
		lineEdit.textChanged.connect(proxy.on_lineEdit_textChanged)
		view           = QTableView()
		view.setSortingEnabled(True)
		comboBox       = QComboBox()
		comboBox.addItems(["{0}".format(x) for x in dataList[0]])
		comboBox.currentIndexChanged.connect(proxy.on_comboBox_currentIndexChanged)
		label          = QLabel()
		label.setText("Regex Filter")

		view.setModel(proxy)
		view.setSelectionBehavior(QAbstractItemView.SelectRows)
		view.setSelectionMode(QAbstractItemView.MultiSelection)
		view.setEditTriggers(QAbstractItemView.NoEditTriggers)

		displayInstiTab.layout.addWidget(lineEdit, 0, 1, 1, 1)
		displayInstiTab.layout.addWidget(view, 1, 0, 1, 3)
		displayInstiTab.layout.addWidget(comboBox, 0, 2, 1, 1)
		displayInstiTab.layout.addWidget(label, 0, 0, 1, 1)

		displayInstiTab.setLayout(displayInstiTab.layout)

	##########################################################################
	##  Functions for Institutes display (END)
	##########################################################################

	def createMain(self):
		self.MainBodyBox = QGroupBox()

		self.mainbodylayout = QHBoxLayout()

		self.MainTabs = QTabWidget()
		self.MainTabs.setTabsClosable(True)
		self.MainTabs.tabCloseRequested.connect(lambda index: self.closeTab(index))
		
		self.mainbodylayout.addWidget(self.MainTabs)

		self.MainBodyBox.setLayout(self.mainbodylayout)
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

	def sendBackSignal(self):
		self.backSignal = True

	def connectDB(self):
		self.TryUsername = self.UsernameEdit.text()
		self.TryPassword = self.PasswordEdit.text()
		self.TryHostAddress = DBServerIP[str(self.HostName.currentText())]
		self.TryDatabase = str(self.DatabaseCombo.currentText())

		if self.TryUsername == '':
			msg.information(None,"Error","Please enter a valid username", QMessageBox.Ok)
			return

		self.connection = QtStartConnection(self.TryUsername, self.TryPassword, self.TryHostAddress, self.TryDatabase)

		if self.connection:
			self.connectedHeadLine()

	def syncDB(self):
		selectedrows = self.view.selectionModel().selectedRows()
		for index in selectedrows:
			rowNumber = index.row()
			print(self.proxy.data(self.proxy.index(rowNumber, 3)))

	def changeDBList(self):
		self.DBNames = DBNames[str(self.HostName.currentText())]
		self.DatabaseCombo.clear()
		self.DatabaseCombo.addItems(self.DBNames)
		self.DatabaseCombo.setCurrentIndex(0)

	def closeTab(self, index):
		self.MainTabs.removeTab(index)

	def closeWindow(self):
		self.release()
		self.close()

	def occupied(self):
		self.master.DBConsoleButton.setDisabled(True)

	def release(self):
		self.master.DBConsoleButton.setDisabled(False)
