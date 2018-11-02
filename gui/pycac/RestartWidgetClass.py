from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

#This file contains all of the functions necessary for the input script handling

class RestartWidget(QWidget):

    submitSignal = pyqtSignal()

    backSignal = pyqtSignal()

#   Output List

    output_list = []

#   class variables accessible by all methods

    sub_layout_list = []

    input_obj_list = []

    validateposdouble = QDoubleValidator()

    validateposdouble.setRange(0, 100000, 15)

    validateposint = QIntValidator(0,1000000)

    validatedouble = QDoubleValidator()

    restart_num = 0

    restart_path = ""

    potential_path = ""

    outpath = ""

#   grain variables

    grain_num = 0

    grain_row = 0

    grain_layout = QVBoxLayout()

    grain_widget = []

    grain_row_widget = []

    sub_grain_layout = []

#   Subdomain variables

    subdomain_num = []

    subdomain_row = []

    subdomain_widget = []

    subdomain_sub_widgets =[[]]

    subdomain_layout = []

    subdomain_grain = []

#   Simulator variables

    simulator_layout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
                
    simulator = []

    sim_rowcount = 0

    sim_num = 1

    simbox_flags = 0

#   Constrain variables

    constrain_widget = []

#   Group variables

    group_num = 0

    group_row = 0

    group_widgets = []

    group_name_array = []

    group_name_layout = []

    group_row_widgets = []

    group_layout = QVBoxLayout()

    sub_group_layout = []

    group_num_layout = []

    group_type_layout = []

    group_type_widgets = []

    fixLayout = []

    fixRow = 0

    fixflag = 0

    dispflag = []

    fixWidgets = []

    boolean_btnGroup = []

    fixnum = 0

    calLayout = []

    calRow = 0

    calflag = 0

    calWidgets = []

    calnum = 0

#   Modify Variables

    modify_num = 0

    add_atom_count = 0

    modify_row = 0

    modify_layout = QVBoxLayout()

    modify_widget = []

    modify_row_widget = []

    sub_modify_layout = []

    modify_options_layout = []

    modify_options_butngroup = []

    modify_flag = 0

#   Deform variables

    deform_widgets = []

    deform_layout = []

    deform_num = 0

