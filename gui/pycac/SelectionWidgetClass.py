from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

# This widget class lets you select what you want to do

class SelectionWidget(QWidget):

    submitSignal = pyqtSignal()

    def __init__(self):

        super(SelectionWidget, self).__init__()

        SelectionWidget.window(self)

    def window(self):

        self.uploadDir = ''

        box_layout = QVBoxLayout()

        textField = QPlainTextEdit()

        textField.setReadOnly(True)

        textField.setPlainText("Copyright (c) 2017-2018 Georgia Institute of Technology. All Rights Reserved.\n\n" + 
                               "PyCAC, the concurrent atomistic-continuum (CAC) simulation environment, is a software suite that allows users to run CAC simulations and analyze data. " +
                               "For more information and for documentation please visit www.pycac.org.\n\n" +
                               "The PyCAC code development was sponsored by \n" +
                               "National Science Foundation \n" +
                               "\tGeorgia Institute of Technology, CMMI-1232878 \n" +
                               "\tUniversity of Florida, CMMI-1233113 \n" +
                               "\tIowa State University, CMMI-1536925 \n" +
                               "Department of Energy, Office of Basic Energy Sciences \n" +
                               "\tUniversity of Florida, DE-SC0006539 \n" +
                               " Institute for Materials, Georgia Institute of Technology \n\n" +
                               "If you use PyCAC results in your published work, please cite these papers: \n\n" +
                               "\tShuozhi Xu, Thomas G. Payne, Hao Chen, Yongchao Liu, Liming Xiong, Youping Chen, David L. McDowell. PyCAC: The concurrent atomistic-continuum simulation environment, J. Mater. Res. 33 (2018) 857-871 \n\n" +
                               "\tShuozhi Xu, Rui Che, Liming Xiong, Youping Chen, David L. McDowell. A quasistatic implementation of the concurrent atomistic-continuum method for FCC crystals, Int. J. Plast. 72 (2015) 91–126 \n\n" +
                               "\tLiming Xiong, Garritt Tucker, David L. McDowell, Youping Chen. Coarse-grained atomistic simulation of dislocations, J. Mech. Phys. Solids 59 (2011) 160-177 \n\n" +
                               "\tYouping Chen. Reformulation of microscopic balance equations for multiscale materials modeling, J. Chem. Phys. 130 (2009) 134706 \n\n" )

        
        box_layout.addWidget(textField)

        self.button_layout = [QHBoxLayout() for i in range(0,5)]

        self.button_layout[0].setAlignment(Qt.AlignLeft)

        self.button_layout[1].setAlignment(Qt.AlignLeft)

        self.button_layout[2].setAlignment(Qt.AlignLeft)

        radiobuttonStrings = ["Create Input File", "Edit Input File", 'Submit Job(s)', "Download Project Results", 'Convert directory to dump']

        self.buttonArray = [QRadioButton(text) for text in radiobuttonStrings]

        [button.setObjectName(str(i)) for i, button in enumerate(self.buttonArray)]

        self.buttonArray[0].toggled.connect(lambda: self.restartOptions())

        self.buttonArray[1].toggled.connect(lambda: self.submitOptions())

        self.buttonArray[2].toggled.connect(lambda: self.submitOptions())

        #Wrap all buttons in their own layouts. This is in case we want to add more widgets under them later

        for indx,button in enumerate(self.buttonArray):

            self.button_layout[indx].addWidget(button)

            box_layout.addLayout(self.button_layout[indx])

        submit = QPushButton('Next')

        submit.clicked.connect(lambda: self.submission())

        box_layout.addWidget(submit)

        self.setLayout(box_layout)

    def submission(self):

        self.option = [indx for indx,button in enumerate(self.buttonArray) if button.isChecked()][0]

        self.submitSignal.emit()

    def configIO(self, configio):

        if configio == 0:

            self.buttonArray[1].setEnabled(False)

    def restartOptions(self):

      button = self.sender()

      if button.isChecked():

        restart_button = QCheckBox('Use Restart File?')

        self.restartTF = False

        restart_button.toggled.connect(lambda: self.restartBox())

        self.button_layout[0].addWidget(restart_button)

      else:

        item = self.button_layout[0].takeAt(1)

        widget = item.widget()

        if widget is not None:

          widget.deleteLater()

    def restartBox(self):

      button = self.sender()

      if button.isChecked():

        self.restartTF = True

      else:

        self.restartTF = False

    def submitOptions(self):

        button = self.sender()

        num = int(button.objectName())

        if button.isChecked():

            submitJobWidgets = [QPushButton('Browse'), QLabel('No file selected')]

            submitJobWidgets[0].clicked.connect(lambda: self.getlocalpath(submitJobWidgets[1], num))

            [self.button_layout[num].addWidget(widget) for widget in submitJobWidgets]

        else:

            while self.button_layout[num].count() > 1:

                item = self.button_layout[num].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

    def getlocalpath(self, label, option):

          if option == 1:

            self.uploadDir, throwaway = QFileDialog.getOpenFileName(self, 'Save file', os.getcwd(), '*.in')

          elif option == 2:

            self.uploadDir = QFileDialog.getExistingDirectory(self, 'Directory', os.getcwd())

          if self.uploadDir != '':

              label.setText(self.uploadDir)

          else:

              label.setText('No file selected')




