from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

#This file contains all of the functions necessary for the input script handling

class InputWidget(QWidget):

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

        super(InputWidget, self).__init__()

        InputWidget.window(self)

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

    #       Simulator Options

        sim_lays = QVBoxLayout()

        sim_widget = QWidget()

        self.simulator_layout[1].setAlignment(Qt.AlignLeft)

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

        [sim_lays.addLayout(layout) for layout in self.simulator_layout]

        sim_widget.setLayout(sim_lays)

        self.sub_layout_list[rowcount].addWidget(sim_widget)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount+1

    #       Boundary Options
        
        self.label_list.append(QLabel("Boundary:"))

        self.sub_layout_list.append(QHBoxLayout())

        self.input_obj_list.append([QCheckBox("Shrink-Wrap (x)"), QCheckBox("Shrink-Wrap (y)"), QCheckBox("Shrink-Wrap (z)")])

        for i in range(0,3):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount+1

    #       ZigZag Options
        
        self.label_list.append(QLabel("ZigZag boundaries:"))

        self.sub_layout_list.append(QHBoxLayout())

        zigzagbox = [QCheckBox() for i in range(0,3)]

        self.input_obj_list.append(zigzagbox)

        for i in range(0,3):

            self.input_obj_list[rowcount][i].setText(dir_list[i])

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount+1

    #       Lattice Options

        self.label_list.append(QLabel("Lattice:"))

        self.input_obj_list.append([QLabel("Chemical Element"), QLineEdit(), QComboBox(), QLabel("Lattice Parameter"), QLineEdit()])

        self.input_obj_list[rowcount][2].addItems(["FCC","BCC"])

        self.input_obj_list[rowcount][4].setValidator(self.validateposdouble)

        self.sub_layout_list.append(QHBoxLayout())

        for i in range(0,5):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

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

    #       Grain Direction

        self.sub_layout_list.append(QHBoxLayout())

        self.label_list.append(QLabel("Grain Stack Direction:"))

        self.input_obj_list.append([QLabel("Direction:"), QComboBox(), QLabel("Overlap:"), QLineEdit()])

        self.input_obj_list[rowcount][1].addItems(["  1  ", "  2  ", "  3  "])

        self.input_obj_list[rowcount][1].setCurrentIndex(2)

        self.input_obj_list[rowcount][3].setValidator(self.validatedouble)

        self.input_obj_list[rowcount][3].setPlaceholderText('0')

        for i in range(0, 4):

            self.sub_layout_list[rowcount].addWidget(self.input_obj_list[rowcount][i])

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

    #       Grains

        self.sub_layout_list.append(QVBoxLayout())

        grain_lay = []

        grain_lay.append(QHBoxLayout())    

        self.grain_num = 0

        self.grainrow = rowcount

        self.label_list.append(QLabel("Grain:"))

        grain_buttons = [QPushButton("+"), QPushButton("-")]

        self.grain_widget = [QLabel(str(self.grain_num)), grain_buttons[0], grain_buttons[1]]

        grain_buttons[0].clicked.connect(lambda: self.plusGrain(self.grainrow))

        grain_buttons[1].clicked.connect(lambda: self.minusGrain(self.grainrow))

        self.input_obj_list.append(self.grain_widget)

        for i in range(0,3):

            grain_lay[self.grain_num].addWidget(self.input_obj_list[rowcount][i])

        self.sub_layout_list[rowcount].addLayout(grain_lay[self.grain_num])

        self.sub_layout_list[self.grainrow].addLayout(self.grain_layout)

        fbox.addRow(self.label_list[rowcount], self.sub_layout_list[rowcount])

        rowcount = rowcount + 1

        self.plusGrain(self.grainrow)

        self.plusSub(0)

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

    #       Modify

        self.sub_layout_list.append(QVBoxLayout())

        modify_lay = QHBoxLayout()

        self.add_atom_paths = []

        self.modify_num = 0

        modify_row = rowcount

        self.label_list.append(QLabel("Modify:"))

        modify_buttons = [QPushButton("+"), QPushButton("-")]

        self.modify_widget = [QLabel(str(self.modify_num)), modify_buttons[0], modify_buttons[1]]

        modify_buttons[0].clicked.connect(lambda: self.plusModify())

        modify_buttons[1].clicked.connect(lambda: self.minusModify())

        self.input_obj_list.append(self.modify_widget)

        for i in range(0,3):

            modify_lay.addWidget(self.input_obj_list[rowcount][i])

        self.sub_layout_list[rowcount].addLayout(modify_lay)

        self.sub_layout_list[rowcount].addLayout(self.modify_layout)

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

        button = self.sender()

        if button.isChecked():

            #Restart row one

            self.restart_widgets[0].extend([QPushButton("Browse"), QLabel("No File Selected")])

            self.restart_widgets[0][1].clicked.connect(lambda: self.getFileName(2))

            self.restart_widgets[0][1].setFixedWidth(self.browse_width)

            for i in range(1,3):

                self.restart_layout[0].addWidget(self.restart_widgets[0][i])

            #Restart row two

            self.restart_widgets.append([QLabel("Number of Restart Groups:"), QLineEdit()])

            self.restart_widgets[1][1].setValidator(self.validateposint)

            for i in range(0,2):

                self.restart_layout[1].addWidget(self.restart_widgets[1][i])

            #Restart row three

            self.restart_widgets.append([QCheckBox("Refine")])

            self.restart_widgets[2][0].toggled.connect(lambda: self.refine_options(row))

            self.restart_layout[2].addWidget(self.restart_widgets[2][0])

        else:

            while self.restart_layout[0].count() > 1:

                item = self.restart_layout[0].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.restart_widgets[0][1]

            for i in range(1, 3):

                while self.restart_layout[i].count():

                    item = self.restart_layout[i].takeAt(0)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                del self.restart_widgets[1]

    def refine_options(self, row):

        button = self.sender()

        if button.isChecked():

            self.restart_widgets[2].append(QComboBox())

            self.restart_widgets[2][1].addItems(["All", "Group"])

            self.restart_layout[2].addWidget(self.restart_widgets[2][1])

            self.restart_widgets[2][1].currentIndexChanged.connect(lambda: self.refine_box(1))

            self.refine_box(0)

        else:

            while self.restart_layout[2].count() > 1:

                item = self.restart_layout[2].takeAt(1)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.restart_widgets[2][1]

    def refine_box(self, butsend):

        if butsend == 0:

            option = "All"

        elif butsend == 1:

            box = self.sender()

            option = box.currentText()

        if option == "All":

            if butsend == 1:

                while self.restart_layout[2].count() > 2:

                    item = self.restart_layout[2].takeAt(2)

                    widget = item.widget()

                    if widget is not None:

                        widget.deleteLater()

                    del self.restart_widgets[2][2]

            self.restart_widgets[2].extend([QLabel("Unit Type:"), QLineEdit()])

            self.restart_widgets[2][3].setValidator(self.validateposint)

            for i in range(2,4):

                self.restart_layout[2].addWidget(self.restart_widgets[2][i])

        elif option == "Group":

            while self.restart_layout[2].count() > 2:

                item = self.restart_layout[2].takeAt(2)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

                del self.restart_widgets[2][2]

            self.restart_widgets[2].extend([QLabel("Groups:"), QLineEdit()])

            self.restart_widgets[2][3].setPlaceholderText("Format: Group_1 Group_2 ... Group_3")

            for i in range(2,4):

                self.restart_layout[2].addWidget(self.restart_widgets[2][i])

    def plusGrain(self, grain_layout_row):

        self.grain_num = self.grain_num + 1

        self.grain_widget[0].setText(str(self.grain_num))

        self.add_grain_row(grain_layout_row)

    def minusGrain(self, grain_layout_row):

        if self.grain_num > 0:

            self.grain_num = self.grain_num - 1

            self.grain_widget[0].setText(str(self.grain_num))

            self.remove_grain_row(grain_layout_row)

    def add_grain_row(self, grain_layout_row):

        #       Row one
        
        self.sub_grain_layout.append(QHBoxLayout())

        self.grain_row_widget.append(QLabel("Grain ID: " + str(self.grain_num)))

        self.sub_grain_layout[self.grain_row].addWidget(self.grain_row_widget[self.grain_row])

        #       Row two

        self.sub_grain_layout.append(QHBoxLayout())

        self.sub_grain_layout[self.grain_row+1].addItem(QSpacerItem(40,20))

        self.grain_row_widget.append([QLabel("Grain Orientation:"), QLineEdit(), QLineEdit(), QLineEdit()])

        self.grain_row_widget[self.grain_row+1][1].setPlaceholderText("x-direction (i j k)")

        self.grain_row_widget[self.grain_row+1][2].setPlaceholderText("y-direction (i j k)")

        self.grain_row_widget[self.grain_row+1][3].setPlaceholderText("z-direction (i j k)")

        for i in range(0,4):

            self.sub_grain_layout[self.grain_row+1].addWidget(self.grain_row_widget[self.grain_row+1][i])

        #       Row three 

        self.sub_grain_layout.append(QHBoxLayout()) 

        self.sub_grain_layout[self.grain_row+2].addItem(QSpacerItem(40,20))

        self.grain_row_widget.append([QLabel("Grain Movement in x: "), QLineEdit(), QLabel("Grain Movement in y:"), QLineEdit(), QLabel("Grain Movement in z:"), QLineEdit()])

        self.grain_row_widget[self.grain_row+2][1].setPlaceholderText("0")

        self.grain_row_widget[self.grain_row+2][1].setValidator(self.validatedouble)
        
        self.grain_row_widget[self.grain_row+2][3].setPlaceholderText("0")

        self.grain_row_widget[self.grain_row+2][3].setValidator(self.validatedouble)

        self.grain_row_widget[self.grain_row+2][5].setPlaceholderText("0")

        self.grain_row_widget[self.grain_row+2][5].setValidator(self.validatedouble)

        for i in range(0,6):

            self.sub_grain_layout[self.grain_row+2].addWidget(self.grain_row_widget[self.grain_row+2][i])

        #       Subdomain information Row four

        self.sub_grain_layout.append(QVBoxLayout())

        self.subdomain_layout.append([QHBoxLayout()])

        self.subdomain_num.append(0)

        self.subdomain_row.append(1)

        self.subdomain_sub_widgets.append([])

        self.subdomain_widget.append([QLabel("Subdomain: "), QLabel(str(self.subdomain_num[self.grain_num-1])), QPushButton("+"), QPushButton("-")])        

        self.grain_row_widget.append(self.subdomain_widget[self.grain_num-1])

        #   Set names for buttons which are used to add forms in the correct regions       

        for i in range(2,4):

            self.subdomain_widget[self.grain_num-1][i].setObjectName(str(self.grain_num))

        self.subdomain_widget[self.grain_num-1][2].clicked.connect(lambda: self.plusSub(1))

        self.subdomain_widget[self.grain_num-1][3].clicked.connect(lambda: self.minusSub(1))

        self.subdomain_layout[self.grain_num-1][0].addItem(QSpacerItem(40,20))

        for i in range(0,4):

            self.subdomain_layout[self.grain_num-1][0].addWidget(self.subdomain_widget[self.grain_num-1][i])

        self.sub_grain_layout[self.grain_row+3].addLayout(self.subdomain_layout[self.grain_num-1][0])

        #       Group    

        for i in range(self.grain_row, self.grain_row + 4):

            self.grain_layout.addLayout(self.sub_grain_layout[i])

        self.grain_row = self.grain_row + 4

    def remove_grain_row(self, grain_layout_row):

        #           Remove widgets for grain
            for i in range(self.grain_row-4, self.grain_row-1):

                if self.sub_grain_layout[i] is not None:

                    while self.sub_grain_layout[i].count():

                        item = self.sub_grain_layout[i].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

        #           Remove widgets for subdomain        

            if self.subdomain_layout[self.grain_num][0] is not None:

                while self.subdomain_layout[self.grain_num][0].count():

                        item = self.subdomain_layout[self.grain_num][0].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

        #           Remove sub_domain layout from sub_grain layout

            for i in range(1,self.subdomain_num[self.grain_num]+1):

                self.minusSub(grain_num = self.grain_num)

            self.sub_grain_layout[self.grain_row-1].removeItem(self.subdomain_layout[self.grain_num][0])

        #           Remove sub_grain_layout

            for j in range(self.grain_row-4, self.grain_row):

                for i in range(self.grain_layout.count()):

                    layout_item = self.grain_layout.itemAt(i)

                    if layout_item is not None:

                        if layout_item.layout() == self.sub_grain_layout[j]:

                            self.grain_layout.removeItem(layout_item)

        #           Remove from layout lists

            for i in range(self.grain_row -4, self.grain_row):   

                del self.grain_row_widget[self.grain_row-4]

            self.grain_row = self.grain_row - 4

            del self.subdomain_widget[self.grain_num]

    def plusSub(self, butsend, grain = 1):

        if butsend == 1:

            button = self.sender()

            button_num = int(button.objectName())

        else:

            button_num = grain

        self.subdomain_num[button_num-1] = self.subdomain_num[button_num-1] + 1

        self.subdomain_widget[button_num-1][1].setText(str(self.subdomain_num[button_num-1]))

        self.addSubRow(button_num-1)

    def addSubRow(self, subdomain_num):

        self.subdomain_sub_widgets[subdomain_num].append([QLabel("Subdomain ID: %s" % str(self.subdomain_num[subdomain_num])), QLabel("Units in x:"), QLineEdit(), QLabel("Units in y:"), QLineEdit(), QLabel("Units in z:"), QLineEdit(),
            QLabel("Unit Type:"), QLineEdit()])

        self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][2].setValidator(self.validateposint)

        self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][4].setValidator(self.validateposint)

        self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][6].setValidator(self.validateposint)

        self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][8].setValidator(self.validateposint)

        #       Row one
        
        self.subdomain_layout[subdomain_num].append(QHBoxLayout())

        self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]].addItem(QSpacerItem(40,20))

        self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]].addWidget(self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][0])

        #            Row two

        self.subdomain_layout[subdomain_num].append(QHBoxLayout())

        self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]+1].addItem(QSpacerItem(80,20))

        for i in range(1, 7):

            self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]+1].addWidget(self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][i])

        #       Row Three

        self.subdomain_layout[subdomain_num].append(QHBoxLayout())

        self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]+2].addItem(QSpacerItem(80,20))

        for i in range(7,9):

            self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num] + 2].addWidget(self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]-1][i])

        #       Add to window

        #Calculate index 

        grain_index = subdomain_num * 4 + 3

        for i in range(0,3):

            self.sub_grain_layout[grain_index].addLayout(self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num] + i])

        self.subdomain_row[subdomain_num] = self.subdomain_row[subdomain_num] + 3

    def minusSub(self, *args, **kwargs):

        if ('grain_num' in kwargs):

            button_num = kwargs['grain_num'] + 1

        else :

            button = self.sender()

            button_num = int(button.objectName())

        if (self.subdomain_num[button_num - 1] > 0):

            self.subdomain_num[button_num-1] = self.subdomain_num[button_num-1] - 1

            self.subdomain_widget[button_num-1][1].setText(str(self.subdomain_num[button_num-1]))

            self.removeSubRow(button_num -1)

    def removeSubRow(self, subdomain_num):

        #       Remove Widgets for Subdomains

        for i in range(self.subdomain_row[subdomain_num] -3, self.subdomain_row[subdomain_num]):

            if self.subdomain_layout[subdomain_num][i] is not None:

                while self.subdomain_layout[subdomain_num][i].count():

                        item = self.subdomain_layout[subdomain_num][i].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

        grain_index = subdomain_num * 4 + 3

        #       Remove all the Subdomain layouts

        for j in range(self.subdomain_row[subdomain_num]-3, self.subdomain_row[subdomain_num]):

            for i in range(self.sub_grain_layout[grain_index].count()):

                layout_item = self.sub_grain_layout[grain_index].itemAt(i)

                if layout_item is not None:

                    if layout_item.layout() == self.subdomain_layout[subdomain_num][j]:

                        self.sub_grain_layout[grain_index].removeItem(layout_item)

        #       Delete from arrays

        del self.subdomain_sub_widgets[subdomain_num][self.subdomain_num[subdomain_num]]

        for i in range(0,3):

            del self.subdomain_layout[subdomain_num][self.subdomain_row[subdomain_num]-3]

        self.subdomain_row[subdomain_num] = self.subdomain_row[subdomain_num] - 3

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

        self.sim_num = self.sim_num + 1
    
    def hybridOptions(self,row):

        #       Clear widgets

        for i in range(1,4):

            while self.simulator_layout[i].count():

                        item = self.simulator_layout[i].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

            if i -1 < len(self.simulator):         

                for j in range(0, len(self.simulator)):

                    del self.simulator[0]

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

            for i in range(0, len(self.fixWidgets[row][0])):

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

    #   Modify methods

    def plusModify(self):

        self.sub_modify_layout.append([])

        self.modify_row_widget.append([])

        self.modify_options_butngroup.append(QButtonGroup())

        self.modify_num = self.modify_num + 1

        self.modify_widget[0].setText(str(self.modify_num))

        self.add_modify_row()

    def add_modify_row(self):

        #       Row 1

        self.sub_modify_layout[self.modify_num - 1].append(QHBoxLayout())

        self.modify_row_widget[self.modify_num-1].append([QLabel("Modify Name:"), QLineEdit()])

        self.modify_row_widget[self.modify_num-1][0][1].setPlaceholderText('modify_' + str(self.modify_num))

        for i in range(0, 2):

            self.sub_modify_layout[self.modify_num -1][0].addWidget(self.modify_row_widget[self.modify_num-1][0][i])

        #       Row 2

        self.add_atom_paths.append('')

        self.sub_modify_layout[self.modify_num-1].append(QHBoxLayout())

        self.modify_row_widget[self.modify_num-1].append([QRadioButton("Delete"), QRadioButton("CG to Atom"), QRadioButton("Dislocation"), QRadioButton("Cutoff"), QRadioButton("Add Atom")])

        for i in range(0, len(self.modify_row_widget[self.modify_num-1][1])):

            self.modify_options_butngroup[self.modify_num-1].addButton(self.modify_row_widget[self.modify_num-1][1][i])

            self.modify_row_widget[self.modify_num-1][1][i].setObjectName(str(self.modify_num-1))

            self.modify_row_widget[self.modify_num-1][1][i].toggled.connect(lambda: self.modify_options())


        for i in range(0, len(self.modify_row_widget[self.modify_num-1][1])):
         
            self.sub_modify_layout[self.modify_num-1][1].addWidget(self.modify_row_widget[self.modify_num-1][1][i])

        #       Row 3

        self.sub_modify_layout[self.modify_num-1].append(QVBoxLayout())

        self.modify_row_widget[self.modify_num-1].append([])

        self.modify_options_layout.append([])

        for i in range(0, len(self.sub_modify_layout[self.modify_num-1])):

            self.modify_layout.addLayout(self.sub_modify_layout[self.modify_num-1][i])

    def modify_options(self):

        button = self.sender()

        #       Add fields for each option

        if button.isChecked():

            self.modify_flag = 1

            row = int(button.objectName())

            option = button.text()

        #           Clear existing widgets

            if self.modify_flag == 1:

             #    Clear Widgets

                for i in range(0, len(self.modify_options_layout[row])):
                
                    while self.modify_options_layout[row][0].count():

                        item = self.modify_options_layout[row][0].takeAt(0)

                        widget = item.widget()

                        if widget is not None:

                            widget.deleteLater()

                    self.sub_modify_layout[row][2].removeItem(self.modify_options_layout[row][0])

                    del self.modify_options_layout[row][0]

                    for i in range(0, len(self.modify_row_widget[row][2])):

                       del self.modify_row_widget[row][2][0]
 
           
            if option == "Delete":

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QCheckBox("Delete outside shape"), QCheckBox("Fill around shape")])

                for i in range(0,2):

                    self.modify_options_layout[row][0].addWidget(self.modify_row_widget[row][2][0][i])

                self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][0])

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("Modify Shape:"), QComboBox()])

                self.modify_row_widget[row][2][1][1].addItems(["Block", "Cylinder", "Cone", "Tube", "Sphere"])

                self.modify_row_widget[row][2][1][1].currentIndexChanged.connect(lambda: self.modifyShape(row)) 

                for i in range(0,2):

                    self.modify_options_layout[row][1].addWidget(self.modify_row_widget[row][2][1][i])

                self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][1]) 

                self.modifyShape(row,1)       

            elif option =="CG to Atom":

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QCheckBox("Refine outside shape")])

                self.modify_options_layout[row][0].addWidget(self.modify_row_widget[row][2][0][0])

                self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][0])

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("Modify Shape:"), QComboBox()])

                self.modify_row_widget[row][2][1][1].addItems(["Block", "Cylinder", "Cone", "Tube", "Sphere"])

                self.modify_row_widget[row][2][1][1].currentIndexChanged.connect(lambda: self.modifyShape(row)) 

                for i in range(0,2):

                    self.modify_options_layout[row][1].addWidget(self.modify_row_widget[row][2][1][i])

                self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][1]) 

                self.modifyShape(row,1)       

            elif option == "Dislocation":

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("Centroid Location (x y z)"), QLineEdit(), QLabel("Line Axis"), QComboBox(), QLabel("Plane Axis"), QComboBox()])

                self.modify_row_widget[row][2][0][3].addItems(["1", "2", "3"])

                self.modify_row_widget[row][2][0][5].addItems(["1", "2", "3"])

                for i in range(0, len(self.modify_row_widget[row][2][0])):

                    self.modify_options_layout[row][0].addWidget(self.modify_row_widget[row][2][0][i])

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("Character Angle:"), QLineEdit(), QLabel("Poisson Ratio"), QLineEdit()])

                self.modify_row_widget[row][2][1][1].setValidator(self.validateposdouble)

                self.modify_row_widget[row][2][1][3].setValidator(self.validateposdouble)

                for i in range(0, len(self.modify_row_widget[row][2][1])):

                    self.modify_options_layout[row][1].addWidget(self.modify_row_widget[row][2][1][i])

                for i in range(0, len(self.modify_options_layout[row])):

                    self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][i])

            elif option == "Cutoff":

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("Depth"), QLineEdit(), QLabel("Delete Distance"), QLineEdit()])

                self.modify_row_widget[row][2][0][1].setValidator(self.validateposdouble)
                
                self.modify_row_widget[row][2][0][3].setValidator(self.validateposdouble)

                for i in range(0, 4):

                    self.modify_options_layout[row][0].addWidget(self.modify_row_widget[row][2][0][i])

                self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][0])

            elif option == "Add Atom":

                modify_num = button.objectName()

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_row_widget[row][2].append([QLabel("x-Displacement"), QLineEdit(), QLabel("y-Displacement"), QLineEdit(), QLabel("z-Displacement"), QLineEdit()])

                for i in range(0,6):

                    self.modify_options_layout[row][0].addWidget(self.modify_row_widget[row][2][0][i])

                self.modify_options_layout[row].append(QHBoxLayout())

                self.modify_options_layout[row][1].setAlignment(Qt.AlignLeft)

                self.modify_row_widget[row][2].append([QPushButton('Browse'), QLabel('No file selected')])

                self.modify_row_widget[row][2][1][0].setObjectName(modify_num)

                self.modify_row_widget[row][2][1][0].clicked.connect(lambda: self.getFileName(4))

                [self.modify_options_layout[row][1].addWidget(widget) for widget in self.modify_row_widget[row][2][1]]

                [self.sub_modify_layout[row][2].addLayout(layout) for layout in self.modify_options_layout[row]]

    def modifyShape(self, row, init=0):

        if init == 1:

            option = "Block"

        else:

        #       Pull selected box

            button = self.sender()

            option = button.currentText()

        #       Clear information from previous widgets

        for i in range(2, len(self.modify_options_layout[row])):

            while self.modify_options_layout[row][2].count():

                item = self.modify_options_layout[row][2].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            self.sub_modify_layout[row][2].removeItem(self.modify_options_layout[row][2])

            del self.modify_options_layout[row][2]

        for i in range(2,len(self.modify_row_widget[row][2])):

            del self.modify_row_widget[row][2][2]

        #       If statements to select the correct options for row shape

        if option == "Block":

        #       Row 2

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("x:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            for i in range(0,7):

                self.modify_options_layout[row][2].addWidget(self.modify_row_widget[row][2][2][i])


            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][2])

        #       Row 3

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("y:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            for i in range(0,7):

                self.modify_options_layout[row][3].addWidget(self.modify_row_widget[row][2][3][i])


            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][3])

        #       Row 4

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("z:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            for i in range(0,7):

                self.modify_options_layout[row][4].addWidget(self.modify_row_widget[row][2][4][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][4])

        elif option == "Cylinder" or option == "Tube" or option == "Cone":

        #           Row 2

            self.modify_options_layout[row].append(QHBoxLayout())

        #           Cylinder, tube, and cone have similar options. the only difference are the radii options.

            if option == "Cylinder":

                self.modify_row_widget[row][2].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Radius"), QLineEdit()])

            elif option == "Tube":

                self.modify_row_widget[row][2].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Outer Radius"), QLineEdit(), QLabel("Inner Radius"), QLineEdit()])

            elif option == "Cone":

                self.modify_row_widget[row][2].append([QLabel("Group Axis Direction"), QComboBox(), QLabel("Large Radius"), QLineEdit(), QLabel("Small Radius"), QLineEdit()])

            self.modify_row_widget[row][2][2][1].addItems(["1", "2", "3"])

            self.modify_row_widget[row][2][2][1].setObjectName(str(row))

            self.modify_row_widget[row][2][2][1].currentIndexChanged.connect(lambda: self.centroidlabels(2))

            for i in range(0,len(self.modify_row_widget[row][2][2])):

                self.modify_options_layout[row][2].addWidget(self.modify_row_widget[row][2][2][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][2])

        #           Row 3

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("Group Axis:"), QLabel("Lower bound"), QLineEdit(), QLabel("Upper bound"), QLineEdit(), QLabel("Orientation"), QLineEdit()])

            for i in range(0,7):

                self.modify_options_layout[row][3].addWidget(self.modify_row_widget[row][2][3][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][3])

        #           Row 4

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("Centroid in non group axis directions:"), QLabel('2'), QLineEdit(), QLabel('3'), QLineEdit()])

            for i in range(0,5):

                self.modify_options_layout[row][4].addWidget(self.modify_row_widget[row][2][4][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][4])

        elif option == "Sphere":

        #          Row 1

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("Radius"), QLineEdit()])

            for i in range(0,len(self.modify_row_widget[row][2][2])):

                self.modify_options_layout[row][2].addWidget(self.modify_row_widget[row][2][2][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][2])

        #           Row 2

            self.modify_options_layout[row].append(QHBoxLayout())

            self.modify_row_widget[row][2].append([QLabel("Centroid:"), QLabel("x"), QLineEdit(), QLabel("y"), QLineEdit(), QLabel("z"), QLineEdit()])

            for i in range(0,7):

                self.modify_options_layout[row][3].addWidget(self.modify_row_widget[row][2][3][i])

            self.sub_modify_layout[row][2].addLayout(self.modify_options_layout[row][3])

    def minusModify(self):

        if self.modify_num > 0:

            self.modify_num = self.modify_num - 1

            self.modify_widget[0].setText(str(self.modify_num))

            self.remove_modify_row()

    def remove_modify_row(self):

        #       Clear option widgets

        row = self.modify_num 

        for i in range(0, len(self.modify_options_layout[row])):

            while self.modify_options_layout[row][0].count():

                item = self.modify_options_layout[row][0].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            self.sub_modify_layout[row][2].removeItem(self.modify_options_layout[row][0])

            del self.modify_options_layout[row][0]

        for i in range(0, len(self.sub_modify_layout[row])):

            while self.sub_modify_layout[row][0].count():

                item = self.sub_modify_layout[row][0].takeAt(0)

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            self.modify_layout.removeItem(self.sub_modify_layout[row][0])

            del self.sub_modify_layout[row][0]

        for i in range(0,len(self.modify_row_widget[row])):

            del self.modify_row_widget[row][0]

    def defoptions(self, row) :

        button = self.sender()

        if button.isChecked():

            self.deform_num = 0

            self.deform_widgets[0].extend([QLabel('Start Timestep'), QLineEdit(), QLabel('End Timestep'), QLineEdit(), QLabel('Hold Strain at Step:'), QLineEdit()])

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

        self.output_list.append(('refine', ['all','1','6']))

        for i in range(0,len(labels)):

            label = labels[i].text()

            if label == "Restart Options:":

                self.restart_pull(i)

            elif label == "Simulator:":

                self.Simulator(i)

            elif label == "Boundary:":

                self.Boundary(i)

            elif label == "ZigZag boundaries:":

                self.zigzag(i)

            elif label == "Lattice:":

                self.lattice(i)

            elif label == "Mass:":

                if str(self.input_obj_list[i].text()) == '':

                    self.errormsg.append(('Mass', 'Mass is missing')) 

                else:

                    self.output_list.append(("mass", [float(self.input_obj_list[i].text())]))

            elif label == "Grain Stack Direction:":       

                stack_direction = int(self.input_obj_list[i][1].currentText())

                if str(self.input_obj_list[i][3].text()) == '':

                    overlap = 0

                else:

                    overlap = float(self.input_obj_list[i][3].text())

                self.output_list.append(("grain_dir", [stack_direction, overlap]))

            elif label == "Grain:": 

                self.grain(i) 

                self.subdomain(i) 

            elif label == "Group:":

                self.group(i)

            elif label == "Modify:":

                self.modify(i)

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

        self.FilePaths = [self.restart_path, self.outpath, self.potential_path]

        self.submitSignal.emit()

    def restart_pull(self, index):

        if self.restart_widgets[0][0].isChecked():

            boolean_restart = "t"

            if self.restart_widgets[1][1].text() == '':

                self.restart_num = 0

                self.errormsg.append(('restart_num','Missing number of restart groups in Restart Options Command'))

            else:

                self.restart_num = int(self.restart_widgets[1][1].text())

            if self.restart_widgets[2][0].isChecked():

                boolean_restart_refine = "t"

                refine_style = str(self.restart_widgets[2][1].currentText()).lower()

                if self.restart_widgets[2][3].text() == '':

                    if refine_style == 'all':

                        self.errormsg.append(('unitype', 'Missing Unit Type in Restart Options command'))

                    elif refine_style == 'group':

                        self.errormsg.append(('group_number', 'Missing Groups in Restart Options command'))

                    refine_vals = 0

                else:

                    refine_vals = str(self.restart_widgets[2][3].text())

                if refine_style == "all":

                    unitype = refine_vals

                    group_number = 1

                    self.output_list.append(("refine", [refine_style, group_number, unitype]))

                elif refine_style == "group":

                    group_number = refine_vals

                    unitype = 12

                    for item in group_number:

                        self.output_list.append(("refine", [refine_style, int(item), unitype]))

            else:

                boolean_restart_refine = "f"

                self.output_list.append(("refine", ['all', 1, 12]))

        else:

            boolean_restart = "f"

            boolean_restart_refine = "f"

            self.output_list.append(("refine", ['all', 1, 12]))


        self.output_list.append(("restart", [boolean_restart, boolean_restart_refine]))

    def Simulator(self, index):

        #       Pull which simulator is being used

        option = ''

        temp_bool = 'f'

        temperature = 10

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

    #   Saves periodic boundary information to output

    def Boundary(self, index):

        boundaries = 3 * [None]

        for i in range(0,3):

            if self.input_obj_list[index][i].isChecked():

                boundaries[i] = "s"

            else:

                boundaries[i] = "p"

        self.output_list.append(("boundary", boundaries))

    #   Sends zigzag boundary information to output

    def zigzag(self, index):

        zigzag = 3*[None]

        for i in range(0,3):

            if self.input_obj_list[index][i].isChecked():

                zigzag[i] = "t"

            else:

                zigzag[i] = "f"

        self.output_list.append(("zigzag", zigzag))

    #   Sends the lattice information to output

    def lattice(self, index):

        if str(self.input_obj_list[index][1].text()) == '':

            self.errormsg.append(('Lattice', 'Element name is missing'))

            chemicalName = 'Wrong'

        else:

            chemicalName = str(self.input_obj_list[index][1].text())

        lattice_structure = self.input_obj_list[index][2].currentText()

        #   Convert lattice structure to right format

        if lattice_structure == "FCC":

            lattice_structure = "fcc"

        elif lattice_structure == "BCC":

            lattice_structure = "bcc"

        if self.input_obj_list[index][4].text() == '':

            self.errormsg.append(('Lattice', 'Lattice parameter is missing'))

            lattice_parameter = 0

        else:

            lattice_parameter = float(self.input_obj_list[index][4].text())

        self.output_list.append(("lattice", [chemicalName, lattice_structure, lattice_parameter]))

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

    def grain(self, index):

        grain_row = 0

        grain_ori_x = []

        grain_ori_y = []

        grain_ori_z = []

        output_grain_ori = []

        grain_move = []

        output_grain_move =  []

        self.output_list.append(('grain_num', [self.grain_num]))

        if self.grain_num == 0:

            self.errormsg.append(('grain_num', 'Must create at least one grain'))

        for i in range(0, self.grain_num):

        #   Pull grain orientation

            grain_ori_x.append(str(self.grain_row_widget[grain_row+1][1].text()).split())

            if grain_ori_x == '' or len(grain_ori_x[i]) != 3:

                self.errormsg.append(('grain_ori_x', 'Incorrect format for grain orientation in x for grain '+str(i+1)))

                grain_ori_x[i] = ['1', '0', '0']

            grain_ori_y.append(str(self.grain_row_widget[grain_row+1][2].text()).split())

            if grain_ori_y == '' or len(grain_ori_y[i]) != 3:

                self.errormsg.append(('grain_ori_y', 'Incorrect format for grain orientation in y for grain '+str(i+1)))

                grain_ori_y[i] = ['0', '1', '0']

            grain_ori_z.append(str(self.grain_row_widget[grain_row+1][3].text()).split())

            if grain_ori_z == '' or len(grain_ori_z[i]) != 3:

                self.errormsg.append(('grain_ori_z', 'Incorrect format for grain orientation in z for grain '+str(i+1)))

                grain_ori_z[i] = ['0', '0', '1']

        #   Pull grain_movement

            grain_move.append([])

            for j in [1, 3 , 5]:

                if self.grain_row_widget[grain_row+2][j].text() == '':

                    grain_move[i].append(0)

                else:

                    grain_move[i].append(float(self.grain_row_widget[grain_row+2][j].text()))

            grain_row = grain_row + 4

        #   Save grain options to output

        for i in range(0, self.grain_num):

            output_grain_ori = ([i+1, "x", float(grain_ori_x[i][0]), float(grain_ori_x[i][1]), float(grain_ori_x[i][2]), "y", float(grain_ori_y[i][0]), float(grain_ori_y[i][1]), float(grain_ori_y[i][2]), "z", float(grain_ori_z[i][0]), float(grain_ori_z[i][1]), float(grain_ori_z[i][2])])

            output_grain_move = ([i+1, float(grain_move[i][0]), float(grain_move[i][1]), float(grain_move[i][2])])

            self.output_list.append(("grain_mat", output_grain_ori))

            self.output_list.append(("grain_move", output_grain_move))

    def subdomain(self,row):

        output_unit_num = []

        output_unit_type = []

        error = ['x', 'y', 'z']

        for i in range(0, self.grain_num):

            subdomain_row = 0

            unit_type = []

            output_unit_num.append(i+1)

            output_unit_type.append(i+1)

            self.output_list.append(('subdomain', [i+1, self.subdomain_num[i]]))

            if self.subdomain_num[i] == 0:

                self.errormsg.append(('subdomain_num', 'Must have at least one subdomain in grain ' + str(self.grain_num)))

            for j in range(0,self.subdomain_num[i]):

                unit_num = []

                for idx,k in enumerate([2, 4, 6]):

                    if self.subdomain_sub_widgets[i][j][k].text() == '':

                        self.errormsg.append(('unit_num', 'Missing Units in ' + error[idx] + ' in subdomain ' + str(j+1) + ' of grain ' + str(i+1)))

                        unit_num.append(1)

                    else:

                        unit_num.append(int(self.subdomain_sub_widgets[i][j][k].text()))

                if self.subdomain_sub_widgets[i][j][8].text() == '':

                    self.errormsg.append(('unit_type', 'Missing unit type in subdomain ' + str(j+1) + ' of grain ' + str(i+1)))

                    unit_type = 1

                else:

                    unit_type = int(self.subdomain_sub_widgets[i][j][8].text())

                #output_unit_num.extend([j+1, unit_num[0], unit_num[1], unit_num[2]])

                self.output_list.append(('unit_num', [i+1, j+1, unit_num[0], unit_num[1], unit_num[2]]))

                #output_unit_type.extend([j+1, unit_type])

                self.output_list.append(('unit_type', [i+1, j+1, unit_type]))

                subdomain_row = subdomain_row + 3

    def group(self, row):

        group_row = 0

        #Group Num command

        self.output_list.append(("group_num", [self.group_num, self.restart_num, self.fixnum, self.calnum]))

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

    def modify(self, row):

        self.output_list.append(("modify_num", [self.modify_num]))

        self.add_atom_vals = []

        for i in range(0, self.modify_num):

            lower_b = []

            upper_b = []

            ori = []

            if self.modify_row_widget[i][0][1].text() == '':

                modify_name = 'modify_'+str(i + 1)

            else:

                modify_name = str(self.modify_row_widget[i][0][1].text())

        #   Pull the correct option for the data

            option = ''

            for button in self.modify_row_widget[i][1]:

                if button.isChecked():

                    option = str(button.text())

        #   Both delete and CG to Atom require shape parameters.

            if option == "Delete" or option == "CG to Atom":

                if self.modify_row_widget[i][2][0][0].isChecked():

                    boolean_in = "t"

                else:

                    boolean_in = "f"

                if option == "Delete":

                    modify_style = "delete"

                    if self.modify_row_widget[i][2][0][1].isChecked():

                        boolean_delete_filled = "t"

                    else:

                        boolean_delete_filled = "f"

                else: 

                    modify_style = "cg2at"

                modify_shape = str(self.modify_row_widget[i][2][1][1].currentText())
            
            #   Group Shape Parameters

                if modify_shape == "Block":

                    for j in range(2,5):

                        if self.modify_row_widget[i][2][j][2].text() == '':

                            self.errormsg.append(('lower_b', 'Missing lower bound in modify ' + modify_name))

                            lower_b.append(0)

                        else:

                            try:

                                lower_b.append(self.checkinf(str(self.modify_row_widget[i][2][j][2].text())))

                            except ValueError:

                                self.errormsg.append(('lower_b', 'Incorrect format for lower bound in modify ' + modify_name))

                                lower_b.append(0)

                        if self.modify_row_widget[i][2][j][4] == '':

                            self.errormsg.append(('upper_b', 'Missing upper bound in modify ' + modify_name))

                            upper_b.append(0)

                        else: 

                            try:

                                upper_b.append(self.checkinf(str(self.modify_row_widget[i][2][j][4].text())))

                            except ValueError:

                                self.errormsg.append(('upper_b', 'Incorrect format for upper bound in modify ' + modify_name))

                                upper_b.append(0)

                        ori.append(str(self.modify_row_widget[i][2][j][6].text()).split())

                        ori_flag = 0

                        if ori[j-2] == '' or len(ori[j-2]) != 3:

                            ori[j-2] = [0, 0, 0]

                            self.errormsg.append(('ori', 'Incorrect format for orientation in modify ' + modify_name))

                    for list in ori:

                        list = [float(k) for k in list]

                    modify_axis = 1

                    modify_centroid = [0, 0, 0]

                    modify_radius_large = 10

                    modify_radius_small = 10

                elif modify_shape == "Cylinder":

                    lower_b = [0, 0, 0]

                    upper_b = [0, 0, 0]

                    ori = [[0, 0, 0], [0,0,0], [0,0,0]]

                    modify_centroid = [0, 0, 0]

                    modify_axis = int(self.modify_row_widget[i][2][2][1].currentText())

                    if self.modify_row_widget[i][2][2][3].text() == '':

                        self.errormsg.append(('modify_radius_large', 'Missing radius in modify ' + modify_name))

                        modify_radius_large = 1

                    else:

                        modify_radius_large = float(self.modify_row_widget[i][2][2][3].text())

                    modify_radius_small = 1

                    if self.modify_row_widget[i][2][3][2].text() == '':

                        self.errormsg.append(('lower_b', 'Missing lower bound in modify ' + modify_name))

                    else:

                        try:

                            lower_b[modify_axis] = self.checkinf(str(self.modify_row_widget[i][2][3][2].text()))

                        except ValueError:

                            self.errormsg.append(('lower_b', 'Incorrect format for lower bound in modify ' + modify_name))

                    if self.modify_row_widget[i][2][3][4].text() == '':

                        self.errormsg.append(('upper_b', 'Missing upper bound in modify ' + modify_name))

                    else:

                        try:

                            upper_b[modify_axis] = self.checkinf(self.modify_row_widget[i][2][3][4].text())

                        except ValueError:

                            self.errormsg.append(('upper_b', 'Incorrect format for upper bound in modify ' + modify_name))

                    if self.modify_row_widget[i][2][3][6].text() == '' or len(str(self.modify_row_widget[i][2][3][6].text()).split()) != 3:

                        self.errormsg.append(('ori', 'Incorrect format for orientation in modify ' + modify_name))
                        
                    else:

                        ori[modify_axis] = str(self.modify_row_widget[i][2][3][6].text()).split()

                    count = 1

                    for k in range(1, 4):

                        if k != modify_axis:

                            if self.modify_row_widget[i][2][4][count].text() == '':

                                self.errormsg.append(('modify_centroid','Missing modify centroid in modify ' + modify_name))

                            else:

                                modify_centroid[k-1] = float(self.modify_row_widget[i][2][4][count].text())

                            count = count + 1

                elif modify_shape == "Cone" or modify_shape == "Tube":

                    lower_b = [0, 0, 0]

                    upper_b = [0, 0, 0]

                    ori = [[0, 0, 0], [0,0,0], [0,0,0]]

                    modify_centroid = [0, 0, 0]

                    modify_axis = int(self.modify_row_widget[i][2][2][1].currentText())

                    if self.modify_row_widget[i][2][2][3].text() == '':

                        self.errormsg.append(('modify_radius_large', 'Missing large radius in modify ' + modify_name))

                        modify_radius_large = 0

                    else:
                    
                        modify_radius_large = float(self.modify_row_widget[i][2][2][3].text())

                    if self.modify_row_widget[i][2][2][5].text() == '':

                        self.errormsg.append(('modify_radius_small', 'Missing small radius in modify ' + modify_name))

                        modify_radius_small = 0

                    else:

                        modify_radius_small = float(self.modify_row_widget[i][2][2][5].text())

                    if self.modify_row_widget[i][2][3][2].text() == '':

                        self.errormsg.append(('lower_b', 'Missing lower bound in modify ' + modify_name))

                    else:

                        try:

                            lower_b[modify_axis-1] = self.checkinf(str(self.modify_row_widget[i][2][3][2].text()))

                        except ValueError:

                            self.errormsg.append(('lower_b', 'Incorrect format for lower bound in modify ' + modify_name))

                    if self.modify_row_widget[i][2][3][4].text() == '':

                        self.errormsg.append(('upper_b', 'Missing upper bound in modify ' + modify_name))

                    else:

                        try:

                            upper_b[modify_axis-1] = self.checkinf(str(self.modify_row_widget[i][2][3][4].text()))

                        except ValueError:

                            self.errormsg.append(('upper_b', 'Incorrect format for upper bound in modify ' + modify_name))

                    if self.modify_row_widget[i][2][3][6].text() == '' or len(str(self.modify_row_widget[i][2][3][6].text()).split()) !=3:

                        self.errormsg.append(('ori', 'Incorrect format for orientation in modify ' + modify_name))

                    else:

                        ori[modify_axis -1] = str(self.modify_row_widget[i][2][3][6].text()).split()

                    count = 1

                    for k in range(1, 4):

                        if k != modify_axis:

                            if self.modify_row_widget[i][2][4][count].text() == '':

                                self.errormsg.append(('modify_centroid', 'Missing centroid in modify ' + modify_name))

                            else:

                                modify_centroid[k-1] = float(self.modify_row_widget[i][2][4][count].text())

                            count = count + 1

                elif modify_shape == 'Sphere':

                    lower_b = [0, 0, 0]

                    upper_b = [0, 0, 0]

                    ori = [[0, 0, 0], [0,0,0], [0,0,0]]

                    modify_centroid = [0, 0, 0]

                    modify_axis = 1

                    dirs = ['x', 'y', 'z']

                    modify_radius_small = 1

                    if self.modify_row_widget[i][2][2][1].text() == '':

                        self.errormsg.append(('modify_radius_large', 'Missing radius for modify ' + modify_name))

                        modify_radius_large = 0

                    else:

                        modify_radius_large = float(self.modify_row_widget[i][2][2][1].text())


                    for indx, val in enumerate([2,4,6]):

                        if self.modify_row_widget[i][2][3][val].text() == '':

                            self.errormsg.append(('modify_centroid', 'Missing centroid position in ' + dirs[indx] + ' for modify ' + modify_name))

                        else:

                            modify_centroid[indx] = float(self.modify_row_widget[i][2][3][val].text())

                if modify_style == "delete":

                    self.output_list.append(("modify", [modify_name, modify_style, modify_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                      "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                      ori[2][2], boolean_in, boolean_delete_filled, modify_axis, modify_centroid[0], modify_centroid[1], modify_centroid[2], modify_radius_large, modify_radius_small]))

                elif modify_style == "cg2at":

                    self.output_list.append(("modify", [modify_name, modify_style, modify_shape.lower(), "x", lower_b[0], upper_b[0], ori[0][0], ori[0][1], ori[0][2],
                                      "y", lower_b[1], upper_b[1], ori[1][0], ori[1][1], ori[1][2], "z", lower_b[2], upper_b[2], ori[2][0], ori[2][1], 
                                      ori[2][2], boolean_in, 'f', modify_axis, modify_centroid[0], modify_centroid[1], modify_centroid[2], modify_radius_large, modify_radius_small]))

        #   Dislocation options

            elif option == "Dislocation":

                if self.modify_row_widget[i][2][0][1].text() == '' or len(self.modify_row_widget[i][2][0][1].text().split()) != 3:

                    centroid = [0, 0, 0]

                    self.errormsg.append(('centroid', 'Incorrect format for centroid in modify ' + modify_name))

                else:

                    centroid = str(self.modify_row_widget[i][2][0][1].text()).split()

                line_axis = int(self.modify_row_widget[i][2][0][3].currentText())

                plane_axis = int(self.modify_row_widget[i][2][0][5].currentText())

                if self.modify_row_widget[i][2][1][1].text() == '':

                    self.errormsg.append(('dis_angle', 'Missing dislocation angle in modify ' + modify_name))

                    dis_angle = 0

                else:

                    dis_angle = float(self.modify_row_widget[i][2][1][1].text())

                if self.modify_row_widget[i][2][1][3].text() == '':

                    self.errormsg.append(('poisson_ratio', 'Missing poisson ratio in modify ' + modify_name))

                    poisson_ratio = 0.5

                else:

                    poisson_ratio = float(self.modify_row_widget[i][2][1][3].text())

                self.output_list.append(("modify", [modify_name, "dislocation", line_axis, plane_axis, centroid[0], centroid[1], centroid[2], 
                                         dis_angle, poisson_ratio]))

            elif option == "Cutoff":

                if self.modify_row_widget[i][2][0][1].text() == '':

                    self.errormsg.append(('depth', 'Missing depth in modify ' + modify_name))

                    depth = 0

                else:

                    depth = float(self.modify_row_widget[i][2][0][1].text())

                if self.modify_row_widget[i][2][0][3].text() == '':

                    self.errormsg.append(('tolerance', 'Missing tolerance in modify ' + modify_name))

                    tolerance = 0

                else:

                    tolerance = float(self.modify_row_widget[i][2][0][3].text())

                self.output_list.append(("modify", [modify_name, "cutoff", depth, tolerance]))

            elif option == "Add Atom":

                self.add_atom_vals.append((i+1, self.add_atom_paths[i]))

                if self.modify_row_widget[i][2][0][1].text() == '':

                    self.errormsg.append(('xdisp', 'Missing x displacement in modify ' + modify_name))

                    xdisp = 0

                else:

                    xdisp = float(self.modify_row_widget[i][2][0][1].text())

                if self.modify_row_widget[i][2][0][3].text() == '':

                    self.errormsg.append(('ydisp', 'Missing y displacement in modify ' + modify_name))

                    ydisp = 0

                else: 

                    ydisp = float(self.modify_row_widget[i][2][0][3].text())

                if self.modify_row_widget[i][2][0][5].text() == '':

                    self.errormsg.append(('zdisp', 'Missing z displacement in modify ' + modify_name))

                    zdisp = 0

                else:

                    zdisp = float(self.modify_row_widget[i][2][0][5].text())

                self.output_list.append(("modify", [modify_name, "add_atom", xdisp, ydisp, zdisp]))

            elif option == '':

                self.errormsg.append(('modify_option','Missing modify type in modify command'))


    def getFileName(self, option):

        if option == 1:

            self.outpath,throwaway = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), 'Directory')

            if self.outpath:

                self.input_obj_list[self.outputrow][1].setText(self.outpath)

            else:

                self.input_obj_list[self.outputrow][1].setText('No folder selected')

        if option == 3:

            self.potential_path = QFileDialog.getExistingDirectory(self, 'Directory', os.getcwd())

            if self.potential_path:

                self.input_obj_list[self.potential_num][3].setText(self.potential_path)

            else:

                self.input_obj_list[self.potential_num][3].setText('No folder selected')

        if option == 4:

            button = self.sender()

            row = int(button.objectName())

            self.add_atom_paths[row], throwaway = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Lammps dump file (*)')

            if self.add_atom_paths[row]:

                self.modify_row_widget[row][2][1][1].setText(self.add_atom_paths[row])

            else:

                self.modify_row_widget[row][2][1][1].setText('No file selected')

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

    def populateFields(self, path, cac):

#       Read existing input file and populate fields


        for i,label in enumerate(self.label_list):

            if label.text() == 'Create Project Folder':

                self.input_obj_list[i][1].setText(path)

                self.outpath = path

            elif label.text() == 'Simulator:':

                options = ['dynamics', 'statics', 'hybrid']

                simulator = cac.input.simulator['type']

                option = options.index(simulator)

                self.sim_options[option].setChecked(True)

                if option == 0:

                    dyn_style = cac.input.dynamics['dyn_style']

                    if dyn_style == 'ld':

                        self.simulator[0][1].setCurrentIndex(0)

                        damping = cac.input.dynamics['damping_coefficient']

                        self.simulator[0][3].setText(str(damping))

                    elif dyn_style == 'qd':

                        self.simulator[0][1].setCurrentIndex(1)

                    elif dyn_style == 'vv':

                        self.simulator[0][1].setCurrentIndex(2)

                elif option == 1:

                    mini_style = cac.input.minimize['mini_style']

                    styles = ['cg', 'sd', 'fire', 'qm']

                    self.simulator[0][1].setCurrentIndex(styles.index(mini_style))

                    iterations = cac.input.minimize['max_iteration']

                    self.simulator[0][2].setText(str(iterations))

                    tol = cac.input.minimize['tolerance']

                    self.simulator[0][3].setText(str(tol))

                elif option == 2: 

                    dyn_style = cac.input.dynamics['dyn_style']

                    if dyn_style == 'ld':

                        self.simulator[0][1].setCurrentIndex(0)

                        damping = cac.input.dynamics['damping_coefficient']

                        self.simulator[0][3].setText(str(damping))

                        if cac.input.temperature['boolean'] == 't':

                            self.simulator[0][-1].setChecked(True)

                            self.simulator[0][-1].setText(str(cac.input.temperature['temp']))

                    elif dyn_style == 'qd':

                        self.simulator[0][1].setCurrentIndex(1)

                    elif dyn_style == 'vv':

                        self.simulator[0][1].setCurrentIndex(2)

                    energy_min = cac.input.dynamics['energy_min_freq']

                    self.simulator[0][2].setText(str(energy_min))

                    mini_style = cac.input.minimize['mini_style']

                    styles = ['cg', 'sd', 'fire', 'qm']

                    self.simulator[1][1].setCurrentIndex(styles.index(mini_style))

                    iterations = cac.input.minimize['max_iteration']

                    self.simulator[1][2].setText(str(iterations))

                    tol = cac.input.minimize['tolerance']

                    self.simulator[1][3].setText(str(tol))

            elif label.text() == 'Boundary:':

                boundaries = cac.input.boundary

                dirs = ['x', 'y', 'z']

                [self.input_obj_list[i][j].setChecked(True) for j in [dirs.index(k) for  k,v in boundaries.items() if v == 's']]

            elif label.text() == 'ZigZag boundaries:':

                zigzag = cac.input.zigzag

                dirs = ['boolean_x', 'boolean_y', 'boolean_z']

                [self.input_obj_list[i][j].setChecked(True) for j in [dirs.index(k) for  k,v in zigzag.items() if v == 't']]

            elif label.text() == 'Lattice:':

                element = cac.input.lattice['chemical_element']

                structure = cac.input.lattice['lattice_structure']

                la_pa = cac.input.lattice['lattice_constant']

                self.input_obj_list[i][1].setText(str(element))

                structs = ['fcc', 'bcc']

                self.input_obj_list[i][2].setCurrentIndex(structs.index(structure))

                self.input_obj_list[i][4].setText(str(la_pa))

            elif label.text() == 'Mass:':

                mass = cac.input.mass['atomic_mass']

                self.input_obj_list[i].setText(str(mass))

            elif label.text() == 'Grain Stack Direction:':

                stack_dir = cac.input.grain_dir['direction']

                overlap = cac.input.grain_dir['overlap']

                self.input_obj_list[i][1].setCurrentIndex(stack_dir-1)

                self.input_obj_list[i][3].setText(str(overlap))

            elif label.text() == 'Grain:':

                grain_num = cac.input.grain_num['grain_number']

                while self.grain_num < grain_num:

                    self.plusGrain(self.grainrow)

                    self.plusSub(0, self.grain_num-1)

                grain_row = 0

                for num, grain_mat in cac.input.grain_mat.items():

                    for direction, matrix in grain_mat.items():

                        dirs = ['x', 'y', 'z']

                        orientation = ''

                        for i in matrix:

                            orientation = orientation + str(i) + ' '

                        self.grain_row_widget[grain_row+1][dirs.index(direction) + 1].setText(orientation)

                    grain_row += 4

                grain_row = 0

                for num, grain_move in cac.input.grain_move.items():

                    for i,j in enumerate([1,3,5]):

                        self.grain_row_widget[grain_row+2][j].setText(str(grain_move[i]))

                    grain_row += 4

                for grain_num, subdomains in cac.input.subdomain.items():

                    while subdomains > self.subdomain_num[int(grain_num)-1]:

                        self.plusSub(0, int(grain_num))

                for grain_num,unit_num in cac.input.unit_num.items():

                    grain_num = int(grain_num)

                    for sub_num, num_mat in unit_num.items():

                        sub_num = int(sub_num)

                        for i,j in enumerate([2,4,6]):

                            self.subdomain_sub_widgets[grain_num-1][sub_num-1][j].setText(str(int(num_mat[i])))

                for grain_num,unit_type in cac.input.unit_num.items():
                    
                    grain_num = int(grain_num)

                    for sub_num, val in unit_type.items():

                        sub_num = int(sub_num)

                        self.subdomain_sub_widgets[grain_num-1][sub_num-1][8].setText(str(int(val[0])))

            elif label.text() == 'Group:':

                group_num = cac.input.group_num['new_group_number']

                fix_num = cac.input.group_num['fix_number']

                cal_num = cac.input.group_num['cal_number']

                while group_num > self.group_num:

                    self.plusGroup(self.groupRow)

                group_num = 0

                group_row = 0

                for name, params in cac.input.group.items():

                    self.group_name_array[group_num][1].setText(name)

                    cg_opts = ['element', 'node', 'null']

                    style_cg = params['style_cg']

                    self.group_row_widgets[group_row][1].setCurrentIndex(cg_opts.index(style_cg))

                    at_opts = ['atom', 'null']

                    style_at = params['style_at']

                    self.group_row_widgets[group_row][3].setCurrentIndex(at_opts.index(style_at))

                    shape_opts = ['block', 'cylinder', 'cone', 'tube', 'sphere']

                    shape = params['group_shape']

                    self.group_row_widgets[group_row][5].setCurrentIndex(shape_opts.index(shape))

                    if params['boolean_in'] == 't':

                        self.group_row_widgets[group_row+1][0][0].setChecked(True)

                    if shape == 'block':

                        for bounds, vals in params['x'].items():

                            options = ['lower_b', 'upper_b', 'orientation']

                            if bounds == options[2]:

                                output = ' '.join(str(i) for i in vals)

                            else:

                                output = vals

                            self.group_row_widgets[group_row+1][1][2*(options.index(bounds)+1)].setText(str(output))

                        for bounds, vals in params['y'].items():

                            options = ['lower_b', 'upper_b', 'orientation']

                            if bounds == options[2]:

                                output = ' '.join(str(i) for i in vals)

                            else:

                                output = vals

                            self.group_row_widgets[group_row+1][2][2*(options.index(bounds)+1)].setText(str(output))

                        for bounds, vals in params['z'].items():

                            options = ['lower_b', 'upper_b', 'orientation']

                            if bounds == options[2]:

                                output = ' '.join(str(i) for i in vals)

                            else:

                                output = vals

                            self.group_row_widgets[group_row+1][3][2*(options.index(bounds)+1)].setText(str(output))

                    elif shape == 'cylinder' or shape == 'cone' or shape == 'tube':

                        directions = ['x','y','z']

                        self.group_row_widgets[group_row+1][1][1].setCurrentIndex(params['group_axis']-1)

                        self.group_row_widgets[group_row+1][1][3].setText(str(params['group_radius_large']))

                        if shape == 'cone' or shape == 'tube':

                            self.group_row_widgets[group_row + 1][1][5].setText(str(params['group_radius_small']))

                        for bounds, vals in params[directions[params['group_axis']-1]].items():

                            options = ['lower_b', 'upper_b', 'orientation']

                            if bounds == options[2]:

                                output = ' '.join(str(i) for i in vals)

                            else:

                                output = vals

                            self.group_row_widgets[group_row+1][2][2*(options.index(bounds)+1)].setText(str(output))

                        centroid_options = ['group_centroid_x', 'group_centroid_y', 'group_centroid_z']

                        [self.group_row_widgets[group_row+1][3][2*(i + 1)].setText(str(j)) for i,j in enumerate([params[item] for item in centroid_options if item != centroid_options[params['group_axis']-1]])]

                    elif shape == 'sphere':

                        self.group_row_widgets[group_row+1][1][1].setText(str(params['group_radius_large']))

                        directions = ['group_centroid_x','group_centroid_y','group_centroid_z']

                        k = [2,4,6]

                        [self.group_row_widgets[group_row + 1][2][k[i]].setText(str(params[directions[i]])) for i in range(0,3)]

                    if fix_num > 0:

                        for fixname,fixparams in cac.input.fix.items():

                            if fixname == name:

                                self.group_row_widgets[group_row+1][0][2].setChecked(True)

                                self.fixWidgets[group_num][0][1].setChecked(True) if fixparams['boolean_def'] == 't' else None

                                self.fixWidgets[group_num][0][2].setChecked(True) if fixparams['boolean_release'] == 't' else None

                                styles = ['force', 'displacement']

                                self.fixWidgets[group_num][1][1].setCurrentIndex(styles.index(fixparams['assign_style']))

                                assignKey = ['assign_x', 'assign_y', 'assign_z']

                                assign_vec = ' '.join(str(i) for i in [fixparams[keyval] for keyval in assignKey])

                                self.fixWidgets[group_num][1][3].setText(assign_vec)

                                self.fixWidgets[group_num][1][5].setText(str(fixparams['disp_lim'])) if fixparams['assign_style'] == 'displacement' else None

                                self.fixWidgets[group_num][2][1].setText(str(fixparams['time']['time_start']))

                                self.fixWidgets[group_num][2][3].setText(str(fixparams['time']['time_end']))
                    
                                if fixparams['boolean_grad'] == 't':

                                    self.fixWidgets[group_num][3][0].setChecked(True)

                                    self.fixWidgets[group_num][3][2].setCurrentIndex(fixparams['grad_assign_axis']-1)

                                    self.fixWidgets[group_num][3][4].setCurrentIndex(fixparams['grad_assign_axis']-1)

                                    self.fixWidgets[group_num][4][1].setText(str(fixparams['grad_ref_l']))

                                    self.fixWidgets[group_num][4][3].setText(str(fixparams['grad_ref_u']))

                    if cal_num > 0:

                        for calname, calparams in cac.input.cal.items():

                            if calname == name:

                                self.group_row_widgets[group_row+1][0][3].setChecked(True)

                                cal_options = ['energy', 'force', 'virial']

                                self.calWidgets[group_num][0][1].setCurrentIndex(cal_options.index(calparams['cal_variable']))

                    group_row += 2

                    group_num += 1

            elif label.text() == 'Modify:':

                modify_num = cac.input.modify_num['modify_number']

                while modify_num > self.modify_num:

                    self.plusModify()

                modify_num = 0

                for name, params in cac.input.modify.items():

                    self.modify_row_widget[modify_num][0][1].setText(name)

                    styles = ['delete', 'cg2at', 'dislocation', 'cutoff', 'add_atom']

                    [self.modify_row_widget[modify_num][1][i].setChecked(True) for i,j in enumerate(styles) if j == params['modify_style']]

                    if params['modify_style'] == 'delete' or params['modify_style'] == 'cg2at':

                        shape = params['modify_shape']

                        self.modify_row_widget[modify_num][2][1][1].setCurrentIndex(['block','cylinder','cone','tube','sphere'].index(shape))

                        if shape == 'block':

                            for bounds, vals in params['x'].items():

                                options = ['lower_b', 'upper_b', 'orientation']

                                if bounds == options[2]:

                                    output = ' '.join(str(i) for i in vals)

                                else:

                                    output = vals

                                self.modify_row_widget[modify_num][2][2][2*(options.index(bounds)+1)].setText(str(output))

                            for bounds, vals in params['y'].items():

                                options = ['lower_b', 'upper_b', 'orientation']

                                if bounds == options[2]:

                                    output = ' '.join(str(i) for i in vals)

                                else:

                                    output = vals

                                self.modify_row_widget[modify_num][2][3][2*(options.index(bounds)+1)].setText(str(output))

                            for bounds, vals in params['z'].items():

                                options = ['lower_b', 'upper_b', 'orientation']

                                if bounds == options[2]:

                                    output = ' '.join(str(i) for i in vals)

                                else:

                                    output = vals

                                self.modify_row_widget[modify_num][2][4][2*(options.index(bounds)+1)].setText(str(output))          

                        elif shape == 'cylinder' or shape == 'cone' or shape == 'tube':

                            directions = ['x','y','z']

                            self.modify_row_widget[modify_num][2][2][1].setCurrentIndex(params['modify_axis']-1)

                            self.modify_row_widget[modify_num][2][2][3].setText(str(params['modify_radius_large']))

                            if shape == 'cone' or shape == 'tube':

                                self.modify_row_widget[i][2][2][5].setText(str(params['modify_radius_small']))

                            for bounds, vals in params[directions[params['modify_axis']-1]].items():

                                options = ['lower_b', 'upper_b', 'orientation']

                                if bounds == options[2]:

                                    output = ' '.join(str(i) for i in vals)

                                else:

                                    output = vals

                                self.modify_row_widget[modify_num][2][3][2*(options.index(bounds)+1)].setText(str(output))

                            centroid_options = ['modify_centroid_x', 'modify_centroid_y', 'modify_centroid_z']

                            [self.modify_row_widget[modify_num][2][4][2*(i + 1)].setText(str(j)) for i,j in enumerate([params[item] for item in centroid_options if item != centroid_options[params['modify_axis']-1]])]

                        elif shape == 'sphere':

                            self.modify_row_widget[modify_num][2][2][1].setText(str(params['modify_radius_large']))

                            directions = ['modify_centroid_x','modify_centroid_y','modify_centroid_z']

                            k = [2,4,6]

                            [self.modify_row_widget[modify_num][2][3][k[i]].setText(str(params[directions[i]])) for i in range(0,3)]

                    elif params['modify_style'] == 'dislocation':

                        centroid_opts = ['modify_centroid_x', 'modify_centroid_y', 'modify_centroid_z']

                        centroid = ' '.join(str(i) for i in [params[key] for key in centroid_opts])

                        self.modify_row_widget[modify_num][2][0][1].setText(centroid)

                        self.modify_row_widget[modify_num][2][0][3].setCurrentIndex(params['line_axis']-1)

                        self.modify_row_widget[modify_num][2][0][5].setCurrentIndex(params['plane_axis']-1)

                        self.modify_row_widget[modify_num][2][1][1].setText(str(params['dis_angle']))

                        self.modify_row_widget[modify_num][2][1][3].setText(str(params['poisson_ratio']))

                    elif params['modify_style'] == 'cutoff':

                        self.modify_row_widget[modify_num][2][0][1].setText(str(params['depth']))

                        self.modify_row_widget[modify_num][2][0][3].setText(str(params['tolerance']))

                    elif params['modify_style'] == 'add_atom':

                        self.modify_row_widgets[modify_num][2][0][1].setText(str(params['disp_x']))

                        self.modify_row_widgets[modify_num][2][0][3].setText(str(params['disp_y']))

                        self.modify_row_widgets[modify_num][2][0][5].setText(str(params['disp_z']))

                    modify_num += 1

            elif label.text() == 'Element':

                optionList = ['lumped','consistent', 1, 2]

                [self.input_obj_list[i][j].isChecked(True) for j,val in enumerate(optionList) if val in [cac.input.element[key] for key in ['mass_matrix','intpo_depth']]]

            elif label.text() == 'Limits:':

                self.input_obj_list[i][1].setText(str(cac.input.limit['atom_per_cell_number']))

                self.input_obj_list[i][3].setText(str(cac.input.limit['atomic_neighbor_number']))

            elif label.text() == 'Neighbor:':

                self.input_obj_list[i][1].setText(str(cac.input.neighbor['bin_size']))

                self.input_obj_list[i][3].setText(str(cac.input.neighbor['neighbor_freq']))

            elif label.text() == 'Box Direction (format is i j k):':

                x = ' '.join(str(i) for i in cac.input.box_dir['x'])

                self.input_obj_list[i][1].setText(x)

                y = ' '.join(str(i) for i in cac.input.box_dir['y'])

                self.input_obj_list[i][3].setText(y)

                z = ' '.join(str(i) for i in cac.input.box_dir['z'])

                self.input_obj_list[i][5].setText(z)

            elif label.text() == 'Deform:':

                deformNum = list(cac.input.deform.keys())

                if not deformNum:

                    continue

                subdict = cac.input.deform[deformNum[0]]

                defkeys = subdict.keys()

                modekeys = ['xx', 'yy', 'zz', 'xy', 'xz', 'yz']

                defkeys = [key for key in defkeys if key in modekeys]

                if cac.input.deform[deformNum[0]]['boolean_def'] == 't':

                    self.deform_widgets[0][0].setChecked(True)

                    [self.deform_widgets[0][2*(i+1)].setText(str(val)) for i,val in enumerate([subdict['time'][key] for key in ['time_start', 'time_end', 'time_always_flip']])] 

                    count = 0

                    while True:

                        print('{} \t {}'.format(self.deform_num, int(deformNum[0])))

                        if count == 0:

                            row = self.deform_num + 1

                        else:

                            row = self.deform_num + 2

                            self.changedef(self.defrow, 1)

                        key = defkeys[count]

                        self.deform_widgets[row][1][1].setCurrentIndex(modekeys.index(key))

                        self.deform_widgets[row][0][0].setChecked(True) if subdict[key]['boolean_cg'] == 't' else self.deform_widgets[row][0][0].setChecked(False)
                        
                        self.deform_widgets[row][0][1].setChecked(True) if subdict[key]['boolean_at'] == 't' else self.deform_widgets[row][0][1].setChecked(False)

                        self.deform_widgets[row][0][-1].setText(str(subdict[key]['def_rate']))

                        if subdict[key]['flip_frequency'] < subdict['time']['time_end']:

                            self.deform_widgets[row][1][2].setChecked(True)

                            self.deform_widgets[row][1][4].setText(str(subdict[key]['stress_l']))

                            self.deform_widgets[row][1][6].setText(str(subdict[key]['stress_u']))

                            self.deform_widgets[row][1][8].setText(str(subdict[key]['flip_frequency']))

                        count += 1

                        if not (self.deform_num < int(deformNum[0])):

                            break

                        

            elif label.text() == 'Convert:':

                output = ' '.join(str(i) for i in cac.input.convert['direction_vec'])

                self.input_obj_list[i][1].setText(output)

            elif label.text() == 'Potential:':

                pot_opts = ['eam', 'lj']

                [self.input_obj_list[i][j].setChecked(True) for j,val in enumerate(pot_opts) if val == cac.input.potential['potential_type']]

                self.potential_path = path

                self.input_obj_list[self.potential_num][3].setText(self.potential_path)

            elif label.text() == 'Constrain:':

                if cac.input.constrain['boolean'] == 't':

                    self.input_obj_list[i].setChecked(True)

                    constrain = ' '.join(str(i) for i in cac.input.constrain['direction_vec'])

                    self.constrain_widget[1].setText(constrain)

            elif label.text() == 'Dump:':

                dump = cac.input.dump

                self.input_obj_list[i][1].setText(str(dump['output_freq']))

                self.input_obj_list[i][3].setText(str(dump['reduce_freq']))

                self.input_obj_list[i][5].setText(str(dump['restart_freq']))

                self.input_obj_list[i][7].setText(str(dump['log_freq']))

            elif label.text() == 'Run:':

                self.input_obj_list[i][1].setText(str(cac.input.run['total_step']))

                self.input_obj_list[i][3].setText(str(cac.input.run['time_step']))

    def refreshFields(self):

        for i, label in enumerate(self.label_list):

            if label.text() == 'Create Project Folder':

                self.input_obj_list[i][1].setText('No file selected')

                self.outpath = ''

            elif label.text() == 'Restart Options:':

                self.restart_widgets[0][0].setChecked(False)

            elif label.text() == 'Simulator':

                [self.sim_options[i].setChecked(False)]

            elif label.text() == 'Boundary:':

                [self.input_obj_list[i][j].setChecked(False) for j in range(0,3)]

            elif label.text() == 'Lattice:':

                [self.input_obj_list[i][j].setText('') for j in [1,4]]

            elif label.text() == 'Mass:':

                self.input_obj_list[i].setText('')

            elif label.text() == 'Grain Stack Direction:':

                self.input_obj_list[i][3].setText('') 

            elif label.text() == 'Grain:':

                while self.grain_num > 0:

                    self.minusGrain(self.grainrow)

                self.plusGrain(self.grainrow)

                self.plusSub(0)

            elif label.text() == 'Group:':

                while self.group_num > 0:

                    self.minusGroup(self.groupRow)

            elif label.text() == 'Modify:':

                while self.modify_num > 0:

                    self.minusModify()

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