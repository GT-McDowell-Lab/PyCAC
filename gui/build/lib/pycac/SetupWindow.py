import pycac

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from installWidget import *
import sys


class installPyCAC(QMainWindow):

    def __init__(self, parent = None):

        super(installPyCAC, self).__init__(parent)

        self.central_widget = QStackedWidget()

        self.setCentralWidget(self.central_widget)

        self.installWidget = installWidget()

        self.installWidget.submitSignal.connect(lambda: self.submit(self.installWidget.output))

        self.central_widget.addWidget(self.installWidget)

        self.setWindowTitle("Install PyCAC")

        self.setGeometry(500, 300, 800, 200)

        self.base = None

    def submit(self, output):

        status, msg = run_install(output[0], output[2], output[3], output[1], self.installWidget.osType, self.installWidget.cac_path, self.installWidget.qname)

        message = QMessageBox()

        message.setText(msg)

        message.setWindowTitle('Installation Status')
        
        message.exec_()

        if not status:
            
            sys.exit()

def start_config_gui():

    app = QApplication([])

    window = installPyCAC()

    window.show()

    app.exec_()
 