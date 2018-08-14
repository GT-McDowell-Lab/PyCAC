import pycac

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .installWidget import installWidget
from .install import run_install
import sys, os


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

        if self.installWidget.cac_path == '':

            self.errorDialog('No CAC file selected, please select a correct CAC.tar file')

        else:

            status, msg = run_install(output[0], output[2], output[3], output[1], self.installWidget.osType, self.installWidget.cac_path)

            message = QMessageBox()

            message.setText(msg)

            message.setWindowTitle('Installation Status')
            
            message.exec_()

            if not status:
                
                sys.exit()


    def errorDialog(self, message):

        errorbox = QMessageBox()

        errorbox.setWindowTitle('Error')

        errorbox.setText(message)

        errorbox.exec_()

def start_config_gui():

    app = QApplication([])

    window = installPyCAC()

    window.setWindowIcon(QIcon(os.path.join(os.path.dirname(pycac.__file__), 'icon.png')))

    window.show()

    app.exec_()
 