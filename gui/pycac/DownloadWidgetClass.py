from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .downloads import load_config, get_recent_projects
import os, copy, pdb

#This file contains all of the functions necessary for the input script handling

class DownloadWidget(QWidget):

    backButton = pyqtSignal()

    submitButton = pyqtSignal()

    def __init__(self):

        super(DownloadWidget, self).__init__()

        DownloadWidget.window(self)

    def window(self):

        scrollArea = QScrollArea()

        groupbox = QGroupBox()

        box_layout = QVBoxLayout()

        box_layout.setAlignment(Qt.AlignTop)

        sublayouts = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

        self.local_dir = ''

        self.errormsg = []

        self.cluster_widgets = [QLabel('Server'), QLineEdit(), QLabel('Username'), QLineEdit(), QLabel('Password'), QLineEdit(), QLabel('Local directory for download:'), QPushButton('Browse'), QLabel('No directory ' +
         'selected')]

        browse_width = self.cluster_widgets[-2].fontMetrics().boundingRect("Browse").width() + 50

        self.cluster_widgets[-2].setFixedWidth(browse_width)

        sublayouts[2].setAlignment(Qt.AlignLeft)

        self.cluster_widgets[7].clicked.connect(lambda: self.getlocalpath())

        self.loadConfig()

        self.cluster_widgets[5].setEchoMode(QLineEdit.Password)

        [self.cluster_widgets[i].setPlaceholderText([self.servername, self.username][int(i/2)]) for i in [1,3]]

        for indx,widget in enumerate(self.cluster_widgets):

            if indx < 2:

                sublayouts[0].addWidget(widget)

            elif indx > 5:

                sublayouts[2].addWidget(widget)

            else:

                sublayouts[1].addWidget(widget)

        [box_layout.addLayout(layout) for layout in sublayouts]

        self.boxNameList = []

        self.downloadFileLayout = QVBoxLayout()

        box_layout.addLayout(self.downloadFileLayout)

        self.add_file_widget = [QLabel("Number of projects for download:"), QLabel('0'), QPushButton('+'), QPushButton('-')] 

        self.fileWidgets = []

        self.fileLayouts = []

        self.rowLayout = []

        self.convertWidgets = []

        self.convertLayouts = []

        self.selectedNames = []

        self.boolConvert = []

        self.fileNum = 0

        self.add_file_widget[2].clicked.connect(lambda: self.addFileRow())

        self.add_file_widget[3].clicked.connect(lambda: self.removeFileRow())

        fileButtonLayout = QHBoxLayout()

        [fileButtonLayout.addWidget(widget) for widget in self.add_file_widget]

        self.downloadFileLayout.addLayout(fileButtonLayout)

        self.addFileRow()

        directionButtons = [QPushButton('Back'), QPushButton('Submit')]

        directionButtons[0].clicked.connect(lambda: self.back())

        directionButtons[1].clicked.connect(lambda: self.submit())

        buttonLayout = QHBoxLayout()

        [buttonLayout.addWidget(button) for button in directionButtons]

        box_layout.addLayout(buttonLayout)

        groupbox.setLayout(box_layout)
    
        scrollArea.setWidget(groupbox)

        scrollArea.setWidgetResizable(True)

        finalLayout = QVBoxLayout()

        finalLayout.addWidget(scrollArea)

        self.setLayout(finalLayout)

    def addFileRow(self):

        self.rowLayout.append(QVBoxLayout())

        self.fileLayouts.append(QHBoxLayout())

        self.convertLayouts.append([QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()])

        [self.convertLayouts[self.fileNum][i].setAlignment(Qt.AlignLeft) for i in [1,2,3]]

        self.convertWidgets.append([])

        self.boolConvert.append(False)

        self.fileWidgets.append([QLabel("Project Name:"), QComboBox() , QCheckBox('Convert .vtk to dump file'), QLineEdit()])

        self.boxNameList.append(self.projectNames)

        self.popList(0)

        currentWidgets = self.fileWidgets[self.fileNum]

        currentWidgets[2].setObjectName(str(self.fileNum))

        currentWidgets[2].toggled.connect(lambda: self.convertOptions(1))

        currentWidgets[1].setObjectName(str(self.fileNum))

        currentWidgets[1].activated.connect(lambda: self.popList(1))

        currentWidgets[3].setPlaceholderText('Path to file on cluster if other')

        [self.fileLayouts[self.fileNum].addWidget(widget) for widget in currentWidgets]

        [self.rowLayout[self.fileNum].addLayout(layout) for layout in [self.fileLayouts[self.fileNum], *self.convertLayouts[self.fileNum]]]

        self.downloadFileLayout.addLayout(self.rowLayout[self.fileNum])

        self.fileNum += 1

        self.add_file_widget[1].setText(str(self.fileNum))

    def removeFileRow(self):

        if self.fileNum > 0:

            self.fileNum -= 1

            while self.fileLayouts[self.fileNum].count() > 0:

                item = self.fileLayouts[self.fileNum].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            [self.rowLayout[self.fileNum].removeItem(layout) for layout in [self.fileLayouts[self.fileNum], self.rowLayout[self.fileNum]]]

            self.downloadFileLayout.removeItem(self.rowLayout[self.fileNum])

            del self.fileLayouts[self.fileNum]

            del self.fileWidgets[self.fileNum]

            self.convertOptions(0)

            self.add_file_widget[1].setText(str(self.fileNum))

            if self.fileNum < len(self.projectNames):

                del self.selectedNames[self.fileNum]

            self.popList(2)

    def popList(self, butsend):

        if butsend == 1:

            box = self.sender()

            numBox = int(box.objectName())

            self.selectedNames[numBox] = box.currentText()
       
            if box.currentText() == 'Other':

                self.fileWidgets[numBox][3].setEnabled(True)

                return

            else:

                self.fileWidgets[numBox][3].setEnabled(False)

        else:

            numBox = self.fileNum

            if butsend == 0:

                if numBox < len(self.projectNames):

                    self.selectedNames.append([name for name in self.projectNames if name not in self.selectedNames][0]) 

                    self.fileWidgets[numBox][3].setEnabled(False)

                else:

                    self.selectedNames.append('Other')

                    self.fileWidgets[numBox][3].setEnabled(True)

        for index,widgetList in enumerate(self.fileWidgets):

            box_options = []

            for name in self.projectNames:

                temp_exclude_list = [name for i,name in enumerate(self.selectedNames) if i != index]

                if name not in temp_exclude_list:
                
                    box_options.append(name)

            widgetList[1].clear()

            widgetList[1].addItems(box_options)

            widgetList[1].addItem('Other')

            if index < len(self.selectedNames):

                if self.selectedNames[index] in box_options:

                    widgetList[1].setCurrentIndex(box_options.index(self.selectedNames[index]))

                else:

                    widgetList[1].setCurrentIndex(len(box_options))

    def loadConfig(self):

        error, dictionary = get_recent_projects(5)

        self.projectNames = []

        self.projectDirectories = []

        if not error:

            for key,directories in dictionary.items():

                projectName = directories[1].split('/')[-1]

                self.projectNames.append(projectName)

                self.projectDirectories.append(directories[1])

        error,config = load_config()

        self.username = config['install']['user']

        self.servername = config['install']['server']

    def getlocalpath(self):

        self.local_dir = QFileDialog.getExistingDirectory(self, 'Directory', os.getcwd())

        if self.local_dir != '':

            self.cluster_widgets[-1].setText(self.local_dir)

        else:

            self.cluster_widgets[-1].setText('No directory selected')

    def convertOptions(self, butsend):

        button = self.sender()

        if butsend:

            num = int(button.objectName())

            if button.isChecked():

                self.convertWidgets[num].extend([QCheckBox('Convert Coarse Grained'), QCheckBox('Convert Atomistic'), QLabel('x'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), QLineEdit(), QLineEdit(), 
                                                 QLabel('y'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), QLineEdit(), QLineEdit(), QLabel('z'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), 
                                                 QLineEdit(), QLineEdit()])

                [self.convertLayouts[num][0].addWidget(self.convertWidgets[num][i]) for i in [0,1]]

                [self.convertLayouts[num][int(i/5)+1].addWidget(widget) for i,widget in enumerate(self.convertWidgets[num][2:])]

                for i,j in enumerate([4, 9, 14]):

                    self.convertWidgets[num][j].setObjectName(str(num) +' ' + str(i*2))

                    self.convertWidgets[num][j].toggled.connect(lambda: self.customBounds())

                dirs = ['x','y','z']

                for i,j in enumerate([5,6,10,11,15,16]):

                    self.convertWidgets[num][j].setEnabled(False)

                    if not i%2:

                        self.convertWidgets[num][j].setPlaceholderText('Lower bound for '+dirs[int(i/2)] + ' direction')

                    else:

                        self.convertWidgets[num][j].setPlaceholderText('Upper bound for '+dirs[int(i/2)] + ' direction')

                self.boolConvert[num] = True

                return

        else:

            num = self.fileNum

        for layout in self.convertLayouts[num]:

            while layout.count() > 0:

                item = layout.takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            del layout

        if not butsend:

            del self.convertWidgets[num]

            del self.convertLayouts[num]

            self.boolConvert[num] = False
            
        else:

            for i in range(0,len(self.convertWidgets[num])):

                del self.convertWidgets[num][0]


    def customBounds(self):

        button = self.sender()

        num = int(button.objectName().split()[0])

        direction = int(button.objectName().split()[1])

        lineEditIndex = [5,6,10,11,15,16]

        if button.isChecked():

            [self.convertWidgets[num][i].setEnabled(True) for j,i in enumerate(lineEditIndex) if j in [direction + k for k in [0, 1]]]

        else:

            [self.convertWidgets[num][i].setEnabled(False) for j,i in enumerate(lineEditIndex) if j in [direction + k for k in [0, 1]]]

        
    def submit(self):

        self.errormsg = []

        #Pull server info

        self.server = str(self.cluster_widgets[1].text())

        if not self.server:

            self.server = self.servername

        self.user = str(self.cluster_widgets[3].text())

        if not self.user:

            self.user = self.username

        self.password = str(self.cluster_widgets[5].text())

        if not self.local_dir:

            self.errormsg.append(('local_dir', 'Missing local directory for download'))

            self.local_dir = ''

        self.projectDirs = []

        project_names = []

        for widgetList in self.fileWidgets:

            option = str(widgetList[1].currentText())

            if option != 'Other':

                project_names.append(option)

                self.projectDirs.append(self.projectDirectories[self.projectNames.index(option)])

            else:

                self.projectDirs.append(str(widgetList[3].text()))

                project_names.append(str(widgetList[3]).split('/')[-1])

        self.convertProjectDirs = []

        self.convertProjectParams = []

        self.convertNum = 0

        for index,convertTrue in enumerate(self.boolConvert):

            if convertTrue:

                self.convertProjectDirs.append(self.local_dir + '/' + project_names[index])

                widgets = self.convertWidgets[index]

                bool_cg = widgets[0].isChecked()

                bool_at = widgets[1].isChecked()

                if widgets[3].isChecked():

                    bound_x = 'p'

                else:

                    bound_x = 's'

                if widgets[4].isChecked():

                    custom_x = 't'

                    lower_x = str(widgets[5].text())

                    upper_x = str(widgets[6].text())

                else:

                    custom_x = 'f'

                    lower_x = '0'

                    upper_x = '0'

                if widgets[8].isChecked():

                    bound_y = 'p'

                else:

                    bound_y = 's'

                if widgets[9].isChecked():

                    custom_y = 't'

                    lower_y = str(widgets[9].text())

                    upper_y = str(widgets[10].text())

                else:

                    custom_y = 'f'

                    lower_y = '0'

                    upper_y = '0'

                if widgets[13].isChecked():

                    bound_z = 's'

                else:

                    bound_z = 'p'

                if widgets[14].isChecked():

                    custom_z = 't'

                    lower_z = str(widgets[15].text())

                    upper_z = str(widgets[16].text())

                else:

                    custom_z = 'f'

                    lower_z = '0'

                    upper_z = '0'

                file = self.convertProjectDirs[self.convertNum]

                self.convertProjectParams.append([bool_cg, bool_at, bound_x, custom_x, self.checkinf(lower_x, ('lower_x', ('lower bound in x',file))), self.checkinf(upper_x,('upper_x', ('upper bound in x',file))),  
                                                  bound_y, custom_y, self.checkinf(lower_y,('lower_y',('lower bound in y',file))), self.checkinf(upper_y,('upper_y',('upper bound in y',file))), 
                                                  bound_z, custom_z, self.checkinf(lower_z,('lower_z',('lower bound in z',file))), self.checkinf(upper_z,('upper_z',('upper bound in z',file)))]) 

                self.convertNum += 1

        self.submitButton.emit()

    def back(self):

        self.backButton.emit()

    def checkinf(self,val, designator):

        #Returns either a string with inf or a number or an error message

        try:

            if val.strip() == "inf" or val.strip() == "Inf" or val.strip() == "INF":

                out = "inf"

            else:

                out = float(val)

            return out

        except ValueError:

            self.errormsg.append((designator[0], 'Incorrect format for ' + designator[1][0] + ' in file ' + designator[1][1]))

            out = 0            


    def refreshFields(self):

        [widget.setText('') for widget in self.cluster_widgets if isinstance(widget, QLineEdit)]

        while self.fileNum > 0:

            self.removeFileRow()

        self.loadConfig()

        self.addFileRow()

        self.cluster_widgets[-1].setText('No directory selected')

        self.local_dir = ''