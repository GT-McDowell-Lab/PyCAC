from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

class installWidget(QWidget):

    submitSignal = pyqtSignal()

    def __init__(self):

        super(installWidget, self).__init__()

        installWidget.window(self)

    def window(self):

        self.cac_path = ''

        box_layout = QVBoxLayout()

        textField = QPlainTextEdit()

        textField.setReadOnly(True)

        textField.setPlainText("This installs PyCAC to the specified destination directory." +
            " This directory will remain as your working directory for future PyCAC runs so please select the path accordingly. \n NOTE: Install will proceed in the background. Wait for pop up message to confirm completion.")

        box_layout.addWidget(textField)

        fileLayout = QHBoxLayout()

        fileLayout.setAlignment(Qt.AlignLeft)

        self.fileWidgets = [QLabel("Select CAC .tar file:"),QPushButton('Browse'), QLabel('No file selected')]

        self.fileWidgets[1].clicked.connect(lambda: self.getFileNames())

        [fileLayout.addWidget(widget) for widget in self.fileWidgets]

        box_layout.addLayout(fileLayout)

        subLayoutone = QHBoxLayout()

        self.input_forms = []

        for i in range(0,4):

            self.input_forms.append(QLineEdit())

        self.input_forms[3].setEchoMode(QLineEdit.Password)

        widgets = [QLabel('Server URL:'), self.input_forms[0], QLabel('Server Installation Directory:'), self.input_forms[1], QLabel('Workload Manager:')]

        self.jobType = QComboBox()

        self.jobType.addItems(['torque', 'slurm'])

        for widget in widgets:

            subLayoutone.addWidget(widget)

        subLayoutone.addWidget(self.jobType)

        subLayouttwo = QHBoxLayout()

        box_layout.addLayout(subLayoutone)

        widgets = [QLabel('Username:'), self.input_forms[2], QLabel('Password:'), self.input_forms[3]]

        for widget in widgets:

            subLayouttwo.addWidget(widget)

        box_layout.addLayout(subLayouttwo)

        submit = QPushButton('Install')

        submit.clicked.connect(lambda: self.install())

        box_layout.addWidget(submit)

        self.setLayout(box_layout)

    def install(self):

        self.output = []

        for lineedit in self.input_forms:

            self.output.append(str(lineedit.text()))

        self.osType = str(self.jobType.currentText())

        self.submitSignal.emit()

    def getFileNames(self):

        self.cac_path, throwaway = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'CAC source (*.tar)')

        if not self.cac_path:

            self.fileWidgets[2].setText('No file selected')

        else:

            self.fileWidgets[2].setText(self.cac_path)


