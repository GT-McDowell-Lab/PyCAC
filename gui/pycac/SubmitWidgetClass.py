import pdb

from fnmatch import fnmatch

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .InputWidgetClass import InputWidget

import json, sys, os

class SubmitWidget(QWidget):

    submitsignal = pyqtSignal()

    backsignal = pyqtSignal()

    def __init__(self):

        super(SubmitWidget,self).__init__()

        self.window()

    def window(self):


        self.validateposdouble = QDoubleValidator()

        self.validateposdouble.setRange(0, 100000, 15)

        self.validateposint = QIntValidator(0,10000)

        self.validatedouble = QDoubleValidator()

        vlay = QVBoxLayout()

        scrollArea = QScrollArea()

        groupbox = QGroupBox()

        self.pullConfig()
   
        self.layout_list = []

        rowcount = 0

        self.layout_list.append(QHBoxLayout())

        labelone = QLabel('Queue Name:  ')

        labeltwo = QLabel('Server Directory:  ')

        width = [labelone.fontMetrics().boundingRect('Queue Name:  ').width(), labeltwo.fontMetrics().boundingRect('Server Directory:  ').width()]

        self.cluster_widgets = [QLabel("Nodes:"), QLineEdit(), QLabel("Processors per Node:"), QLineEdit(), QLabel('Walltime:'), QLineEdit(), 
                                QLabel('Queue Name:'), QLineEdit(), QLabel('Job Name:'), QLineEdit()]

        [widget.setFixedWidth(width[bool(i)]) for i,widget in enumerate(self.cluster_widgets[6:]) if isinstance(widget, QLabel)]

        [widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter) for i,widget in enumerate(self.cluster_widgets) if isinstance(widget, QLabel) and i > 5]

        self.cluster_widgets[1].setValidator(self.validateposint)

        self.cluster_widgets[3].setValidator(self.validateposint)

        walltimeValidator = QRegExpValidator()

        walltimeValidator.setRegExp(QRegExp(r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]'))

        self.cluster_widgets[5].setValidator(walltimeValidator)

        self.cluster_widgets[5].setPlaceholderText('Must be in HH:MM:SS format')

        self.cluster_widgets[9].setPlaceholderText('Default name is \'batching\'')

        for widget in self.cluster_widgets[0:6]:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        self.layout_list.append(QHBoxLayout())

        self.layout_list[rowcount].setAlignment(Qt.AlignLeft)

        for widget in self.cluster_widgets[6:]:
            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        self.layout_list.append(QHBoxLayout())

        self.submitWidgets = [QLabel('Server:'), QLineEdit(), QLabel('Server Directory:'), QLineEdit(), QLabel('Username:'), QLineEdit(), 
                              QLabel('Password:'), QLineEdit()]

        [widget.setFixedWidth(width[bool(i%4)]) for i,widget in enumerate(self.submitWidgets) if isinstance(widget, QLabel)]

        [widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter) for i,widget in enumerate(self.submitWidgets) if isinstance(widget, QLabel)]

        self.submitWidgets[1].setPlaceholderText(self.server)

        self.submitWidgets[3].setPlaceholderText("Leave empty for home directory")

        self.submitWidgets[5].setPlaceholderText(self.username)

        self.submitWidgets[7].setEchoMode(QLineEdit.Password)

        for widget in self.submitWidgets[0:4]:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        self.layout_list.append(QHBoxLayout())

        for widget in self.submitWidgets[4:]:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        [layout.setAlignment(Qt.AlignRight) for layout in self.layout_list]

    #   Add final buttons

        self.layout_list.append(QHBoxLayout())

        submitWidgets = [QPushButton('Back'), QPushButton("Submit to Cluster")]

        submitWidgets[0].clicked.connect(lambda: self.back())

        submitWidgets[1].clicked.connect(lambda: self.submit())

        for widget in submitWidgets:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        #Final setup

        vlay.setAlignment(Qt.AlignTop)

        groupbox.setLayout(vlay)
     
        scrollArea.setWidget(groupbox)
     
        scrollArea.setWidgetResizable(True)
     
        layout = QVBoxLayout()

        layout.addWidget(scrollArea)

        self.setLayout(layout)       

    def submit(self):

        self.errorvals = []

               #Pull Cluster data

        if self.cluster_widgets[1].text() == '':

            self.nodes = 0

        else:

            self.nodes = int(self.cluster_widgets[1].text())

        if self.cluster_widgets[3].text() == '':

            self.ppn = 0

        else: 

            self.ppn = int(self.cluster_widgets[3].text())

        if self.cluster_widgets[5].text() == '':

            self.walltime = 0

        else: 

            self.walltime = self.cluster_widgets[5].text()

            placeholder = self.walltime.split(':')

            self.walltime = ''

            for index,string in enumerate(placeholder):

                if len(string) < 2:

                    string = '0' + string  

                if index == len(placeholder)-1:

                    self.walltime += string

                else:

                    self.walltime += string + ':'

        #Pull submission data 

        self.host = str(self.submitWidgets[1].text())

        self.hostdir = self.submitWidgets[3].text()

        if self.host == '':

            self.host = self.server

        self.qname  = str(self.cluster_widgets[7].text())

        if self.qname == '':

            self.errorvals.append(('qname', 'Missing queue name in input field'))

        self.jobname = str(self.cluster_widgets[9].text())

        if self.jobname =='':

            self.jobname = 'batching'

        self.user = str(self.submitWidgets[5].text())

        if self.user == '':

            self.user = self.username

        self.password = str(self.submitWidgets[7].text())

        self.submitsignal.emit()

    def convert(self, num):

        try: 

            return int(num)

        except ValueError:

            return float(num)

    def pullConfig(self):

        pwd = os.getcwd()

        try:

            with open(os.path.realpath(pwd + '/config.json'), 'r') as infile:
                
                config = json.load(infile)

                self.username = config['install']['user']

                self.server = config['install']['server']

        except FileNotFoundError:

            errormsg = QMessageBox()

            errormsg.setText("Config file was not found on the current path. Please run Setup to initialize CAC, or create a config file named 'config.json' from 'config.template'."+
                             " If a config file is not created, you cannot submit jobs to cluster.")

            errormsg.setWindowTitle("Config file not found")

            errormsg.exec_()

            self.server = ''

            self.username = ''

            self.configio = 0

    def back(self):

        self.backsignal.emit()

    def refreshFields(self):

        [widget.setText('') for widget in self.cluster_widgets if isinstance(widget, QLineEdit)]

        [widget.setText('') for widget in self.submitWidgets if isinstance(widget, QLineEdit)]

