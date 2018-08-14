import pdb

from fnmatch import fnmatch

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .InputWidgetClass import InputWidget

import json, sys, os

class SubmissionWidget(QWidget):

    param_options = []

    submitClusterSignal = pyqtSignal()

    submitLocalSignal = pyqtSignal()

    backSignal = pyqtSignal()

    errormsg = []

    boxOptions = []

    def __init__(self, inputWidget):

        super(SubmissionWidget, self).__init__()

        self.window(inputWidget)

    def window(self, inputWidget):

        vlay = QVBoxLayout()

        scrollArea = QScrollArea()

        groupbox = QGroupBox()

        rowcount = 0

        self.layout_list = []

        self.param_layout = []

        self.param_row = 0

        self.box_widgets = []

    #   Pull user and server info 

        self.configio = 1

        self.pullConfig()

    #   Parameterize options

        self.layout_list.append(QHBoxLayout())

        self.validateposdouble = QDoubleValidator()

        self.validateposdouble.setRange(0, 100000, 15)

        self.validateposint = QIntValidator(0,10000)

        self.validatedouble = QDoubleValidator()

        #This second append is used for the parameterization options

        self.layout_list.append(QVBoxLayout())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

        self.param_num = 0

        self.param_row = rowcount + 1

        self.param_widgets = [QLabel("Parameterization:"), QLabel(), QPushButton("+"), QPushButton("-")]

        self.param_widgets[2].clicked.connect(lambda: self.paramOptions(self.param_row, 0))

        self.param_widgets[3].clicked.connect(lambda: self.paramOptions(self.param_row, 1))

        self.param_widgets[1].setNum(0)

        self.userInput(inputWidget)

        for widget in self.param_widgets:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

    #   Options for submitting jobs

        self.layout_list.append(QHBoxLayout())

        labelone = QLabel('Queue Name:  ')

        labeltwo = QLabel('Server Directory:  ')

        width = [labelone.fontMetrics().boundingRect('Queue Name:  ').width(), labeltwo.fontMetrics().boundingRect('Server Directory:  ').width()]

        self.cluster_widgets = [QLabel("Nodes:"), QLineEdit(), QLabel("Processors per Node:"), QLineEdit(), QLabel('Walltime:'), QLineEdit(), 
                                QLabel('Queue Name'), QLineEdit(), QLabel('Job Name:'), QLineEdit()]

        [widget.setFixedWidth(width[bool(i)]) for i,widget in enumerate(self.cluster_widgets[6:]) if isinstance(widget, QLabel)]

        [widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter) for i,widget in enumerate(self.cluster_widgets) if isinstance(widget, QLabel) and i > 5]

        self.cluster_widgets[1].setValidator(self.validateposint)

        self.cluster_widgets[3].setValidator(self.validateposint)

        walltimeValidator = QRegExpValidator()

        walltimeValidator.setRegExp(QRegExp(r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]'))

        self.cluster_widgets[5].setValidator(walltimeValidator)

        self.cluster_widgets[5].setPlaceholderText('In HH:MM:SS format')

        self.cluster_widgets[9].setPlaceholderText('Default name is \'batching\'')

        for widget in self.cluster_widgets[0:6]:

            self.layout_list[rowcount].addWidget(widget)

        vlay.addLayout(self.layout_list[rowcount])

        rowcount = rowcount + 1

        self.layout_list.append(QHBoxLayout())

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
        
    #   Add final buttons

        self.layout_list.append(QHBoxLayout())

        submitWidgets = [QPushButton('Back'), QPushButton('Create Local File'), QPushButton("Submit to Cluster")]

        submitWidgets[0].clicked.connect(lambda: self.back())

        submitWidgets[1].clicked.connect(lambda: self.submit(0))

        if self.configio == 0:

            submitWidgets[2].setEnabled(False)

        else: 

            submitWidgets[2].clicked.connect(lambda: self.submit(1))

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

    def paramOptions(self, row, io):

        #io = 0 for adding param fields

        if io == 0:

            self.param_options.append(QComboBox())

            self.param_options[self.param_num].setObjectName(str(self.param_num))

            self.param_options[self.param_num].clear()

            self.param_options[self.param_num].addItems(self.boxOptions)

            self.param_options[self.param_num].setObjectName(str(self.param_num))

            self.param_options[self.param_num].currentIndexChanged.connect(lambda: self.param_box_widgets(1))

            self.param_layout.append(QHBoxLayout())

            self.param_layout[self.param_num].addItem(QSpacerItem(100,20))

            self.param_layout[self.param_num].addWidget(self.param_options[self.param_num])

            self.param_layout[self.param_num].setAlignment(Qt.AlignLeft)

            self.layout_list[row].addLayout(self.param_layout[self.param_num])

            self.param_box_widgets(0)

            self.param_num = self.param_num + 1

            self.param_widgets[1].setNum(self.param_num)

        elif io == 1:

            if self.param_num > 0:

                self.param_num = self.param_num - 1

                self.param_widgets[1].setNum(self.param_num)

                while self.param_layout[self.param_num].count():

                    item = self.param_layout[self.param_num].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                self.layout_list[row].removeItem(self.param_layout[self.param_num])

                del self.param_layout[self.param_num]

                del self.box_widgets[self.param_num]

                del self.param_options[self.param_num]
                

    def param_box_widgets(self, butsend):

        if butsend == 0:

            option = 'box_dir'

            row = self.param_num

            self.box_widgets.append([QComboBox(), QLabel('Increase'), QLineEdit(), QLabel('Number of Steps:'), QLineEdit()])

            self.box_widgets[row][0].currentIndexChanged.connect(lambda: self.labelchanges(row))

            self.box_widgets[row][4].setValidator(self.validateposint)

            for widget in self.box_widgets[row]:

                self.param_layout[self.param_num].addWidget(widget)

        elif butsend == 1:

            button = self.sender()

            row = int(button.objectName())

            option = button.currentText()

        self.box_widgets[row][0].clear()

        #This try pass statement is used in order to ensure that the button is reset at the beginning of every change.

        self.box_widgets[row][0].setFixedWidth(200)

        self.box_widgets[row][2].setPlaceholderText('')

        self.box_widgets[row][4].setPlaceholderText('')

        if option == 'box_dir':

            self.box_widgets[row][0].addItems(['x','y','z'])

            self.box_widgets[row][2].setPlaceholderText('di dj dk')

            #self.box_widgets[row][4].setPlaceholderText(di dj dk')

        elif option == 'deform':

            #Create the combobox options for all of the deform commands 

            boxitems = []

            for i in range(0,self.deform_num):

                boxitems.append('deform '+str(i+1)+': def_rate')

                boxitems.append('deform '+str(i+1)+': stress_l')

                boxitems.append('deform '+str(i+1)+': stress_u')

                boxitems.append('deform '+str(i+1)+': time_always_flip')

                boxitems.append('deform '+str(i+1)+': flip_frequency')

            self.box_widgets[row][0].addItems(boxitems)

            self.box_widgets[row][2]

        elif option == 'dynamics':

            dynamics_options = []

            if self.dynamics_input[0] == 'ld':

                dynamics_options.append('damping_coefficient')

            if self.hybridFlag == 2:

                dynamics_options.append('energy_min_freq')

            self.box_widgets[row][0].addItems(dynamics_options)

        elif option == 'minimize':

            self.box_widgets[row][0].addItems(['max_iteration', 'tolerance'])

        elif option == 'fix':

            fix_options = []

            for item in self.fixCommands:

                group = 'Fix ' + item[0] + ': '

                fix_options.append(group + 'assign_x')

                fix_options.append(group + 'assign_y')

                fix_options.append(group + 'assign_z')

                fix_options.append(group + 'disp_limit')

                fix_options.append(group + 'time_start')  

                fix_options.append(group + 'time_end') 

                if item[10] == 't':

                    fix_options.append(group + 'grad_ref_l')

                    fix_options.append(group + 'grad_ref_u')

            self.box_widgets[row][0].addItems(fix_options)

        elif option == 'grain_dir':

            self.box_widgets[row][0].addItem('overlap')

        elif option == 'grain_move':

            grain_move_options = []

            for i in range(0, self.grain_num):

                grain_move_options.append('Grain ' + str(i + 1) + ': move_x')

                grain_move_options.append('Grain ' + str(i + 1) + ': move_y')

                grain_move_options.append('Grain ' + str(i + 1) + ': move_z')

            self.box_widgets[row][0].addItems(grain_move_options)

        elif option == 'grain_mat':

            grain_mat_options = []

            for i in range(0,self.grain_num):

                grain_mat_options.append('Grain ' + str(i + 1) + ': x-orientation')

                grain_mat_options.append('Grain ' + str(i + 1) + ': y-orientation')

                grain_mat_options.append('Grain ' + str(i + 1) + ': z-orientation')

            self.box_widgets[row][0].addItems(grain_mat_options)

            self.box_widgets[row][2].setPlaceholderText('di dj dk')

            # #self.box_widgets[row][4].setPlaceholderText(di dj dk')

        elif option == 'group':

            for item in self.groupCommands:

                group_options = []

                group_name = item[0]

                group_shape = item[3]

                dirs = ['x', 'y', 'z']

                if group_shape == 'block':

                    group_options.append( group_name+ ': x-lower_b')

                    group_options.append( group_name+ ': x-upper_b')

                    group_options.append( group_name+ ': x-orientation')

                    group_options.append( group_name+ ': y-lower_b')

                    group_options.append( group_name+ ': y-upper_b')

                    group_options.append( group_name+ ': y-orientation')

                    group_options.append( group_name+ ': z-lower_b')

                    group_options.append( group_name+ ': z-upper_b')

                    group_options.append( group_name+ ': z-orientation')

                elif group_shape == 'cylinder' or group_shape == 'cone' or group_shape == 'tube':

                    group_axis_dir = int(item[23])

                    non_group_axis_dir = [x for x in [1, 2, 3] if x not in [group_axis_dir]]

                    axis = ['x', 'y', 'z']

                    if group_shape == 'cylinder':

                        group_options.append( group_name+ ': radius')

                    elif group_shape == 'cone':

                        group_options.append( group_name+ ': radius_large')

                        group_options.append( group_name+ ': radius_small')

                    elif group_shape == 'tube':

                        group_options.append( group_name+ ': radius_large')

                        group_options.append( group_name+ ': radius_small')

                    group_options.append( group_name+ ':' + dirs[group_axis_dir -1] + '-lower_b')

                    group_options.append( group_name+ ':' + dirs[group_axis_dir -1]+'-upper_b')

                    group_options.append( group_name+ ':' + dirs[group_axis_dir -1]+'-orientation')

                    group_options.append( group_name+ ': centroid along ' + axis[non_group_axis_dir[0]-1])

                    group_options.append( group_name+ ': centroid along ' + axis[non_group_axis_dir[1]-1])

                elif group_shape == 'sphere':

                    group_options.append( group_name+ ': radius')

                    group_options.append( group_name+ ': centroid along x')

                    group_options.append( group_name+ ': centroid along y')

                    group_options.append( group_name+ ': centroid along z')

            self.box_widgets[row][0].addItems(group_options)

        elif option == 'modify':

            modify_options = []

            dirs = ['x', 'y', 'z']

            for item in self.modifyCommands:

                modify_name = item[0]

                modify_style = item[1]

                if modify_style == 'delete' or modify_style == 'cg2at':

                    modify_shape = item[2]

                    modify_axis = item[23]

                    if modify_shape == 'block':

                        modify_options.append(modify_name +  ': x-lower_b')

                        modify_options.append(modify_name +  ': x-upper_b')

                        modify_options.append(modify_name +  ': x-orientation')

                        modify_options.append(modify_name +  ': y-lower_b')

                        modify_options.append(modify_name +  ': y-upper_b')

                        modify_options.append(modify_name +  ': y-orientation')

                        modify_options.append(modify_name +  ': z-lower_b')

                        modify_options.append(modify_name +  ': z-upper_b')

                        modify_options.append(modify_name +  ': z-orientation')

                        self.box_widgets[row][0].currentIndexChanged.connect(lambda: self.labelchanges(row))

                    elif modify_shape == 'cylinder' or modify_shape == 'cone' or modify_shape == 'tube':

                        modify_axis_dir = int(item[23])

                        non_modify_axis_dir = [x for x in [1, 2, 3] if x not in [modify_axis_dir]]

                        axis = ['x', 'y', 'z']

                        if modify_shape == 'cylinder':

                            modify_options.append(modify_name +  ': radius')

                        elif modify_shape == 'cone':

                            modify_options.append(modify_name +  ': radius_large')

                            modify_options.append(modify_name +  ': radius_small')

                        elif modify_shape == 'tube':

                            modify_options.append(modify_name +  ': radius_large')

                            modify_options.append(modify_name +  ': radius_small')

                        modify_options.append(modify_name +  ':' + dirs[modify_axis -1] + '-lower_b')

                        modify_options.append(modify_name +  ':' + dirs[modify_axis-1] + '-upper_b')

                        modify_options.append(modify_name +  ':' + dirs[modify_axis-1] + '-orientation')

                        modify_options.append(modify_name +  ': centroid along ' + axis[non_modify_axis_dir[0] -1])

                        modify_options.append(modify_name +  ': centroid along ' + axis[non_modify_axis_dir[1] -1])

                        self.box_widgets[row][0].currentIndexChanged.connect(lambda: self.labelchanges(row))

                    elif modify_shape == 'sphere':

                        modify_options.append(modify_name +  ': radius')

                        modify_options.append(modify_name +  ': centroid along x')

                        modify_options.append(modify_name +  ': centroid along y')

                        modify_options.append(modify_name +  ': centroid along z')

                elif modify_style == 'dislocation':

                    modify_options.append(modify_name +  ': centroid along x')

                    modify_options.append(modify_name +  ': centroid along y')

                    modify_options.append(modify_name +  ': centroid along z')

                    modify_options.append(modify_name +  ': character angle')

                elif modify_style == 'cutoff':

                    modify_options.append(modify_name +  ': depth')

                    modify_options.append(modify_name +  ': tolerance')

                elif modify_style == 'add_atom':

                    modify_options.append(modify_name +  ': displacement along x')

                    modify_options.append(modify_name +  ': displacement along y')

                    modify_options.append(modify_name +  ': displacement along z')    

            self.box_widgets[row][0].addItems(modify_options)

        elif option == 'neighbor':
        
            self.box_widgets[row][0].addItem('neighbor_freq')

        elif option == 'run':

            self.box_widgets[row][0].addItem('time_step')

        elif option == 'temp':

            self.box_widgets[row][0].addItem('temp')

        elif option == 'unit_type':

            unit_type_options = []

            for index, num in enumerate(self.subdomain_num):

                for i in range(0,num):

                    unit_type_options.append('Subdomain ' + str(i + 1) + ' in grain ' + str(index + 1) + ': unit_type')

            self.box_widgets[row][0].addItems(unit_type_options)

        elif option == 'unit_num':

            unit_num_options = []

            for index, num in enumerate(self.subdomain_num):

                for i in range(0,num):

                    unit_num_options.append('Subdomain ' + str(i + 1) + ' in grain ' + str(index + 1) + ': x-num')

                    unit_num_options.append('Subdomain ' + str(i + 1) + ' in grain ' + str(index + 1) + ': y-num')

                    unit_num_options.append('Subdomain ' + str(i + 1) + ' in grain ' + str(index + 1) + ': z-num')

            self.box_widgets[row][0].addItems(unit_num_options)


    def userInput(self, inputWidget):

        #This widget pulls data from the inputWidget to populate parameterize with only options that are useful to the user

        self.deform_num = inputWidget.deform_num

        self.grain_num = inputWidget.grain_num

        self.outputList = inputWidget.output_list

        self.modify_num = inputWidget.modify_num

        self.subdomain_num = inputWidget.subdomain_num

        self.optionsForBox()


    def optionsForBox(self):

        #Saving the old options. This is used to add the new options to the new comboboxes

        oldOptions = self.boxOptions

        #Options to check for which commands the user has provided 

        self.boxOptions = ['box_dir', 'grain_dir', 'grain_mat', 'grain_move', 'neighbor', 'run', 'unit_num', 'unit_type']

        self.hybridFlag = 0

        #Flags are used in order to make sure the combo box is only populated once with each command type

        mflag = 1

        gflag = 1

        fflag = 1

        self.fixCommands = []

        self.groupCommands = []

        self.modifyCommands = []

        self.deformCommands = []

        self.dynamics_input = ['vv', 500, 1]

        for label, vals in self.outputList:

            if label == 'dynamics':

                self.boxOptions.append(label)

                self.dynamics_input = vals

                self.hybridFlag = self.hybridFlag + 1

            elif label == 'deform':

                self.boxOptions.append(label)

                self.deformCommands.append(vals)

            elif label == 'minimize':

                self.boxOptions.append(label)

                self.hybridFlag = self.hybridFlag + 1

            elif label == 'modify':

                if mflag:

                    self.boxOptions.append(label)

                self.modifyCommands.append(vals)

                mflag = 0

            elif label == 'group':

                if gflag:

                    self.boxOptions.append(label)

                self.groupCommands.append(vals)

                gflag = 0

            elif label == 'temp':

                self.boxOptions.append(label)

            elif label == 'fix':

                if fflag:

                    self.boxOptions.append(label)

                self.fixCommands.append(vals)

                fflag = 0

        if self.hybridFlag != 0 and self.dynamics_input[0] != 'ld':

            for item in self.boxOptions:

                if item == 'dynamics':

                    del item


        #Finding missing elements to add to existing boxes

        newOptions = []

        removeItem = []

        for item in self.boxOptions:

            if item not in oldOptions:

                newOptions.append(item)

        for index,item in enumerate(oldOptions):

            if item not in self.boxOptions:

                removeItem.append(index)


        for box in self.param_options:

            box.addItems(newOptions)

            for item in removeItem:

                box.removeItem(item)


    def labelchanges(self,row):

        button = self.sender()

        option = button.currentText()

        if fnmatch(option, "*orientation"):

            self.box_widgets[row][2].setPlaceholderText("di dj dk")

            # self.box_widgets[row][4].setPlaceholderText("di dj dk")
        
        else: 

            if fnmatch(option, "*def_rate"):

                self.box_widgets[row][2].setValidator(self.validatedouble)

            elif fnmatch(option, "*stress_?"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option,"*time*"):

                self.box_widgets[row][2].setValidator(self.validateposint)

            elif fnmatch(option, "*frequency"):

                self.box_widgets[row][2].setValidator(self.validateposint)

            elif fnmatch(option, "damping_coefficient"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "energy_min_freq"):

                self.box_widgets[row][2].setValidator(self.validateposint)

            elif fnmatch(option, "max_iteration"):

                self.box_widgets[row][2].setValidator(self.validateposint)

            elif fnmatch(option, "*tolerance"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "*assign_?"):

                self.box_widgets[row][2].setValidator(self.validatedouble)

            elif fnmatch(option, "*disp_limit"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "*grad_ref_?"):

                self.box_widgets[row][2].setValidator(self.validatedouble)

            elif fnmatch(option, "*move_?"):

                self.box_widgets[row][2].setValidator(self.validatedouble)

            elif fnmatch(option, "*bound"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "*radius"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "*centroid*"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, "*depth"):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, 'temp'):

                self.box_widgets[row][2].setValidator(self.validateposdouble)

            elif fnmatch(option, 'unit_type'):

                self.box_widgets[row][2].setValidator(self.validateposint)

            elif fnmatch(option, "*-num"):

                self.box_widgets[row][2].setValidator(self.validateposint)

            self.box_widgets[row][2].setPlaceholderText('')

            self.box_widgets[row][4].setPlaceholderText('')

    def back(self):

        self.backSignal.emit()

    def submit(self, submitCluster):

        self.param_list = []

        self.errormsg = []

        for i in range(0, self.param_num):

            command = str(self.param_options[i].currentText())

            if self.box_widgets[i][2].text() == '':

                delta = '1'

                self.errormsg.append(('delta', 'Missing delta for parameter ' + command))

            else: 

                delta = str(self.box_widgets[i][2].text())

            if self.box_widgets[i][4].text() == '':

                num_steps = 1

                self.errormsg.append(('num_steps', 'Missing number of steps for parameter ' + command))

            else:

                num_steps = str(self.box_widgets[i][4].text())

            if command == 'grain_mat' or command == 'box_dir':

                if len(delta.split()) != 3:

                    self.errormsg.append(('delta', 'Incorrect format for delta in ' + command))

                    delta = ['1 1 1']

            if command == 'box_dir':

                self.param_list.append((command, [str(self.box_widgets[i][0].currentText())], [float(i) for i in delta.split()], int(num_steps)))

            elif command == 'deform':

                placeholder = str(self.box_widgets[i][0].currentText()).split(':')

                param = placeholder[1].strip()

                name = int(placeholder[0].split()[1])

                direction = self.deformCommands[name-1][2]

                self.param_list.append((command, [str(name), direction, param], self.convert(delta), int(num_steps)))

            elif command == 'fix':

                placeholder = str(self.box_widgets[i][0].currentText()).split(":")

                param = [placeholder[1].strip()]

                name = placeholder[0].split()[1]

                if fnmatch(param[0], '*time*'):

                    param.insert(0, 'time')

                output = []

                output.append(name)

                output.extend(param)

                self.param_list.append((command, output, self.convert(delta), int(num_steps)))

            elif command == 'grain_move':

                placeholder = str(self.box_widgets[i][0].currentText()).split(':')


                val = (self.convert(delta))

                param = placeholder[1].strip()

                if param == 'move_x':
                    dvec = [val, 0, 0]
                elif param == 'move_y':
                    dvec = [0, val, 0]
                elif param == 'move_z':
                    dvec = [0, 0, val]

                name = str(placeholder[0].split()[1])

                self.param_list.append((command, [name], dvec, int(num_steps)))

            elif command == 'grain_mat':

                placeholder = str(self.box_widgets[i][0].currentText()).split(':')

                param = placeholder[1].strip().split('-')[0]

                name = int(placeholder[0].split()[1])

                self.param_list.append((command, [str(name), param], [int(i) for i in delta.split()], int(num_steps)))

            elif command == 'modify':

                placeholder = str(self.box_widgets[i][0].currentText()).split(':')

                if fnmatch(placeholder[1], "*centroid*"):

                    param = ["modify_centroid_" + placeholder[1].split()[-1]]

                elif fnmatch(placeholder[1], "*displacement*"):

                    param = ["disp_" + placeholder[1].split()[-1]]

                elif fnmatch(placeholder[1], "*_b"):

                    dir = placeholder[1][0]

                    subcommand = placeholder[1].split('-')[1].strip()

                    param = [dir,subcommand]

                elif fnmatch(placeholder[1], "*radius*"):