#   Variables needed for adjusting the number of rows in the lattice layouts 

    def __init__(self):

        super(RestartWidget, self).__init__()

        RestartWidget.window(self)

    def window(self):

        fbox=QFormLayout()

        fin_layout = QVBoxLayout()

        scrollArea = QScrollArea()

        groupbox = QGroupBox()

        rowcount = 0

        self.label_list = []

        dir_list = ["x", "y", "z"]

    #       Filename definition
      
        self.label_list.append(QLabel("Create Project Folder" ))
        
        self.input_obj_list.append([QPushButton('Browse'), QLabel("No Folder Selected")])

        self.input_obj_list[rowcount][0].clicked.connect(lambda: self.getFileName(1))

        self.browse_width = self.input_obj_list[rowcount][0].fontMetrics().boundingRect("Browse").width() + 50

        self.input_obj_list[rowcount][0].setFixedWidth(self.browse_width)

        self.input_obj_list[rowcount][0].setToolTip("Project folder is created locally in the selected location and is uploaded to the run directory on the cluster")

        self.sub_layout_list.append(QHBoxLayout())

        for widget in self.input_obj_list[rowcount]:

            self.sub_layout_list[rowcount].addWidget(widget)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        self.outputrow = rowcount

        rowcount = rowcount+1

    #       Restart Options
     
        self.label_list.append(QLabel("Restart Options:"))        
        
        self.sub_layout_list.append(QVBoxLayout())

        self.restart_layout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

        self.restart_layout[2].setAlignment(Qt.AlignLeft)

        self.restart_layout[3].setAlignment(Qt.AlignLeft)

        self.restart_widgets = [[]]

        restart_row = rowcount

        self.restart_options(restart_row)

        self.input_obj_list.append(self.restart_widgets)

        self.restart_layout[0].setAlignment(Qt.AlignLeft)

        self.restart_groups = []

        for i in range(0,4):

            self.sub_layout_list[rowcount].addLayout(self.restart_layout[i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount+1

    #       Simulator Options

        self.label_list.append(QLabel("Simulator:"))

        self.sub_layout_list.append(QVBoxLayout())

        simulator_row = rowcount

        self.sim_options = [QRadioButton() for i in range(0,3)]

        self.sim_options[0].setText("Dynamics")

        self.sim_options[0].toggled.connect(lambda: self.dynamicOptions(simulator_row, 0))

        self.sim_options[1].setText("Statics")
        
        self.sim_options[1].toggled.connect(lambda: self.minimizeOptions(simulator_row, 0))

        self.sim_options[2].setText("Hybrid")

        self.sim_options[2].toggled.connect(lambda: self.hybridOptions(simulator_row))

        self.sim_btngroup = QButtonGroup()

        for i in range(0,3):

            self.sim_btngroup.addButton(self.sim_options[i])

        self.input_obj_list.append(self.sim_options)

        for i in range(0,3):

            self.simulator_layout[0].addWidget(self.input_obj_list[rowcount][i])

        self.sub_layout_list[rowcount].addLayout(self.simulator_layout[0])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount+1

    #       Mass

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Mass:"))

        self.input_obj_list.append(QLineEdit())

        self.input_obj_list[rowcount].setValidator(self.validateposdouble)

        self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Group options

        self.sub_layout_list.append(QVBoxLayout())

        group_lay = QHBoxLayout()

        self.groupRow = rowcount

        self.label_list.append(QLabel("Group:"))

        group_buttons = [QPushButton("+"), QPushButton("-")]

        self.group_widgets = [QLabel(str(self.group_num)), group_buttons[0], group_buttons[1]]

        group_buttons[0].clicked.connect(lambda: self.plusGroup(self.groupRow))

        group_buttons[1].clicked.connect(lambda: self.minusGroup(self.groupRow))

        self.input_obj_list.append(self.group_widgets)

        for i in range(0,3):

            group_lay.addWidget(self.input_obj_list[rowcount][i])

        self.sub_layout_list[rowcount].addLayout(group_lay)

        self.sub_layout_list[rowcount].addLayout(self.group_layout)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Element options

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Element:"))

        self.mass_group = QButtonGroup()

        mass_options = [QRadioButton("Lumped"), QRadioButton("Consistent")]

        self.mass_group.addButton(mass_options[0])

        self.mass_group.addButton(mass_options[1])

        mass_options[0].toggle()

        for i in range(0,2):

            self.sub_layout_list[rowcount].addWidget(mass_options[i])

        self.neighbor_group = QButtonGroup()

        neighbor_options = [QRadioButton("1NN"), QRadioButton("2NN")]

        self.neighbor_group.addButton(neighbor_options[0])

        self.neighbor_group.addButton(neighbor_options[1])

        neighbor_options[1].toggle()

        self.input_obj_list.append([mass_options[0], mass_options[1], neighbor_options[0], neighbor_options[1]])

        for i in range(0,2):

            self.sub_layout_list[rowcount].addWidget(neighbor_options[i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Limit command

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Limits:"))

        self.input_obj_list.append([QLabel("Atoms per cell:"), QLineEdit(),QLabel("Neighbors per atom:"), QLineEdit()])

        self.input_obj_list[rowcount][1].setValidator(self.validateposint)

        self.input_obj_list[rowcount][1].setPlaceholderText('100')

        self.input_obj_list[rowcount][3].setValidator(self.validateposint)

        self.input_obj_list[rowcount][3].setPlaceholderText('100')

        for i  in range(0,4):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Neighbor command

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Neighbor:"))

        self.input_obj_list.append([QLabel("Bin size:"), QLineEdit(),QLabel("Update Neighbor Frequency:"), QLineEdit()])

        self.input_obj_list[rowcount][1].setValidator(self.validateposdouble)

        self.input_obj_list[rowcount][1].setPlaceholderText('1')

        self.input_obj_list[rowcount][3].setValidator(self.validateposint)

        self.input_obj_list[rowcount][3].setPlaceholderText('100')

        for i  in range(0,4):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Box Direction

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Box Direction (format is i j k):"))

        self.input_obj_list.append([QLabel("x-direction:"), QLineEdit(),QLabel("y-direction:"), QLineEdit(), QLabel("z-direction:"), QLineEdit()])

        self.input_obj_list[rowcount][1].setPlaceholderText("1 0 0")

        self.input_obj_list[rowcount][3].setPlaceholderText("0 1 0")

        self.input_obj_list[rowcount][5].setPlaceholderText("0 0 1")

        for i  in range(0,6):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Deform commands

        self.sub_layout_list.append(QVBoxLayout())

        self.label_list.append(QLabel("Deform:"))

        self.deform_widgets.append([QCheckBox("True")])

        self.defrow = rowcount

        self.deform_widgets[0][0].toggled.connect(lambda: self.defoptions(self.defrow))

        self.deform_layout.append(QHBoxLayout())

        self.deform_layout[0].addWidget(self.deform_widgets[0][0])

        self.sub_layout_list[rowcount].addLayout(self.deform_layout[0])

        self.input_obj_list.append(self.deform_widgets)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Convert Command

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Convert:"))

        self.input_obj_list.append( [QLabel("Convert vector (i j k):"), QLineEdit()])

        self.input_obj_list[rowcount][1].setPlaceholderText('1 0 0')

        for i in range(0,2):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Potential Commands

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Potential:"))

        eam_but = QRadioButton("EAM")

        lj_but = QRadioButton("L-J")

        potential_button_group = QButtonGroup()

        potential_button_group.addButton(eam_but)

        potential_button_group.addButton(lj_but)

        self.input_obj_list.append([eam_but, lj_but, QPushButton("Browse"), QLabel("No Folder Selected")])

        self.input_obj_list[rowcount][2].clicked.connect(lambda: self.getFileName(3))

        self.input_obj_list[rowcount][2].setFixedWidth(self.browse_width)

        for i  in range(0,4):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        self.sub_layout_list[rowcount].setAlignment(Qt.AlignLeft)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        self.potential_num = rowcount

        rowcount = rowcount + 1

    #       Constrain Commands

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Constrain:"))

        self.input_obj_list.append(QCheckBox("True"))

        constrain_row = rowcount

        self.input_obj_list[rowcount].stateChanged.connect(lambda: self.constrainField(constrain_row))

        self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Dump Commands

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Dump:"))

        self.input_obj_list.append([QLabel("Output Freq:"), QLineEdit(), QLabel("Reduce Freq:"), QLineEdit(), QLabel("Restart Freq:"), 
                               QLineEdit(), QLabel("Log Freq:"), QLineEdit()])

        self.input_obj_list[rowcount][1].setValidator(self.validateposint)

        self.input_obj_list[rowcount][1].setPlaceholderText('500')

        self.input_obj_list[rowcount][3].setValidator(self.validateposint)

        self.input_obj_list[rowcount][3].setPlaceholderText('1000')

        self.input_obj_list[rowcount][5].setValidator(self.validateposint)

        self.input_obj_list[rowcount][5].setPlaceholderText('5000')

        self.input_obj_list[rowcount][7].setValidator(self.validateposint)

        self.input_obj_list[rowcount][7].setPlaceholderText('50')

        for i in range(0, 8):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Run Commands

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Run:"))

        self.input_obj_list.append([ QLabel("Number of steps:"), QLineEdit(), QLabel("Time step (ps):"), QLineEdit()])

        self.input_obj_list[rowcount][1].setValidator(self.validateposint)

        self.input_obj_list[rowcount][3].setValidator(self.validateposdouble)

        self.input_obj_list[rowcount][3].setPlaceholderText('0.002')

        for i in range(0,4):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Submit buttons

        submit_layout = QHBoxLayout()

        back = QPushButton("Back")

        back.clicked.connect(lambda: self.backButton())

        width = back.fontMetrics().boundingRect("Back").width() + 200

        back.setMaximumWidth(width)

        submit_layout.addWidget(back)

        submit = QPushButton("Next")

        submit.clicked.connect(lambda: self.submission(self.label_list))

        width = submit.fontMetrics().boundingRect("Next").width() + 200

        submit.setMaximumWidth(width)

        submit_layout.addWidget(submit)

        fin_layout.addLayout(fbox)

        fin_layout.addLayout(submit_layout)       

    #       Final set-up

        groupbox.setLayout(fin_layout)

        scrollArea.setWidget(groupbox)
        scrollArea.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scrollArea)

        rowcount = rowcount + 1
        
        self.setLayout(layout)

    def restart_options(self, row):

        self.restart_group_flag = 0

        #Restart row one

        self.restart_widgets[0].extend([QLabel('Restart File:'), QPushButton("Browse"), QLabel("No File Selected")])

        self.restart_widgets[0][1].clicked.connect(lambda: self.getFileName(2))

        self.restart_widgets[0][1].setFixedWidth(self.browse_width)

        [self.restart_layout[0].addWidget(widget) for widget in self.restart_widgets[0]]

        #Restart row two

        self.restart_layout[1].setAlignment(Qt.AlignLeft)

        self.restart_widgets.append([QLabel("Restart Group Paths:"), QPushButton('Browse'), QLabel("No Restart Groups")])

        self.restart_widgets[1][1].clicked.connect(lambda: self.getFileName(5))

        for i in range(0,3):

            self.restart_layout[1].addWidget(self.restart_widgets[1][i])  

    def restart_group_method(self, option):

        if option == 0:
        
            self.restart_widgets.append(QCheckBox("Refine All"))

            self.restart_layout[3].addWidget(self.restart_widgets[2])

            self.restart_group_flag = 1

            self.restart_group_box = [QListWidget(), QStackedWidget()]

            self.restart_group_box[0].currentRowChanged.connect(lambda: self.restart_group_method(1))

            self.restart_group_box[0].insertItems(0, [os.path.basename(path) for path in self.restart_groups])

            self.restart_group_widget = []

            self.restart_group_layout = []

            self.restart_group_fix = []

            self.restart_group_cal = []

            self.restart_refine = []

            self.displacementLimit = []

            self.grad_vals = []

            for i in range(0, len(self.restart_groups)):

                self.restart_group_layout.append([QVBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), 
                                                  QHBoxLayout(), QHBoxLayout()])

                [self.restart_group_layout[i][0].addLayout(layout) for j, layout in enumerate(self.restart_group_layout[i]) if j > 0]

                self.restart_group_layout[i][0].setAlignment(Qt.AlignTop)

                self.restart_group_fix.append([QCheckBox('Fix')])

                self.restart_group_fix[i][0].toggled.connect(lambda: self.restart_group_method(2))

                self.restart_group_layout[i][1].addWidget(self.restart_group_fix[i][0])

                self.restart_group_layout[i][2].setAlignment(Qt.AlignLeft)

                self.restart_group_cal.append([QCheckBox('Cal')])

                self.restart_group_cal[i][0].toggled.connect(lambda: self.restart_group_method(2))

                self.restart_group_layout[i][-2].addWidget(self.restart_group_cal[i][0])
                
                self.restart_group_layout[i][-2].setAlignment(Qt.AlignLeft)

                self.restart_refine.append(QCheckBox('Refine'))

                self.restart_group_layout[i][-1].addWidget(self.restart_refine[i])

                self.restart_group_layout[i][-1].setAlignment(Qt.AlignLeft)

                self.restart_group_widget.append(QWidget())

                self.restart_group_widget[i].setLayout(self.restart_group_layout[i][0])

                self.restart_group_box[1].addWidget(self.restart_group_widget[i])

                self.displacementLimit.append([])

                self.grad_vals.append([])

            button = QPushButton(max([os.path.basename(path) for path in self.restart_groups], key=len))

            width = button.fontMetrics().boundingRect(max([os.path.basename(path) for path in self.restart_groups], key=len)).width() + 7

            self.restart_group_box[0].setCurrentRow(0)

            self.restart_group_box[0].setFixedWidth(width)

            [self.restart_layout[2].addWidget(widget) for widget in self.restart_group_box]

        elif option == -1:

            if self.restart_group_flag:

                print('Delete')

                for layoutList in self.restart_group_layout:

                    for layout in layoutList[1:]:

                        while layout.count() > 0:

                            item = layout.takeAt(0)

                            widget = item.widget()

                            if widget is not None:

                                widget.deleteLater()

                while self.restart_layout[2].count() > 0:

                    item = self.restart_layout[2].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                item = self.restart_layout[3].takeAt(0)

                widget = item.widget()

                widget.deleteLater()

                del self.restart_widgets[2]

                del self.restart_group_box

                del self.restart_group_widget

        elif option == 1:

            row = self.restart_group_box[0].currentRow()

            self.restart_group_box[1].setCurrentIndex(row)

        elif option == 2:

            button = self.sender()

            row = self.restart_group_box[0].currentRow()

            if button.text() == 'Fix':

                if button.isChecked():

                    self.restart_group_fix[row].append([QCheckBox("Deform with Box"), QCheckBox("Release Force")])

                    [self.restart_group_layout[row][1].addWidget(widget) for widget in self.restart_group_fix[row][1]]

                    self.restart_group_fix[row].append([QLabel('Style:'), QComboBox()])

                    self.restart_group_fix[row][2][1].addItems(["Force", "Displacement"])

                    self.restart_group_fix[row][2][1].currentIndexChanged.connect(lambda: self.restart_fix_box(row,1))

                    [self.restart_group_layout[row][2].addWidget(widget) for widget in self.restart_group_fix[row][2]]

                    self.restart_group_fix[row].append([QLabel("Applied Vector:"), QLineEdit(), QLabel("Start Time:"), QLineEdit(), QLabel("End Time:"), QLineEdit()])

                    [self.restart_group_fix[row][3][j].setValidator(self.validateposint) for j in [3,5]]

                    self.restart_group_fix[row][3][1].setPlaceholderText('i j k')

                    [self.restart_group_layout[row][3].addWidget(widget) for widget in self.restart_group_fix[row][3]]

                    self.restart_group_fix[row].append([QCheckBox("Gradient")])

                    self.restart_group_fix[row][4][0].toggled.connect(lambda: self.restart_fix_box(row,2))

                    self.restart_group_layout[row][4].addWidget(self.restart_group_fix[row][4][0])

                else:

                    for i, layout in enumerate(self.restart_group_layout[row]):

                        if i > 0 and i < len(self.restart_group_layout[row]) - 2:

                            if i == 1: 
                                count = 1
                            else:
                                count = 0
                                del self.restart_group_fix[row][1]

                            while layout.count() > count:

                                item = layout.takeAt(count)

                                widget = item.widget()

                                if widget is not None:
                                    widget.deleteLater()

            elif button.text() == 'Cal':

                if button.isChecked():

                    self.restart_group_cal[row].extend([QLabel('Quantity:'), QComboBox()])

                    self.restart_group_cal[row][2].addItems(["Energy", "Force", "Virial"])

                    [self.restart_group_layout[row][-2].addWidget(widget) for widget in self.restart_group_cal[row][1:]]

                else:

                    while self.restart_group_layout[row][-2].count() > 1:

                        item = self.restart_group_layout[row][-2].takeAt(1)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

                    del self.restart_group_cal[row][1:]


    def restart_fix_box(self, row, option):
        
        button = self.sender()

        if option == 1:

            if button.currentText() == 'Displacement':

                self.displacementLimit[row].extend([QLabel('Displacement Limit'), QLineEdit()])

                self.displacementLimit[row][1].setValidator(self.validateposdouble)

                [self.restart_group_layout[row][2].addWidget(widget) for widget in self.displacementLimit[row]]

            else:
                while self.restart_group_layout[row][2].count() > 2:

                    item = self.restart_group_layout[row][2].takeAt(2)

                    widget = item.widget()

                    if widget is not None:
                        widget.deleteLater()

                    del self.displacementLimit[row][:]

        else: 

            if button.isChecked():

                self.grad_vals[row].append([QLabel("Vector Component:"), QComboBox(), QLabel("Gradient Axis:"), QComboBox()])

                self.grad_vals[row][0][1].addItems(["1", "2", "3"])

                self.grad_vals[row][0][3].addItems(["1", "2", "3"])

                [self.restart_group_layout[row][4].addWidget(widget) for widget in self.grad_vals[row][0]]

                self.grad_vals[row].append([QLabel("Gradient Lower Bound:"), QLineEdit(), QLabel("Gradient Upper Bound:"), QLineEdit()])

                [self.restart_group_layout[row][5].addWidget(widget) for widget in self.grad_vals[row][1]]


            else:

                counts = [1,0]

                for i,layout in enumerate(self.restart_group_layout[row][4:6]):

                    while layout.count() > counts[i]:

                        item = layout.takeAt(counts[i])

                        widget = item.widget() 

                        if widget is not None:
                            widget.deleteLater()

                    del self.grad_vals[row][0]

    def dynamicOptions(self,row, hybrid):

        self.sim_rowcount = 0

        #       Remove existing widgets

        if self.sim_num > 1 and hybrid == 0:

            for i in range(1,4):

                while self.simulator_layout[i].count():

                    item = self.simulator_layout[i].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                self.sub_layout_list[row].removeItem(self.simulator_layout[i])


            for j in range(0, len(self.simulator)):

                del self.simulator[0]

        #       Add widgets for dynamic options

        if (hybrid == 0):

            self.simulator.append([QLabel("Dynamics: "), QComboBox()])

        else:

            self.simulator.append([QLabel("Dynamics: "), QComboBox(), QLineEdit()])

            self.simulator[self.sim_rowcount][2].setPlaceholderText("Energy Min Frequency")

            self.simulator[self.sim_rowcount][2].setValidator(self.validateposint)

        self.simulator[self.sim_rowcount][1].addItems(["Langevin Dynamics", "Quenched Dynamics", "Velocity Verlet"])

        self.simulator[self.sim_rowcount][1].currentIndexChanged.connect(lambda:self.dynamicsbox(hybrid))

        for i in range(0, len(self.simulator[self.sim_rowcount])):

            self.simulator_layout[1].addWidget(self.simulator[self.sim_rowcount][i])

        self.simulator_layout[1].setAlignment(Qt.AlignLeft)

        self.sub_layout_list[row].addLayout(self.simulator_layout[1])

        self.sub_layout_list[row].addLayout(self.simulator_layout[2])

        self.dynamicsbox(hybrid, 0)

        self.sim_num = self.sim_num + 1

        self.sim_rowcount = self.sim_rowcount + 1
        
    def dynamicsbox(self, hybrid, butpass = 1):

        if butpass == 0:

            option = "Langevin Dynamics"

        else:

            box = self.sender()

            option = box.currentText()

        if option == "Langevin Dynamics":

            if hybrid == 0:

                self.simulator[0].extend([QLabel("Damping Coefficient"), QLineEdit(), QCheckBox('Temperature')])

                self.simulator[0][3].setValidator(self.validateposdouble)

                for i in range(2,4):

                    self.simulator_layout[1].addWidget(self.simulator[0][i])

                self. simulator[0][4].toggled.connect(lambda: self.tempbox())

                self.simulator_layout[2].addWidget(self.simulator[0][4])

            elif hybrid == 1:

                self.simulator[0].extend([QLineEdit(), QCheckBox('Temperature')])

                self.simulator[0][3].setPlaceholderText("Damping Coefficient")

                self.simulator[0][3].setValidator(self.validateposdouble)

                self.simulator[0][-1].toggled.connect(lambda: self.tempbox())

                self.simulator_layout[1].addWidget(self.simulator[0][3])

                self.simulator_layout[2].addWidget(self.simulator[0][4])

            self.simbox_flags = 0

        else:

            if hybrid == 0:

                counter = 2

            elif hybrid == 1:

                counter = 3

            if self.simbox_flags == 0:

                while self.simulator_layout[1].count() > counter:

                    item = self.simulator_layout[1].takeAt(counter)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                    del self.simulator[0][counter]


                while self.simulator_layout[2].count() > 0:

                    item = self.simulator_layout[2].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                    del self.simulator[0][counter]

            self.simbox_flags = 1

    def tempbox(self):

        button = self.sender()

        if button.isChecked():

            self.simulator[0].append(QLineEdit())

            self.simulator[0][-1].setValidator(self.validateposdouble)

            self.simulator[0][-1].setPlaceholderText('Temperature in kelvin')

            self.simulator_layout[2].addWidget(self.simulator[0][-1])

        else:

            while self.simulator_layout[2].count() > 1:

                item = self.simulator_layout[2].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.simulator[0][-1]

    def minimizeOptions(self,row, hybrid):

        #       Remove existing widgets

        if self.sim_num > 1 and hybrid == 0:

            self.sim_rowcount = 0

            for i in range(1,4):

                while self.simulator_layout[i].count():

                    item = self.simulator_layout[i].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                self.sub_layout_list[row].removeItem(self.simulator_layout[i])


            for j in range(0, len(self.simulator)):

                del self.simulator[0]

        #       Add widgets for static options

        self.simulator.append([QLabel("Minimize: "), QComboBox(), QLineEdit(), QLineEdit()])

        self.simulator[self.sim_rowcount][2].setPlaceholderText("Max Iteration")

        self.simulator[self.sim_rowcount][2].setValidator(self.validateposint)

        self.simulator[self.sim_rowcount][3].setPlaceholderText("Tolerance")

        self.simulator[self.sim_rowcount][3].setValidator(self.validateposdouble)

        self.simulator[self.sim_rowcount][1].addItems(["Conjugate Gradient", "Steepest Descent", "FIRE", "Quick Min"])

        for i in range(0, len(self.simulator[self.sim_rowcount])):

            self.simulator_layout[3].addWidget(self.simulator[self.sim_rowcount][i])

        self.sub_layout_list[row].addLayout(self.simulator_layout[3])

        self.sim_num = self.sim_num + 1
    
    def hybridOptions(self,row):

        #       Clear widgets

        for i in range(1,3):

            while self.simulator_layout[i].count():

                        item = self.simulator_layout[i].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

            if i -1 < len(self.simulator):         

                for j in range(0, len(self.simulator)):

                    del self.simulator[0]

            self.sub_layout_list[row].removeItem(self.simulator_layout[i])

        #       Add options

        self.dynamicOptions(row,1)

        self.minimizeOptions(row,1)

    def constrainField(self, row):

        button = self.sender()

        if button.isChecked():

            self.constrain_widget = [QLabel("Projection Direction (i j k):"), QLineEdit()]

            for i in range(0,2):

                self.sub_layout_list[row].addWidget(self.constrain_widget[i])

        else:

            for i in range(1,3):

                item = self.sub_layout_list[row].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            del self.constrain_widget

    def plusGroup(self, row):

        self.group_num = self.group_num + 1

        self.group_widgets[0].setText(str(self.group_num))

        self.addGroupRow(row)

    def minusGroup(self,row):

        if self.group_num > 0:

            self.group_num = self.group_num - 1

            self.group_widgets[0].setText(str(self.group_num))
            
            self.minusGroupRow()

    def addGroupRow(self, row):

        #       Row One

        self.group_num_layout.append([QVBoxLayout(), QVBoxLayout()])

        self.sub_group_layout.append([QHBoxLayout()])

        self.fixLayout.append([])

        self.fixWidgets.append([])

        self.dispflag.append(0)

        self.calLayout.append([])

        self.calWidgets.append([])

        self.group_name_array.append([QLabel("Group Name:"), QLineEdit()])

        self.group_name_array[self.group_num-1][1].setPlaceholderText('group_' + str(self.group_num))

        self.group_name_layout.append(QHBoxLayout())

        for widget in self.group_name_array[self.group_num-1]:

            self.group_name_layout[self.group_num-1].addWidget(widget)

        self.group_num_layout[self.group_num-1][0].addLayout(self.group_name_layout[self.group_num-1])

        self.group_row_widgets.append([QLabel("CG type"), QComboBox(), QLabel("Atom type"), QComboBox(), QLabel("Shape"),QComboBox()])

        self.group_row_widgets[self.group_row][1].addItems(["Element", "Node", "Null"])

        self.group_row_widgets[self.group_row][3].addItems(["Atom", "Null"])

        self.group_row_widgets[self.group_row][5].addItems(["Block", "Cylinder", "Cone", "Tube", "Sphere"])

        self.group_row_widgets[self.group_row][5].setObjectName(str(self.group_row + 1))

        self.group_row_widgets[self.group_row][5].currentIndexChanged.connect(lambda: self.groupShape())

        for i in range(0, len(self.group_row_widgets[self.group_row])):

            self.sub_group_layout[self.group_row][0].addWidget(self.group_row_widgets[self.group_row][i])

        self.group_num_layout[self.group_num - 1][0].addLayout(self.sub_group_layout[self.group_row][0])

        #       Shape options row 1 (initiates to block)

        self.sub_group_layout.append([])

        self.group_row_widgets.append([])

        self.sub_group_layout[self.group_row+1].append(QHBoxLayout())

        self.group_row_widgets[self.group_row+1].append([QCheckBox("Outside Shape"), QLabel("Group Type:"), QCheckBox("Fix"), QCheckBox("Cal")])

        # self.boolean_btnGroup.append(QButtonGroup())

        # self.boolean_btnGroup[self.group_num -1].addButton(self.group_row_widgets[self.group_row+1][0][1])

        # self.boolean_btnGroup[self.group_num -1].addButton(self.group_row_widgets[self.group_row+1][0][2])
        
        for i in range(2,4):

            self.group_row_widgets[self.group_row+1][0][i].setObjectName(str(self.group_num -1))

        self.group_row_widgets[self.group_row+1][0][2].stateChanged.connect(lambda: self.Fix(1))

        self.group_row_widgets[self.group_row+1][0][3].stateChanged.connect(lambda: self.Cal(1))

        for i in range(0,len(self.group_row_widgets[self.group_row+1][0])):

            self.sub_group_layout[self.group_row+1][0].addWidget(self.group_row_widgets[self.group_row+1][0][i])

        self.group_num_layout[self.group_num - 1][0].addLayout(self.sub_group_layout[self.group_row+1][0])

        #       Row 2

        self.sub_group_layout[self.group_row+1].append(QHBoxLayout())

        self.group_row_widgets[self.group_row + 1].append([QLabel("x:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

        self.group_row_widgets[self.group_row+1][1][6].setPlaceholderText('Format: i j k')

        for i in range(0,7):

            self.sub_group_layout[self.group_row+1][1].addWidget(self.group_row_widgets[self.group_row+1][1][i])


        self.group_num_layout[self.group_num - 1][0].addLayout(self.sub_group_layout[self.group_row+1][1])

        #       Row 3

        self.sub_group_layout[self.group_row+1].append(QHBoxLayout())

        self.group_row_widgets[self.group_row + 1].append([QLabel("y:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

        self.group_row_widgets[self.group_row+1][2][6].setPlaceholderText('Format: i j k')

        for i in range(0,7):

            self.sub_group_layout[self.group_row+1][2].addWidget(self.group_row_widgets[self.group_row+1][2][i])


        self.group_num_layout[self.group_num - 1][0].addLayout(self.sub_group_layout[self.group_row+1][2])

        #       Row 4

        self.sub_group_layout[self.group_row+1].append(QHBoxLayout())

        self.group_row_widgets[self.group_row + 1].append([QLabel("z:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

        self.group_row_widgets[self.group_row+1][3][6].setPlaceholderText('Format: i j k')

        for i in range(0,7):

            self.sub_group_layout[self.group_row+1][3].addWidget(self.group_row_widgets[self.group_row+1][3][i])

        self.group_num_layout[self.group_num - 1][0].addLayout(self.sub_group_layout[self.group_row+1][3])

        for layout in self.group_num_layout[self.group_num-1]:

            self.group_layout.addLayout(layout)

        self.group_row = self.group_row+ 2

    def groupShape(self):

        #       Pull information from sending box

        box = self.sender()

        option = box.currentText()

        row = int(box.objectName())

        lay_row = int(row/2)

        #       Clear information from previous widgets

        for i in range(1, len(self.sub_group_layout[row])):

            while self.sub_group_layout[row][1].count():

                item = self.sub_group_layout[row][1].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            self.group_num_layout[lay_row][0].removeItem(self.sub_group_layout[row][1])

            del self.sub_group_layout[row][1]

        for i in range(1,len(self.group_row_widgets[row])):

            del self.group_row_widgets[row][1]

        #       If statements to select the correct options for row shape

        if option == "Block":

      #       Row 2

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("x:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            self.group_row_widgets[row][1][6].setPlaceholderText('Format: i j k')

            for i in range(0,7):

                self.sub_group_layout[row][1].addWidget(self.group_row_widgets[row][1][i])


            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][1])

            #       Row 3

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("y:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            self.group_row_widgets[row][2][6].setPlaceholderText('Format: i j k')

            for i in range(0,7):

                self.sub_group_layout[row][2].addWidget(self.group_row_widgets[row][2][i])


            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][2])

          #       Row 4

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("z:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            self.group_row_widgets[row][3][6].setPlaceholderText('Format: i j k')

            for i in range(0,7):

                self.sub_group_layout[row][3].addWidget(self.group_row_widgets[row][3][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][3])

        elif option == "Cylinder" or option == "Tube" or option == "Cone":

        #           Row 2

            self.sub_group_layout[row].append(QHBoxLayout())

        #           Cylinder, tube, and cone have similar options. the only difference are the radii options.

            if option == "Cylinder":

                self.group_row_widgets[row].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Radius"), QLineEdit()])

            elif option == "Tube":

                self.group_row_widgets[row].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Outer Radius"), QLineEdit(), QLabel("Inner Radius"), QLineEdit()])

            elif option == "Cone":

                self.group_row_widgets[row].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Large Radius"), QLineEdit(), QLabel("Small Radius"), QLineEdit()])

            self.group_row_widgets[row][1][1].addItems(["1", "2", "3"])

            self.group_row_widgets[row][1][1].setObjectName(str(row))

            self.group_row_widgets[row][1][1].currentIndexChanged.connect(lambda: self.centroidlabels(1))

            for i in range(0,len(self.group_row_widgets[row][1])):

                self.sub_group_layout[row][1].addWidget(self.group_row_widgets[row][1][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][1])

        #           Row 3

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("Group Axis:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            self.group_row_widgets[row][2][6].setPlaceholderText('Format: i j k')

            for i in range(0,7):

                self.sub_group_layout[row][2].addWidget(self.group_row_widgets[row][2][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][2])

        #           Row 4

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("Centroid in non group axis directions:"), QLabel('2'),  QLineEdit(), QLabel('3'), QLineEdit()])

            for i in range(0,5):

                self.sub_group_layout[row][3].addWidget(self.group_row_widgets[row][3][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][3])

        elif option == "Sphere":

        #          Row 1

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("Radius"), QLineEdit()])

            for i in range(0,len(self.group_row_widgets[row][1])):

                self.sub_group_layout[row][1].addWidget(self.group_row_widgets[row][1][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][1])

        #           Row 2

            self.sub_group_layout[row].append(QHBoxLayout())

            self.group_row_widgets[row].append([QLabel("Centroid:"), QLabel("x"), QLineEdit(), QLabel("y"), QLineEdit(), QLabel("z"), QLineEdit()])

            for i in range(0,7):

                self.sub_group_layout[row][2].addWidget(self.group_row_widgets[row][2][i])

            self.group_num_layout[lay_row][0].addLayout(self.sub_group_layout[row][2])

    def minusGroupRow(self):

        self.Fix(0)

        self.Cal(0)

        #       Remove Widgets

        for i in range(self.group_row-2, self.group_row ):

            for j in range(0, len(self.sub_group_layout[i])):

                while self.sub_group_layout[i][j].count():

                    item = self.sub_group_layout[i][j].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

        while self.group_name_layout[self.group_num].count():

            item = self.group_name_layout[self.group_num].takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        self.group_num_layout[self.group_num][0].removeItem(self.group_name_layout[self.group_num])

        del self.group_name_layout[self.group_num]

        del self.group_name_array[self.group_num]

        #       Remove Layouts

        for i in range(self.group_row-2, self.group_row):

            for j in range(0, len(self.sub_group_layout[self.group_row-2])):

                self.group_num_layout[self.group_num][0].removeItem(self.sub_group_layout[self.group_row-2][0])

            del self.sub_group_layout[self.group_row-2]

            del self.group_row_widgets[self.group_row-2]

        for layout in self.group_num_layout[self.group_num]:

            self.group_layout.removeItem(layout)

        del self.group_num_layout[self.group_num]

        self.group_row = self.group_row - 2

    def Fix(self, buttoncall = 15):

        if buttoncall == 0 and self.fixflag:

            row = self.group_num

            if self.fixnum > 0:

                self.fixnum = self.fixnum - 1

        #           Remove widgets

            for i in range(0, len(self.fixLayout[row])):

                while self.fixLayout[row][i].count():

                    item = self.fixLayout[row][i].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                self.group_num_layout[row][1].removeItem(self.fixLayout[row][i])

        #           Clean up lists

            for i in range(0, len(self.fixLayout[row])):

                del self.fixLayout[row][0]

                del self.fixWidgets[row][0]

        elif buttoncall == 1:

            self.fixflag = 1

            button = self.sender()

            row = int(button.objectName())

            if button.isChecked():

                self.fixnum = self.fixnum + 1

                self.fixLayout[row].append(QHBoxLayout())

      #           Row 1

                self.fixWidgets[row].append([QLabel("Fix Commands:"), QCheckBox("Deformed with Box"), QCheckBox("Release Force")])

                for i in range(0,3):

                    self.fixLayout[row][0].addWidget(self.fixWidgets[row][0][i])

                self.fixLayout[row][0].addItem(QSpacerItem(180,20))

                self.group_num_layout[row][1].addLayout(self.fixLayout[row][0])

     #           Row 2

                self.fixLayout[row].append(QHBoxLayout())

                # self.fixLayout[row][1].addItem(QSpacerItem(130,20))

                self.fixWidgets[row].append([QLabel("Style:"), QComboBox(), QLabel("Applied Vector (i j k): "), QLineEdit()])

                self.fixWidgets[row][1][1].addItems(["Force", "Displacement"])


                self.fixWidgets[row][1][1].currentIndexChanged.connect(lambda: self.disp(row)) 
        
                for i in range(0,4):

                    self.fixLayout[row][1].addWidget(self.fixWidgets[row][1][i])

                self.group_num_layout[row][1].addLayout(self.fixLayout[row][1])

        #           Row 3

                self.fixLayout[row].append(QHBoxLayout())

                # self.fixLayout[row][2].addItem(QSpacerItem(130,20))

                self.fixWidgets[row].append([QLabel("Start Time:"), QLineEdit(), QLabel("End Time:"), QLineEdit()])

                for i in range(0,4):

                    self.fixLayout[row][2].addWidget(self.fixWidgets[row][2][i])

                self.group_num_layout[row][1].addLayout(self.fixLayout[row][2])

        #           Row 4

                self.fixLayout[row].append(QHBoxLayout())

                # self.fixLayout[row][3].addItem(QSpacerItem(126,20))

                self.fixWidgets[row].append([QCheckBox("Gradient")])

                self.fixWidgets[row][3][0].stateChanged.connect(lambda: self.gradOption(row))

                self.fixLayout[row][3].addWidget(self.fixWidgets[row][3][0])

                self.group_num_layout[row][1].addLayout(self.fixLayout[row][3])

                self.fixLayout[row].append(QHBoxLayout())

                self.group_num_layout[row][1].addLayout(self.fixLayout[row][4])

            else:

                if self.fixnum > 0:

                    self.fixnum = self.fixnum - 1

        #           Remove widgets

                for i in range(0, len(self.fixLayout[row])):

                    while self.fixLayout[row][i].count():

                        item = self.fixLayout[row][i].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

                    self.group_num_layout[row][1].removeItem(self.fixLayout[row][i])

        #           Clean up lists

                for i in range(0, len(self.fixLayout[row])):

                    del self.fixLayout[row][0]

                for i in range(0, len(self.fixWidgets[row][0])):

                    del self.fixWidgets[row][0]
   
    def disp(self, row):

        box = self.sender()

        if box.currentText() == "Displacement":

            self.fixWidgets[row][1].extend([QLabel("Displacement Limit:"), QLineEdit()])

            for i in range(4, 6):

                self.fixLayout[row][1].addWidget(self.fixWidgets[row][1][i])

            self.dispflag[row] = 1

        elif self.dispflag[row] == 1:

            for i in range(4,6):

                item = self.fixLayout[row][1].takeAt(4)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.fixWidgets[row][1][4]

    def gradOption(self, row):

        button = self.sender()

        if button.isChecked():

            option_widgets = [QLabel("Vector Component:"), QComboBox(), QLabel("Gradient Axis:"), QComboBox()]

            option_widgets[1].addItems(["1", "2", "3"])

            option_widgets[3].addItems(["1", "2", "3"])

            for i in range(0,4):

                self.fixWidgets[row][3].append(option_widgets[i])

                self.fixLayout[row][3].addWidget(self.fixWidgets[row][3][i+1])

            self.fixWidgets[row].append([QLabel("Gradient Lower Bound:"), QLineEdit(), QLabel("Gradient Upper Bound:"), QLineEdit()])

            for i in range(0,4):

                self.fixLayout[row][4].addWidget(self.fixWidgets[row][4][i])

            self.group_num_layout[row][1].addLayout(self.fixLayout[row][4])

        else:

        #           Remove the added Widgets

            while self.fixLayout[row][3].count() > 1:

                item = self.fixLayout[row][3].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            for i in range(1, len(self.fixWidgets[row][3])):

                del self.fixWidgets[row][3][1]

            while self.fixLayout[row][4].count():

                item = self.fixLayout[row][4].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            del self.fixWidgets[row][4]

            self.group_num_layout[row][1].removeItem(self.fixLayout[row][4])

    def Cal(self, buttoncall=15):

        if buttoncall == 0 and self.calflag == 1:

            row = self.group_num

            if self.calnum > 0:

                self.calnum = self.calnum - 1

                while self.calLayout[row][0].count():

                    item = self.calLayout[row][0].takeAt(0)

                    widget = item.widget()

                    if widget is not None:
         
                        widget.deleteLater()

                self.group_num_layout[row][1].removeItem(self.calLayout[row][0])

                del self.calLayout[row]

                del self.calWidgets[row]

        elif buttoncall == 1:

            self.calflag = 1

            button = self.sender()

            row = int(button.objectName())

            if button.isChecked():

                self.calnum = self.calnum + 1
                
                self.calLayout[row].append(QHBoxLayout())

                self.calWidgets[row].append([QLabel("Cal Type:"), QComboBox()])

                self.calWidgets[row][0][1].addItems(["Energy", "Force", "Virial"])

                for i in range(0,2):

                    self.calLayout[row][0].addWidget(self.calWidgets[row][0][i])

                self.group_num_layout[row][1].addLayout(self.calLayout[row][0])

            else:

                if self.calnum > 0:

                    self.calnum = self.calnum - 1

                while self.calLayout[row][0].count():

                    item = self.calLayout[row][0].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                self.group_num_layout[row][1].removeItem(self.calLayout[row][0])

                del self.calLayout[row][0]

                del self.calWidgets[row][0]

    def defoptions(self, row) :

        button = self.sender()

        if button.isChecked():

            self.deform_num = 0

            self.deform_widgets[0].extend([QLabel('Start Timestep'), QLineEdit(), QLabel('End Timestep'), QLineEdit(), QLabel('Hold Strain at Step'), QLineEdit()])

            self.deform_widgets[0][-1].setPlaceholderText('No Hold')

            [widget.setValidator(self.validateposint) for widget in self.deform_widgets[0] if isinstance(widget, QLineEdit)]

            [self.deform_layout[0].addWidget(widget) for widget in self.deform_widgets[0][1:]]

            self.deform_widgets.append([QLabel('Deform style number'), QLabel('0'), QPushButton('+'), QPushButton('-')])

            self.deform_widgets[1][2].clicked.connect(lambda: self.changedef(row, 1))

            self.deform_widgets[1][3].clicked.connect(lambda: self.changedef(row, 0))

            self.deform_layout.append(QHBoxLayout())

            [self.deform_layout[1].addWidget(widget) for widget in self.deform_widgets[1]]

            self.sub_layout_list[row].addLayout(self.deform_layout[1])

            self.changedef(row,1)

        else: 

            for layoutlist in self.deform_layout[1:]:

                if isinstance(layoutlist, QHBoxLayout):

                    self.clearLayout(layoutlist)

                    self.sub_layout_list[row].removeItem(layoutlist)

                else:

                    for layout in layoutlist:

                        self.clearLayout(layout)

                        self.sub_layout_list[row].removeItem(layout)

            while self.deform_layout[0].count() > 1:

                item = self.deform_layout[0].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            del self.deform_widgets[0][1:]

            del self.deform_widgets[1:]

            del self.deform_layout[1:]


    def changedef(self,row, add):

        if add:

            widgetRow = self.deform_num + 2

            self.deform_num += 1

            self.deform_widgets.append([[QCheckBox('Deform CG'), QCheckBox('Deform Atomistic'), QLabel('Deformation Rate:'), QLineEdit()],
                                        [QLabel('Mode'), QComboBox(), QCheckBox('Flip')]])

            self.deform_widgets[widgetRow][0][-1].setValidator(self.validatedouble)

            self.deform_widgets[widgetRow][1][2].setObjectName(str(widgetRow))

            self.deform_widgets[widgetRow][1][2].toggled.connect(lambda: self.flipOptions())

            def_modes = ['xx','yy','zz','xy','xz','yz']

            self.deform_widgets[widgetRow][1][1].addItems(def_modes)

            self.deform_layout.append([QHBoxLayout(), QHBoxLayout()])

            self.deform_layout[widgetRow][1].setAlignment(Qt.AlignLeft)

            [self.sub_layout_list[row].addLayout(layout) for layout in self.deform_layout[widgetRow]]

            [self.deform_layout[widgetRow][0].addWidget(widget) for widget in self.deform_widgets[widgetRow][0]] 

            [self.deform_layout[widgetRow][1].addWidget(widget) for widget in self.deform_widgets[widgetRow][1]]

        else:

            if self.deform_num > 1:

                self.deform_num -= 1

                widgetRow = self.deform_num + 2

                for layout in self.deform_layout[widgetRow]:

                    while layout.count() > 0:

                        item = layout.takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

                [self.sub_layout_list[row].removeItem(layout) for layout in self.deform_layout[widgetRow]]

                del self.deform_layout[widgetRow]

                del self.deform_widgets[widgetRow]

        self.deform_widgets[1][1].setText(str(self.deform_num))

    def flipOptions(self):

        button = self.sender()

        num = int(button.objectName())

        if button.isChecked():

            self.deform_widgets[num][1].extend([QLabel('Lower Stress'), QLineEdit(), QLabel('Upper Stress'), QLineEdit(), QLabel('Flip Frequency'), QLineEdit()])

            [self.deform_widgets[num][1][i].setValidator(self.validatedouble) for i in [4,6]]

            self.deform_widgets[num][1][-1].setValidator(self.validateposint)

            [self.deform_layout[num][1].addWidget(widget) for widget in self.deform_widgets[num][1][3:]]

        else:

            while self.deform_layout[num][1].count() > 3:

                item = self.deform_layout[num][1].takeAt(3)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.deform_widgets[num][1][3:]



    def submission(self, labels):

        #   This method pulls data from fields and saves them to a list of (label, [values]) tuples.

        self.output_list = []

        self.errormsg = []

        for i in range(0,len(labels)):

            label = labels[i].text()

            if label == "Restart Options:":

                self.restart_pull(i)

            elif label == "Mass:":

                if str(self.input_obj_list[i].text()) == '':

                    self.errormsg.append(('Mass', 'Mass is missing')) 

                else:

                    self.output_list.append(("mass", [float(self.input_obj_list[i].text())]))

            elif label == "Group:":

                self.group(i)

            elif label == "Element:":

                self.element(i)

            elif label == "Limits:":

                if str(self.input_obj_list[i][1].text()) == '':

                    atoms_per_cell = 100

                else:

                    atoms_per_cell = int(self.input_obj_list[i][1].text())

                if str(self.input_obj_list[i][3].text()) == '':

                    atomic_neighbor_number = 100

                else:

                    atomic_neighbor_number = int(self.input_obj_list[i][3].text())

                self.output_list.append(("limit", [atoms_per_cell, atomic_neighbor_number]))

            elif label == "Neighbor:":

                if str(self.input_obj_list[i][1].text()) == '':

                    bin_size = 1

                else:

                    bin_size = float(self.input_obj_list[i][1].text())

                if str(self.input_obj_list[i][3].text()) == '':

                    neighbor_freq = 200

                else:

                    neighbor_freq = int(self.input_obj_list[i][3].text())

                self.output_list.append(("neighbor", [bin_size, neighbor_freq]))

            elif label == "Box Direction (format is i j k):":

                if str(self.input_obj_list[i][1].text()) == '':

                    box_dir_x = [1, 0, 0]
                
                elif len(str(self.input_obj_list[i][1].text()).split()) == 3:

                    box_dir_x = str(self.input_obj_list[i][1].text()).split()

                else:

                    box_dir_x = [1, 0, 0]

                    self.errormsg.append(('box_dir_x', 'Incorrect input format for box_dir in x, requires vector in form i j k. Ex. 1 0 0'))

                if str(self.input_obj_list[i][3].text()) == '':

                    box_dir_y = [0, 1, 0]
                
                elif len(str(self.input_obj_list[i][3].text()).split()) == 3:

                    box_dir_y = str(self.input_obj_list[i][3].text()).split()

                else:

                    box_dir_y = [0, 1, 0]

                    self.errormsg.append(('box_dir_y', 'Incorrect input format for box_dir in y, requires vector in form i j k. Ex. 0 1 0'))

                if str(self.input_obj_list[i][5].text()) == '':

                    box_dir_z = [0, 0, 1]
                
                elif len(str(self.input_obj_list[i][5].text()).split()) == 3:

                    box_dir_z = str(self.input_obj_list[i][5].text()).split()

                else:

                    box_dir_z = [0, 0, 1]

                    self.errormsg.append(('box_dir_z', 'Incorrect input format for box_dir in z, requires vector in form i j k. Ex. 0 0 1'))

                for i in range(0,3):

                    box_dir_x[i] = float(box_dir_x[i])

                    box_dir_y[i] = float(box_dir_y[i])

                    box_dir_z[i] = float(box_dir_z[i])

                self.output_list.append(("box_dir", [ box_dir_x[0], box_dir_x[1], box_dir_x[2], box_dir_y[0], box_dir_y[1], box_dir_y[2],
                                                      box_dir_z[0], box_dir_z[1], box_dir_z[2]]))

            elif label == "Deform:":

                self.deform(i)

            elif label == "Convert:":

                if str(self.input_obj_list[i][1].text()) == '':

                    convert_dir = [1,0,0]

                elif len(str(self.input_obj_list[i][1].text()).split()) == 3:

                    convert_dir = str(self.input_obj_list[i][1].text()).split()

                else:

                    convert_dir = [0,0,0]

                    self.errormsg.append(('convert_dir', 'Incorrect input format for convert_dir, requires vector in form i j k Ex. 1 0 0'))

                for i in range(0,3):

                    convert_dir[i] = float(convert_dir[i])

                self.output_list.append(("convert", convert_dir))

            elif label == "Potential:":

                potential_type = 'eam'

                flag = 0

                for j in range(0,2):

                    if self.input_obj_list[i][j].isChecked():

                        potential_type = str(self.input_obj_list[i][j].text()).lower()

                        flag = 1

                if potential_type == 'l-j':

                    potential_type = 'lj'

                if flag == 0:

                    self.errormsg.append(('potential_type', 'Missing potential type in Potential command'))

                else:

                    self.output_list.append(("potential", [potential_type]))

                if self.potential_path == '':

                    self.errormsg.append(('potential_path', 'Missing path for potential files in Potential command'))

            elif label == "Constrain:":

                if self.input_obj_list[i].isChecked():

                    boolean = "t"

                    constrain = str(self.constrain_widget[1].text()).split()

                    for i in range(0,3):

                        constrain[i] = float(constrain[i])

                else:

                    boolean = "f"

                    constrain = [0, 0, 0]

                self.output_list.append(("constrain", [boolean, constrain[0], constrain[1], constrain[2]]))         

            elif label == "Dump:":

                if self.input_obj_list[i][1].text() == '':

                    output_freq = 1000

                else:

                    output_freq = int(self.input_obj_list[i][1].text())

                if self.input_obj_list[i][3].text() == '':

                    reduce_freq = 1000

                else:

                    reduce_freq = int(self.input_obj_list[i][3].text())

                if self.input_obj_list[i][5].text() == '':

                    restart_freq = 5000

                else:

                    restart_freq = int(self.input_obj_list[i][5].text())

                if self.input_obj_list[i][7].text() == '':

                    log_freq = 50

                else:

                    log_freq = int(self.input_obj_list[i][7].text())


                self.output_list.append(("dump", [output_freq, reduce_freq, restart_freq, log_freq]))

            elif label == "Run:":

                if self.input_obj_list[i][1].text() == '':

                    self.errormsg.append(('total_step', 'Number of steps missing in Run command'))

                    total_step = 0

                else:

                    total_step = int(self.input_obj_list[i][1].text())

                if str(self.input_obj_list[i][3].text()) == '':

                    time_step = 0.002

                else:

                    time_step = float(self.input_obj_list[i][3].text())

                self.output_list.append(("run", [total_step, time_step]))

        self.FilePaths = [[self.restart_path, self.restart_groups, self.refine_indices], self.outpath, self.potential_path]

        # Define default values for model variables which are not needed for restart projects

        self.output_list.append(('modify_num', [0]))

        self.output_list.append(('grain_mat', [1, 'x', 1, 0, 0, 'y', 0, 1, 0, 'z', 0, 0, 1]))

        self.output_list.append(('grain_move', [1, 0., 0., 0.]))

        self.output_list.append(('grain_dir', [3, 0]))

        self.output_list.append(('subdomain', [1, 1]))

        self.output_list.append(('unit_type', [1, 1, 1]))

        self.output_list.append(('unit_num', [1, 1, 1, 1, 1]))

        self.output_list.append(('lattice', ['Cu', 'fcc', 3.615]))

        self.add_atom_vals = []

        self.submitSignal.emit()

    def restart_pull(self, index):

        boolean_restart = "t"

        self.restart_num = len(self.restart_groups)

        refine_bool = []

        i_refine = 1

        i_not_refine = 1

        for i,path in enumerate(self.restart_groups):

            if self.restart_refine[i].isChecked():

                refine_bool.append((i_refine, 0))

                i_refine += 1

            else:

                refine_bool.append((0, i_not_refine))

                i_not_refine += 1

        refine_num = max([tupl[0] for tupl in refine_bool])

        self.refine_indices = []

        self.restart_cal = 0

        self.restart_fix = 0

        for i, path in enumerate(self.restart_groups):

            if refine_bool[i][0]:
                groupname = 'group_' + str(refine_bool[i][0]+self.group_num)
                self.refine_indices.append(i)
            else:
                groupname = 'group_' + str(refine_num + refine_bool[i][1]+self.group_num)

            if self.restart_group_fix[i][0].isChecked():

                self.restart_fix += 1

                bool_release = self.restart_group_fix[i][1][1].isChecked()

                bool_deform = self.restart_group_fix[i][1][0].isChecked()

                assign_style = str(self.restart_group_fix[i][2][1].currentText())
                
                assign_vector = str(self.restart_group_fix[i][3][1].text())

                if assign_vector == '':
                    assign_vector = [1,0,0]
                    self.errormsg.append(('assign_vector', 'Missing assign vector for fix in restart group ' + os.path.basename(path)))
                else:
                    assign_vector == [float(string) for string in assign_vector.split()]

                if assign_style == 'Displacement':
                    disp_lim = (self.displacementLimit[i][1].text())
                    if displ_limit == '':
                        disp_lim = 0
                        self.errormsg.append(('disp_lim', 'Displacement limit missing for fix in restart group ' + os.path.basename(path)))
                    else:
                        disp_lim = float(disp_lim)
                else:
                    disp_lim = 0

                start_time, end_time = [self.restart_group_fix[i][3][j].text() for j in [3,5]]

                if start_time == '':
                    start_time=0
                    self.errormsg.append(('start_time','Start time missing for fix in restart group ' + os.path.basename(path)))
                else:
                    start_time=int(start_time)

                if end_time == '':
                    end_time=0
                    self.errormsg.append(('end_time', 'End time missing for fix in restart group ' + os.path.basename(path)))
                else:
                    end_time = int(end_time)

                if self.restart_group_fix[i][4][0].isChecked():
                    
                    boolean_grad = 't'

                    grad_ref_axis = str(self.grad_vals[i][0][3].currentText())

                    grad_assign_axis = str(self.grad_vals[i][0][1].currentText())

                    try:
                        lower_b = self.checkinf(str(self.grad_vals[i][1][1].text()))
                    except ValueError:
                        self.errormsg.append(('lower_b', 'Gradient Lower Bound missing for fix in restart group ' + os.path.basename(path)))

                    try:
                        upper_b = self.checkinf(str(self.grad_vals[i][1][3].text()))
                    except ValueError:
                        self.errormsg.append(('upper_b', 'Gradient Upper Bound missing for fix in restart group ' + os.path.basename(path)))
                else:

                    boolean_grad = 'f'
                    grad_ref_axis = 1
                    grad_assign_axis=1
                    lower_b=1
                    upper_b=1

                    self.output_list.append(("fix", [groupname, bool_release, bool_deform, assign_style, *assign_vector, disp_lim, 
                        'time', start_time, end_time, boolean_grad, grad_ref_axis, grad_assign_axis, lower_b, upper_b]))

            if self.restart_group_cal[i][0].isChecked():

                self.restart_cal += 1 

                caltype = str(self.restart_group_cal[i][2].currentText())   
                
                self.output_list.append(('cal', [groupname, caltype]))

        if self.refine_indices:
            self.output_list.append(('refine',['group', len(self.refine_indices), '12']))
            boolean_restart_refine = 't'
        else:
            self.output_list.append(('refine', ['group', 1, 12]))
            boolean_restart_refine = 'f'

        self.output_list.append(("restart", [boolean_restart, boolean_restart_refine]))

    def Simulator(self, index):

        #       Pull which simulator is being used

        option = ''

        for i in range(0,3):

            if self.input_obj_list[index][i].isChecked():

                option = self.input_obj_list[index][i].text()

        #       Statement to pull the data from the correct simulator

        if option == "Dynamics":

            for i in range(0,len(self.simulator[0])):

        #               This references the ComboBox containing the dyn_style options and converts the values to the correct format

                if i == 1:

                    dyn_style = self.simulator[0][i].currentText()

                    if dyn_style == "Langevin Dynamics":

                        dyn_style = "ld"

                    elif dyn_style == "Quenched Dynamics":

                        dyn_style = "qd"

                    elif dyn_style == "Velocity Verlet":

                        dyn_style = "vv"

        #               Checks for damping_coefficient

                if i == 3 and dyn_style == "ld":

                    if str(self.simulator[0][i].text()) == '':

                        self.errormsg.append(('damping_coefficient','Missing damping coefficient in Simulator command'))

                        damping_coefficient = 0

                    else:

                        damping_coefficient = float(self.simulator[0][i].text()) 

                else: 

                    damping_coefficient = 1.0

                if isinstance(self.simulator[0][i], QCheckBox):

                    if self.simulator[0][i].isChecked():

                        temp_bool = 't'

                        temperature = float(self.simulator[0][i+1].text())

                    else:

                        temp_bool = 'f'

                        temperature = 10

            energy_min_freq = 500
            
            self.output_list.append(("simulator", ["dynamics"]))

            self.output_list.append(("dynamics", [dyn_style, energy_min_freq, damping_coefficient]))

            self.output_list.append(("temperature", [temp_bool, temperature]))

        # Pulling data from static fields

        elif option == "Statics":

            for i in range(0, len(self.simulator[0])):

                if i ==1:

                    mini_style = self.simulator[0][i].currentText()

                    if mini_style == "Conjugate Gradient":

                        mini_style = "cg"

                    elif mini_style == "Steepest Descent":

                        mini_style = "sd"

                    elif mini_style == "FIRE":

                        mini_style = "fire"

                    elif mini_style == "Quick Min":

                        mini_style = "qm"

                elif i == 2:

                    if self.simulator[0][i].text() == '':

                        self.errormsg.append(('max_iteration', 'Missing max iteration in Simulator command'))

                        max_iteration = 0

                    else:

                        max_iteration = int(self.simulator[0][i].text())

                elif i == 3:

                    if self.simulator[0][i].text() == '':

                        self.errormsg.append(('tolerance', 'Missing tolerance in Simulator command'))

                        tolerance = 0

                    else:

                        tolerance = self.simulator[0][i].text()

            self.output_list.append(("simulator", ["statics"]))

            self.output_list.append(("minimize", [mini_style, max_iteration, tolerance]))

        elif option == "Hybrid":

            for i in range(0, len(self.simulator)):

                for j in range(0, len(self.simulator[i])):

                #   i ==0 is for the dynamics options fields in the hybrid selection
                    if i == 0:

                        if j == 1:

                            dyn_style = self.simulator[i][j].currentText()

                            if dyn_style == "Langevin Dynamics":

                                dyn_style = "ld"

                            elif dyn_style == "Quenched Dynamics":

                                dyn_style = "qd"

                            elif dyn_style == "Velocity Verlet":

                                dyn_style = "vv"

                        elif j == 2:

                            if self.simulator[i][j].text() == '':

                                self.errormsg.append(('energy_min_freq', 'Missing energy min frequency in Simulator command'))

                                energy_min_freq = 0

                            else:

                                energy_min_freq = int(self.simulator[i][j].text())

                        if j == 3 and dyn_style == "ld":


                            if str(self.simulator[i][j].text()) == '':

                                self.errormsg.append(('damping_coefficient','Missing damping coefficient in Simulator command'))

                                damping_coefficient = 0

                            else:

                                damping_coefficient = float(self.simulator[i][j].text()) 

                        else:

                            damping_coefficient = 1.0

                        if isinstance(self.simulator[i][j], QCheckBox):

                            if self.simulator[i][j].isChecked():

                                temp_bool = 't'

                                temperature = float(self.simulator[i][j+1].text())

                            else:

                                temp_bool = 'f'

                                temperature = 10

                    elif i == 1:

                        if j == 1:

                            mini_style = self.simulator[i][j].currentText()

                            if mini_style == "Conjugate Gradient":

                                mini_style = "cg"

                            elif mini_style == "Steepest Descent":

                                mini_style = "sd"

                            elif mini_style == "FIRE":

                                mini_style = "fire"

                            elif mini_Style == "Quick Min":

                                mini_style = "qm"

                        elif j == 2:

                            if self.simulator[i][j].text() == '':

                                self.errormsg.append(('max_iteration', 'Missing max iteration in Simulator command'))

                                max_iteration = 0

                            else:

                                max_iteration = int(self.simulator[i][j].text())

                        elif j == 3:

                            if self.simulator[i][j].text() == '':

                                self.errormsg.append(('tolerance', 'Missing tolerance in Simulator command'))

                                tolerance = 0

                            else:

                                tolerance = self.simulator[i][j].text()

            self.output_list.append(("simulator", ["hybrid"]))

            self.output_list.append(("dynamics", [dyn_style, energy_min_freq, damping_coefficient]))

            self.output_list.append(("minimize", [mini_style, max_iteration, tolerance]))

            self.output_list.append(('temperature', [temp_bool, temperature]))

        elif option == '':

            self.errormsg.append(('Simulator', 'Simulator has not been selected'))

    #   Pulls the data from element and sends to output

    def element(self,index):

        element = []

        for button in self.input_obj_list[index]:

            if button.isChecked():

                text = str(button.text())

                if text == '1NN':

                    element.append('1')

                elif text == '2NN': 

                    element.append('2')

                else:

                    element.append(text.lower())

        self.output_list.append(("element", element))

    #   Pulls the data from the deform command

    def deform(self, index):

        boolbutton = self.deform_widgets[0][0]

        if boolbutton.isChecked():

            output = []

            # Row 1 data

            boolean_def = "t"

            times = [widget.text() for widget in self.deform_widgets[0] if isinstance(widget,QLineEdit)]

            timeoptions = ['time_start', 'time_end', 'time_always_flip']

            for i,time in enumerate(times):

                if not time:

                    if i < 2:

                        self.errormsg.append((timeoptions[i], 'Missing time parameter {} in deform'.format(timeoptions[i])))

                        times[i] = 100

                    else:

                        try:

                            times[2] = int(times[1]) + 1

                        except ValueError:

                            pass

                else: 

                    times[i] = int(times[i])

            times[1], times[2] = times[2], times[1]

            def_params = []

            for row in range(2, self.deform_num+2):

                bools = ['f','t'] 

                output.append(str(self.deform_widgets[row][1][1].currentText()))

                output.extend([bools[widget.isChecked()] for widget in self.deform_widgets[row][0] if isinstance(widget,QCheckBox)]) 

                self.errormsg.append(('def_rate', 'Missing deformation rate in deform number {}'.format(str(row-1)))) if not str(self.deform_widgets[row][0][3].text()) else output.append(float(self.deform_widgets[row][0][3].text()))

                if self.deform_widgets[row][1][2].isChecked():

                    for i, widget in enumerate(self.deform_widgets[row][1]):

                        if isinstance(widget, QLineEdit):
                            
                            if not str(widget.text()):

                                identifier = str(self.deform_widgets[row][1][i-1].text())

                                self.errormsg.append((identifier, 'Missing {} in deform number {}'.format(identifier, row-1)))

                                output.append(1)

                            else:

                                output.append(float(widget.text()))

                else:

                    if not times[2]:

                        times[2] = 1000 

                    output.extend([1,1, times[2] + 1])

            def_output = (['t', self.deform_num, *output, 'time', *times])

            self.output_list.append(("deform", def_output))

        else:

            self.output_list.append(("deform", ['f', 1, 'xx', 'f', 'f', 1, 1, 1, 1, 'time', 1, 1, 1]))

    def group(self, row):

        group_row = 0

        #Group Num command

        self.output_list.append(("group_num", [self.group_num, self.restart_num, (self.fixnum + self.restart_fix), (self.calnum+self.restart_cal)]))

        for i in range(0, self.group_num):

            fix = 0

            cal = 0

            lower_b = []

            upper_b = []

            ori = []

        #   Row one data

            if self.group_name_array[i][1].text() == '':

                group_name = 'group_' + str(i+1)

            else:

                group_name = str(self.group_name_array[i][1].text())

            style_cg = str(self.group_row_widgets[group_row][1].currentText())

            style_at = str(self.group_row_widgets[group_row][3].currentText())

            group_shape = str(self.group_row_widgets[group_row][5].currentText())

        #   Row two data

            if self.group_row_widgets[group_row + 1][0][0].isChecked():

                boolean_in = "f"

            else:

                boolean_in = "t"

            if self.group_row_widgets[group_row+1][0][2].isChecked():

                fix = 1
            
            if self.group_row_widgets[group_row+1][0][3].isChecked():

                cal = 1

        #   Group shape data 

            if group_shape == "Block":

                for j in range(1,4):

                    if self.group_row_widgets[group_row + 1][j][2].text() == '':

                        self.errormsg.append(('lower_b', 'Missing lower bound in '+ group_name))

                        lower_b.append(0)

                    else:

                        try:

                            lower_b.append(self.checkinf(str(self.group_row_widgets[group_row+1][j][2].text())))

                        except ValueError:

                            self.errormsg(('lower_b', 'Incorrect format for lower bound in ' + group_name))

                            lower_b.append(0)

                    if self.group_row_widgets[group_row+1][j][4].text() == '':

                        self.errormsg.append(('upper_b', 'Missing upper bound in ' + group_name))

                        upper_b.append(0)

                    else:

                        try:

                            upper_b.append(self.checkinf(str(self.group_row_widgets[group_row+1][j][4].text())))

                        except ValueError:

                            self.errormsg.append(('upper_b', 'Incorrect format for upper bound in ' + group_name))

                            upper_b.append(0)

                    ori.append(str(self.group_row_widgets[group_row+1][j][6].text()).split())

                    if ori[j-1] == '' or len(ori[j-1]) < 3:

                        ori[j-1] = [1, 1, 1]

                        self.errormsg.append(('ori', 'Error in orientation for group ' + group_name))

                    else:

                        for list in ori[j-1]:

                            list = [float(k) for k in list]

                group_axis = 1

                group_centroid = [0, 0, 0]

                group_radius_large = 10

                group_radius_small = 10



                self.output_list.append(("group", [group_name, style_cg.lower(), style_at.lower(), group_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                                  "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                                  ori[2][2], boolean_in, group_axis, 0, 0, 0, 10, 10]))

            elif group_shape == "Cylinder":

                lower_b = [0, 0, 0]

                upper_b = [0, 0, 0]

                ori = [[0, 0, 0], [0,0,0], [0,0,0]]

                group_centroid = [0, 0, 0]

                group_axis = int(self.group_row_widgets[group_row+1][1][1].currentText())

                if self.group_row_widgets[group_row+1][1][3].text() == '':

                    self.errormsg.append(('group_radius_large', 'Error in radius for group ' + group_name))

                    group_radius_large = 1

                else:

                    group_radius_large = float(self.group_row_widgets[group_row+1][1][3].text())

                group_radius_small = 1

                if self.group_row_widgets[group_row+1][2][2].text() == '':

                    self.errormsg.append(('lower_b', 'Missing lower bound for group ' + group_name))

                else:

                    try:

                        lower_b[group_axis] = self.checkinf(str(self.group_row_widgets[group_row+1][2][2].text()))

                    except ValueError:

                        self.errormsg.append(('lower_b', 'Error in lower bound value for group ' + group_name))

                if self.group_row_widgets[group_row+1][2][4].text() == '':

                    self.errormsg.append(('upper_b', 'Missing upper bound for group ' + group_name))

                else:

                    try:

                        upper_b[group_axis] = self.checkinf(self.group_row_widgets[group_row+1][2][4].text())

                    except ValueError:

                        self.errormsg.append(('upper_b', 'Error in upper bound value for group ' + group_name))

                ori[group_axis] = str(self.group_row_widgets[group_row+1][2][6].text()).split()

                if ori[group_axis] == '' or len(ori[group_axis]) != 3:

                    ori[group_axis] = [0,0,0]

                    self.errormsg.append(('ori', 'Error in orientation for group_axis for group ' + group_name))

                count = 2

                for k in range(1, 4):

                    if k != group_axis:

                        if self.group_row_widgets[group_row+1][3][count].text() == '':

                            self.errormsg.append(('group_centroid', 'Error in group centroid command for group ' + group_name))

                        else:

                            group_centroid[k-1] = float(self.group_row_widgets[group_row+1][3][count].text())

                        count = count + 2

                self.output_list.append(("group", [group_name, style_cg.lower(), style_at.lower(), group_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                  "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                  ori[2][2], boolean_in, group_axis, group_centroid[0], group_centroid[1], group_centroid[2], group_radius_large, group_radius_small]))

            elif group_shape == "Cone" or group_shape == "Tube":

                lower_b = [0, 0, 0]

                upper_b = [0, 0, 0]

                ori = [[0, 0, 0], [0,0,0], [0,0,0]]

                group_centroid = [0, 0, 0]

                group_axis = int(self.group_row_widgets[group_row+1][1][1].currentText())

                if self.group_row_widgets[group_row+1][1][3].text() == '':

                    self.errormsg.append(('group_radius_large', 'Missing large radius in group ' + group_name))

                    group_radius_large = 0

                else:

                    group_radius_large = float(self.group_row_widgets[group_row+1][1][3].text())

                if self.group_row_widgets[group_row+1][1][5].text() == '':

                    self.errormsg.append(('group_radius_small', 'Missing small radius in group ' + group_name))

                    group_radius_small = 0

                else:

                    group_radius_small = float(self.group_row_widgets[group_row+1][1][5].text())

                if self.group_row_widgets[group_row+1][2][2].text() == '':

                    self.errormsg.append(('lower_b', 'Missing lower bound for group ' + group_name))

                else:

                    try:

                        lower_b[group_axis] = self.checkinf(str(self.group_row_widgets[group_row+1][2][2].text()))

                    except ValueError:

                        self.errormsg.append(('lower_b', 'Error in lower bound value for group ' + group_name))

                if self.group_row_widgets[group_row+1][2][4].text() == '':

                    self.errormsg.append(('upper_b', 'Missing upper bound for group ' + group_name))

                else:

                    try:

                        upper_b[group_axis] = self.checkinf(self.group_row_widgets[group_row+1][2][4].text())

                    except ValueError:

                        self.errormsg.append(('upper_b', 'Error in upper bound value for group ' + group_name))

                ori[group_axis] = str(self.group_row_widgets[group_row+1][2][6].text()).split()

                if ori[group_axis] == '' or len(ori[group_axis]) != 3:

                    ori[group_axis] = [0,0,0]

                    self.errormsg.append(('ori', 'Error in orientation for group_axis for group ' + group_name))

                count = 1

                for k in range(1, 4):

                    if k != group_axis:

                        if self.group_row_widgets[group_row+1][3][count].text() == '':

                            self.errormsg.append(('group_centroid', 'Error in group centroid command for group ' + group_name))

                        else:

                            group_centroid[k-1] = float(self.group_row_widgets[group_row+1][3][count].text())

                        count = count + 1

                self.output_list.append(("group", [group_name, style_cg.lower(), style_at.lower(), group_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                  "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                  ori[2][2], boolean_in, group_axis, group_centroid[0], group_centroid[1], group_centroid[2], group_radius_large, group_radius_small]))

            elif group_shape == "Sphere":

                lower_b = [0, 0, 0]

                upper_b = [0, 0, 0]

                ori = [[0,0,0],[0,0,0],[0,0,0]]

                group_axis = 1

                if self.group_row_widgets[group_row+1][1][1].text() == '':

                    self.errormsg.append(('group_radius_large', 'Error in radius in group ' + group_name))

                    group_radius_large = 1

                else:

                    group_radius_large = float(self.group_row_widgets[group_row+1][1][1].text())

                group_radius_small = 1

                group_centroid = []

                counter = 0

                dirs = ['x', 'y', 'z']

                for k in [2, 4, 6]:

                    if self.group_row_widgets[group_row+1][2][k].text() == '':

                        self.errormsg.append(('group_centroid', 'Error in group centroid in ' + dirs[int(k/2)-1] + ' for group ' + group_name))

                        group_centroid.append([0, 0, 0])

                    else:

                        group_centroid.append(float(self.group_row_widgets[group_row+1][2][k].text()))


                self.output_list.append(("group", [group_name, style_cg.lower(), style_at.lower(), group_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                  "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                  ori[2][2], boolean_in, group_axis, group_centroid[0], group_centroid[1], group_centroid[2], group_radius_large, group_radius_small]))

            group_row = group_row + 2

            if fix == 1:

                self.fixpull(i, group_name)

            if cal == 1:

                self.calpull(i, group_name)

    def checkinf(self,val):

        #Returns either a string with inf or a number

        if val.strip() == "inf" or val.strip() == "Inf" or val.strip() == "INF":

            out = "inf"

        else:

            out = float(val)

        return out

    def fixpull(self, row, group_name):

        if self.fixWidgets[row][0][1].isChecked():

            boolean_def = "t"

        else:

            boolean_def = "f"

        if self.fixWidgets[row][0][2].isChecked():

            boolean_release = "t"

        else:

            boolean_release = "f"

        assign_style = str(self.fixWidgets[row][1][1].currentText())


        if assign_style == "Force":

            assign_style = "force"

            disp_limit = 0

        elif assign_style == "Displacement":

            assign_style = "disp"

            disp_limit = float(self.fixWidgets[row][1][5].text())

            if disp_limit == '': 

                disp_limit = 1

                self.errormsg.append(('disp_limit', 'Missing displacement in fix command for group ' + group_name))

        assign_vector = str(self.fixWidgets[row][1][3].text()).split()

        if assign_vector == '' or len(assign_vector) != 3:

            assign_vector = [1, 1, 1]

            self.errormsg.append(('assign_vector', 'Incorrect format for applied vector in fix command for group ' + group_name))

        if str(self.fixWidgets[row][2][1].text()) == '':

            start_time = 0

            self.errormsg.append(('start_time', 'Missing entry for start time in fix command for group ' + group_name))

        else:

            start_time = int(self.fixWidgets[row][2][1].text())

        if self.fixWidgets[row][2][3].text() == '':

            end_time = 0

            self.errormsg.append(('end_time', 'Missing entry for end time in fix command for group ' + group_name))

        else:

            end_time = int(self.fixWidgets[row][2][3].text())

        if self.fixWidgets[row][3][0].isChecked():

            boolean_grad = "t"

            grad_ref_axis = int(self.fixWidgets[row][3][2].currentText())

            grad_assign_axis = int(self.fixWidgets[row][3][4].currentText())

            grad_lower_b = str(self.fixWidgets[row][4][1].text())

            grad_upper_b = str(self.fixWidgets[row][4][3].text())

        else:

            boolean_grad = "f"

            grad_ref_axis = 1

            grad_assign_axis = 1

            grad_lower_b = 1

            grad_upper_b = 1

        self.output_list.append(("fix", [group_name, boolean_release, boolean_def, assign_style, assign_vector[0], assign_vector[1], assign_vector[2],
                                 disp_limit, 'time', start_time, end_time, boolean_grad, grad_ref_axis, grad_assign_axis, grad_lower_b, grad_upper_b]))

    def calpull(self, row, group_name):

        cal_variable = str(self.calWidgets[row][0][1].currentText()).lower()

        self.output_list.append(("cal", [group_name, cal_variable]))

    def getFileName(self, option):

        if option == 1:

            self.outpath,throwaway = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), 'Directory')

            if self.outpath:

                self.input_obj_list[self.outputrow][1].setText(self.outpath)

            else:

                self.input_obj_list[self.outputrow][1].setText('No file selected')

        if option == 2:

            self.restart_path,throwaway = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "Restart files (*.restart)")

            if self.restart_path:

                self.restart_widgets[0][2].setText(self.restart_path)

            else:

                self.restart_widgets[0][2].setText('No file selected')

        if option == 3:

            self.potential_path = QFileDialog.getExistingDirectory(self, 'Directory', os.getcwd())

            if self.potential_path:

                self.input_obj_list[self.potential_num][3].setText(self.potential_path)

            else:

                self.input_obj_list[self.potential_num][3].setText('No file selected')

        if option == 4:

            button = self.sender()

            row = int(button.objectName())

            self.add_atom_paths[row], throwaway = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Lammps dump file (*)')

            if self.add_atom_paths[row]:

                self.modify_row_widget[row][2][1][1].setText(self.add_atom_paths[row])

            else:

                self.modify_row_widget[row][2][1][1].setText('No file selected')

        if option == 5:

            if self.restart_path:
              path=os.path.dirname(self.restart_path)
            else:
              path=os.getcwd()

            self.restart_groups, throwaway = QFileDialog.getOpenFileNames(self, 'Open files', path, "Restart Group Files (*.id)")

            if self.restart_groups:

                text = ''.join([(os.path.basename(filepath)+ ' | ') for filepath in self.restart_groups])

                self.restart_widgets[1][2].setText('')

                self.restart_group_method(-1)

                self.restart_group_method(0)

        if option == 20: 

            self.refine_groups, throwaway = QFileDialog.getOpenFileNames(self, 'Open files', os.getcwd(), "Restart Group Files (*.id)")

            if self.refine_groups:

                text = ''.join([(os.path.basename(filepath) + ' | ') for filepath in self.refine_groups])

                self.restart_widgets[2][3].setText(text)

            else:

                self.restart_widgets[2][3].setText('No refine groups selected')

    def centroidlabels(self, groupormodify): 

        box = self.sender()

        row = int(box.objectName())

        dirs = ['1', '2', '3']

        if groupormodify == 1:

            count = 1

            for direction in dirs:

                if direction != box.currentText():

                    self.group_row_widgets[row][3][count].setText(direction)

                    count = count + 2

        elif groupormodify == 2:

            count = 1

            for direction in dirs:

                if direction != box.currentText():

                    self.modify_row_widget[row][2][4][count].setText(direction)

                    count = count + 2


    def backButton(self):

        self.backSignal.emit()

    def refreshFields(self):

        for i, label in enumerate(self.label_list):

            if label.text() == 'Create Project Folder':

                self.input_obj_list[i][1].setText('No file selected')

                self.outpath = ''

            elif label.text() == 'Restart Options:':

                self.restart_widgets[0][0].setChecked(False)

            elif label.text() == 'Simulator':

                [self.sim_options[i].setChecked(False)]

            elif label.text() == 'Mass:':

                self.input_obj_list[i].setText('')

            elif label.text() == 'Group:':

                while self.group_num > 0:

                    self.minusGroup(self.groupRow)

            elif label.text() == 'Element:':

                [self.input_obj_list[i][j].setChecked(True) for j in [0,3]]

            elif label.text() == 'Limits:' or label.text() == 'Neighbor:' or label.text() == 'Run:':

                [self.input_obj_list[i][j].setText('') for j in [1,3]]

            elif label.text() == 'Box Direction (format is i j k):':

                [self.input_obj_list[i][j].setText('') for j in [1, 3, 5]]

            elif label.text() == 'Deform:':

                self.deform_widgets[0][0].setChecked(False)   

            elif label.text() == 'Convert:':

                self.input_obj_list[i][1].setText('')

            elif label.text() == 'Potential:':

                [self.input_obj_list[i][j].setChecked(False) for j in [0,1]]

                self.potential_path = ''

            elif label.text() == 'Constrain:':

                self.input_obj_list[i].setChecked(False)

            elif label.text() == 'Dump:':

                [self.input_obj_list[i][j].setText('') for j in [1,3,5,7]] 

            self.input_obj_list[self.outputrow][1].setText('No file selected')

            self.input_obj_list[self.potential_num][3].setText('No file selected')


    def clearLayout(self, layout):

        while layout.count() > 0:

            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()