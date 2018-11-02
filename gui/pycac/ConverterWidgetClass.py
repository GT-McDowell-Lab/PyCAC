from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from itertools import chain
import os, pdb

# This widget class lets you select what you want to do

class ConverterWidget(QWidget):

    submit_signal = pyqtSignal()

    back = pyqtSignal()

    def __init__(self):

        super(ConverterWidget, self).__init__()

        ConverterWidget.window(self)

    def window(self):

        self.box_layout = QVBoxLayout()

        self.box_layout.setAlignment(Qt.AlignTop)

        scrollArea = QScrollArea()

        groupbox = QGroupBox()

        textField = QPlainTextEdit()

        textField.setPlainText('Select files for conversion from .vtk to lammps format dump files.')

        textField.setMaximumHeight(40)

        self.box_layout.addWidget(textField)

        self.convertlayout = []

        self.convertsublayout = []

        self.convertwidget = []

        self.convertNum = 0

        self.box_convert_layout = QVBoxLayout()

        self.box_layout.addLayout(self.box_convert_layout)

        self.path = []

        self.button_widgets = [QLabel('Number of conversions:'), QLabel('0'), QPushButton('+'), QPushButton('-')]

        self.button_widgets[2].clicked.connect(lambda: self.convertFields(0))

        self.button_widgets[3].clicked.connect(lambda: self.convertFields(1))

        button_layout = QHBoxLayout()

        for widget in self.button_widgets:

            button_layout.addWidget(widget)

        self.box_convert_layout.addLayout(button_layout)

        self.convertFields(0)

        submit_buttons = [QPushButton('Back'), QPushButton('Submit')]

        submit_layout = QHBoxLayout()

        submit_buttons[0].clicked.connect(lambda: self.submit(0)) 

        submit_buttons[1].clicked.connect(lambda: self.submit(1))

        [submit_layout.addWidget(widget) for widget in submit_buttons]

        self.box_layout.addLayout(submit_layout)

        groupbox.setLayout(self.box_layout)

        scrollArea.setWidget(groupbox)

        scrollArea.setWidgetResizable(True)

        finalLayout = QVBoxLayout()

        finalLayout.addWidget(scrollArea)

        self.setLayout(finalLayout)

    def convertFields(self, deleteTrue):

        if not deleteTrue:

            self.convertwidget.append([[QPushButton('Browse'), QLabel('No File Selected')], [QCheckBox('Convert Coarse Grained'), QCheckBox('Convert Atomistic') ,
                                                 QLabel('x'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), QLineEdit(), QLineEdit(), 
                                                 QLabel('y'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), QLineEdit(), QLineEdit(), 
                                                 QLabel('z'), QCheckBox('Shrink-Wrapped'), QCheckBox('Custom Bounds'), QLineEdit(), QLineEdit()]])

            self.path.append('')

            self.convertwidget[self.convertNum][0][0].setObjectName(str(self.convertNum))

            self.convertwidget[self.convertNum][0][0].clicked.connect(lambda: self.getFilePaths())

            self.convertlayout.append(QVBoxLayout())

            self.convertlayout[self.convertNum].setAlignment(Qt.AlignTop)

            self.convertsublayout.append([QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()])

            self.convertsublayout[self.convertNum][0].setAlignment(Qt.AlignLeft)

            [self.convertsublayout[self.convertNum][0].addWidget(widget) for widget in self.convertwidget[self.convertNum][0]]

            [self.convertsublayout[self.convertNum][1].addWidget(widget) for i,widget in enumerate(self.convertwidget[self.convertNum][1]) if i in [0,1]]

            for i,j in enumerate([4, 9, 14]):

                self.convertwidget[self.convertNum][1][j].setObjectName(str(self.convertNum) +' ' + str(i*2))

                self.convertwidget[self.convertNum][1][j].toggled.connect(lambda: self.customBounds())

            dirs = ['x','y','z']

            for i,j in enumerate([5,6, 10, 11, 15, 16]):

                self.convertwidget[self.convertNum][1][j].setEnabled(False)

                if not i%2:

                    self.convertwidget[self.convertNum][1][j].setPlaceholderText('Lower bound for '+dirs[int(i/2)] + ' direction')

                else:

                    self.convertwidget[self.convertNum][1][j].setPlaceholderText('Upper bound for '+dirs[int(i/2)] + ' direction')

            [self.convertsublayout[self.convertNum][int(i/5) + 2].addWidget(widget) for i, widget in enumerate(self.convertwidget[self.convertNum][1][2:])]

            [self.convertlayout[self.convertNum].addLayout(layout) for layout in self.convertsublayout[self.convertNum]]

            self.box_convert_layout.addLayout(self.convertlayout[self.convertNum])

            self.convertNum += 1

        elif deleteTrue:

            if self.convertNum > 0:

                self.convertNum -= 1

                for layout in self.convertsublayout[self.convertNum]:

                    while layout.count() > 0:

                        item = layout.takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

                    self.convertlayout[self.convertNum].removeItem(layout)

                del self.convertsublayout[self.convertNum]

                self.box_layout.removeItem(self.convertlayout[self.convertNum])

                del self.convertlayout[self.convertNum]

                del self.convertwidget[self.convertNum] 

        self.button_widgets[1].setText(str(self.convertNum))

            
    def getFilePaths(self):

        button = self.sender()

        num = int(button.objectName())

        self.path[num] = QFileDialog.getExistingDirectory(self, 'Directory', os.getcwd())

        if self.path[num] != '':

            self.convertwidget[num][0][1].setText(self.path[num])

        else:

            self.convertwidget[num][0][1].setText('No file selected')

    def customBounds(self):

        button = self.sender()

        num = int(button.objectName().split()[0])

        direction = int(button.objectName().split()[1])

        lineEditIndex = [5,6,10,11,15,16]

        if button.isChecked():

            [self.convertwidget[num][1][i].setEnabled(True) for j,i in enumerate(lineEditIndex) if j in [direction + k for k in [0, 1]]]

        else:

            [self.convertwidget[num][1][i].setEnabled(False) for j,i in enumerate(lineEditIndex) if j in [direction + k for k in [0, 1]]]

    def submit(self, submitstat):

        self.convertProjectParams = []

        self.errormsg = []

        if submitstat:

            for i,widgetlist in enumerate(self.convertwidget):

                widgets = widgetlist[1]

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

                file = self.path[i]

                self.convertProjectParams.append([bool_cg, bool_at, bound_x, custom_x, self.checkinf(lower_x, ('lower_x', ('lower bound in x',file))), self.checkinf(upper_x,('upper_x', ('upper bound in x',file))),  
                                                  bound_y, custom_y, self.checkinf(lower_y,('lower_y',('lower bound in y',file))), self.checkinf(upper_y,('upper_y',('upper bound in y',file))), 
                                                  bound_z, custom_z, self.checkinf(lower_z,('lower_z',('lower bound in z',file))), self.checkinf(upper_z,('upper_z',('upper bound in z',file)))]) 

            self.submit_signal.emit()

        else:

            self.back.emit()

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

        while self.convertNum > 0:

            self.convertFields(1)

        self.convertFields(0)

        self.path.append('')

        self.convertwidget[0][0][1].setText('No file selected')