#                   Checking for Sphere
                    if fnmatch(placeholder[1], "*radius"):

                        param = ["modify_radius_large"]

                    else:

                        param = ["modify_"+placeholder[1].strip()]

            elif command == 'group':

                placeholder = str(self.box_widgets[i][0].currentText()).split(':')

                if fnmatch(placeholder[1], "*centroid*"):

                    param = ["group_centroid_" + placeholder[1].split()[-1]]


                elif fnmatch(placeholder[1], "*_b"):

                    dir = placeholder[1][0]

                    subcommand = placeholder[1].split('-')[1].strip()

                    param = [dir,subcommand]

                elif fnmatch(placeholder[1], "*radius*"):
#                   Checking for Sphere
                    if fnmatch(placeholder[1], "*radius"):

                        param = ["group_radius_large"]

                    else:

                        param = ["group_"+placeholder[1].strip()]

                else:

                    param = [placeholder[1].strip()]

                name = placeholder[0]

                output = []

                output.append(name)

                output.extend(param)

                self.param_list.append((command, output, self.convert(delta), int(num_steps)))


            elif command == 'unit_num':

                placeholder = str(self.box_widgets[i][0].currentText()).split(":")

                param = placeholder[1].strip()[0]

                grainID = placeholder[0].split()[4]

                subdomainID = placeholder[0].split()[1]

                test = ['x', 'y', 'z']

                values = [0, 0, 0]
                
                values[test.index(param)] = delta

                if bool(int(delta)%int(num_steps)):
                
                     self.errormsg.append(('unit_num','Parameterization of unit num results in non-integer values'))
                
                else:
                
                    self.param_list.append((command, [grainID, int(subdomainID)], values, int(num_steps)))

            elif command == 'unit_type':

                placeholder = str(self.box_widgets[i][0].currentText()).split(":")

                grainID = placeholder[0].split()[4]

                subdomainID = placeholder[0].split()[1]

                if bool(int(self.convert(delta))%int(num_steps)):

                     self.errormsg.append(('unit_type','Parameterization of unit type results in non-integer values'))
                
                else: 
                
                    self.param_list.append((command, [grainID, subdomainID], self.convert(delta), int(num_steps)))

            else:

                self.param_list.append((command, [str(self.box_widgets[i][0].currentText())], float(delta), int(num_steps)))

            #print(self.param_list)


        if submitCluster:

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

            self.jobname = str(self.cluster_widgets[9].text())

            if self.jobname =='':

                self.jobname = 'batching'


            self.qname  = str(self.cluster_widgets[7].text())

            if self.qname == '':

                self.errormsg.append(('qname', 'Missing queue name in input field'))

            if self.host == '':

                self.host = self.server

            self.user = str(self.submitWidgets[5].text())

            if self.user == '':

                self.user = self.username

            self.password = str(self.submitWidgets[7].text())

            self.submitClusterSignal.emit()

        else:

            self.submitLocalSignal.emit()

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

    def refreshFields(self):

        while self.param_num > 0:

            self.paramOptions(self.param_row, 1)

        [widget.setText('') for widget in self.cluster_widgets if isinstance(widget, QLineEdit)]

        [widget.setText('') for widget in self.submitWidgets if isinstance(widget, QLineEdit)]
