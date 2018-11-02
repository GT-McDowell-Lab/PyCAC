

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .InputWidgetClass import InputWidget
from .SubmissionWidgetClass import SubmissionWidget
from .SelectionWidgetClass import SelectionWidget
from .DownloadWidgetClass import DownloadWidget
from .ConverterWidgetClass import ConverterWidget
from .SubmitWidgetClass import SubmitWidget
from .RestartWidgetClass import RestartWidget
from .interface import create_base_input, collect_and_submit, generate_local_input
from .downloads import download_project, extract_timestep
from .uploads import upload_project, project_folder_check, single_run_check
from .vtk2dump import converter

from .ssh_util import login

import sys, os, copy, glob, fnmatch
import pycac

class PyCAC(QMainWindow):

    def __init__(self, parent = None):

        super(PyCAC, self).__init__(parent)

        self.central_widget = QStackedWidget()

        self.setCentralWidget(self.central_widget)

        self.selectionWidget = SelectionWidget()

        self.selectionWidget.submitSignal.connect(lambda: self.ChoosePane(self.selectionWidget.option, 0))

        self.restartWidget = RestartWidget()

        self.restartWidget.submitSignal.connect(lambda: self.errorCheck(1, self.restartWidget.output_list, self.restartWidget.FilePaths, self.restartWidget.add_atom_vals))

        self.restartWidget.backSignal.connect(lambda: self.ChoosePane(10,1))

        self.inputWidget = InputWidget()

        self.inputWidget.submitSignal.connect(lambda: self.errorCheck(0, self.inputWidget.output_list, self.inputWidget.FilePaths, self.inputWidget.add_atom_vals))

        self.inputWidget.backSignal.connect(lambda: self.ChoosePane(10,1))

        self.submitWidget = SubmissionWidget(self.inputWidget)

        self.selectionWidget.configIO(self.submitWidget.configio)

        self.submitWidget.backSignal.connect(lambda: self.swapWindows(0))

        self.submitWidget.submitLocalSignal.connect(lambda: self.submitJob(0))

        self.submitWidget.submitClusterSignal.connect(lambda: self.submitJob(1))

        self.submitjobWidget = SubmitWidget()

        self.submitjobWidget.submitsignal.connect(lambda: self.submitjob())

        self.submitjobWidget.backsignal.connect(lambda: self.ChoosePane(10,1))

        self.downloadWidget = DownloadWidget()

        self.downloadWidget.backButton.connect(lambda: self.ChoosePane(10,1))

        self.downloadWidget.submitButton.connect(lambda: self.downloadFiles())

        self.convertWidget = ConverterWidget()

        self.convertWidget.back.connect(lambda: self.ChoosePane(10,1))

        self.convertWidget.submit_signal.connect(lambda: self.convert())

        self.central_widget.addWidget(self.selectionWidget)

        self.central_widget.addWidget(self.inputWidget)

        self.central_widget.addWidget(self.restartWidget)

        self.central_widget.addWidget(self.submitWidget)

        self.central_widget.addWidget(self.downloadWidget)

        self.central_widget.addWidget(self.convertWidget)

        self.central_widget.addWidget(self.submitjobWidget)

        self.setWindowTitle("PyCAC")

        self.setGeometry(500, 300, 1000, 500)

        self.base = None

    def errorCheck(self, restart, forCheck, filepaths, addAtomVals):

        self.base = create_base_input(forCheck, filepaths, addAtomVals)

        errors = self.base.input.errors #Add filepaths later

        labels = []

        output_error = ""

        for command, error in errors:

            labels.append(command)

            output_error = output_error + '\u2022' + error + "\n"

        if restart:

            for identifier, error in self.restartWidget.errormsg:

                output_error = output_error + '\u2022' + error + "\n"

        else:

            for identifier, error in self.inputWidget.errormsg:

                output_error = output_error + '\u2022' + error + "\n"

        if output_error != "":

            errormsg = QMessageBox()

            errormsg.setText(output_error)

            errormsg.setWindowTitle("Error in Input Form")

            errormsg.exec_()

        else:

            if self.selectionFlag == 0 or self.selectionFlag == 1:

                self.swapWindows(1)

            elif self.selectionFlag == 2:

                if self.submitProjectFlag:

                    overwrite_input(self.selectionWidget.uploadDir + '/' +self.outputList[0][0] + '/input.in', self.base)

                    del self.outputList[0]

                    self.projectErrorCheck()

                else:

                    overwrite_input(self.selectionWidget.uploadDir + '/input.in', self.base)

                    self.central_widget.setCurrentWidget(self.submitjobWidget)

            

    def swapWindows(self, dir):

        if dir == 1:

            self.submitWidget.userInput(self.inputWidget)

            self.central_widget.setCurrentWidget(self.submitWidget)

        elif dir == 0:

            if self.selectionWidget.restartTF:

                self.central_widget.setCurrentWidget(self.inputWidget)

            else:

                self.central_widget.setCurrentWidget(self.inputWidget)

    def submitJob(self, submitCluster):

        errorlist = []

        for ident,error in self.submitWidget.errormsg:

            errorlist.append(error)

        if len(errorlist) == 0:

            if submitCluster:

                fail, errors = collect_and_submit(self.base, self.submitWidget.host, self.submitWidget.user, self.submitWidget.password, self.submitWidget.param_list, self.submitWidget.nodes,
                                                  self.submitWidget.ppn, self.submitWidget.hostdir, self.submitWidget.walltime, self.submitWidget.jobname, self.submitWidget.qname)

            else:

                fail, errors = generate_local_input(self.base, self.submitWidget.param_list)

                print((fail,errors))

            if fail:

                for err in errors:

                    errorlist.append(err) 

            else:

                self.finalMessageBox(errors[0])

        if len(errorlist) > 0:

            output = ''

            for error in errorlist:

                #print(error)

                output = output + error + '\n'

            self.errorDialog(output)

    def ChoosePane(self, selectionOption, callerWidget):

        self.submitProjectFlag = 0

        self.selectionFlag = selectionOption

        self.inputWidget.refreshFields()

        self.downloadWidget.refreshFields()

        self.convertWidget.refreshFields()

        self.submitWidget.refreshFields()

        self.submitjobWidget.refreshFields()

        if selectionOption == 0:

            if self.selectionWidget.restartTF:

                self.central_widget.setCurrentWidget(self.restartWidget)

            else:

              self.central_widget.setCurrentWidget(self.inputWidget)

        elif selectionOption == 1:

            if self.selectionWidget.uploadDir == '':

                self.errorDialog('No directory selected')

                return

            filepath = self.selectionWidget.uploadDir

            run_dir = os.path.dirname(filepath)

            error, cac = single_run_check(run_dir, os.listdir(run_dir))

            if error == 1:

                errors = ''

                for val,msg in cac[1]:

                    errors = errors + msg + "\n"

                errorbox = QMessageBox()

                errorbox.setText(errors)

                errorbox.setWindowTitle('Error in selection of input file')

                errorbox.exec_()

            elif error == 2:

                errorDialog(cac)

            else:

                self.inputWidget.populateFields(run_dir, cac)

                self.central_widget.setCurrentWidget(self.inputWidget)

                if len(cac.input.errors) > 0:

                    errors = ''

                    for ID, errormsg in cac.input.errors:

                        errors = errors + errormsg + '\n'

                    errorbox = QMessageBox()

                    errorbox.setText(errors)

                    errorbox.setWindowTitle('Error in input file')

                    errorbox.exec_()

        elif selectionOption == 2:

            if self.selectionWidget.uploadDir == '':

                self.errorDialog('No directory selected')

                return

            path = self.selectionWidget.uploadDir

            files = glob.glob(path + '/*')

            projectBool = 1

            dir_flag = 0

            for file in files:

                if (os.path.isdir(file) or fnmatch.fnmatch(file.split('/')[-1], '*.pbs')):

                    dir_flag = 1

                else:

                    projectBool = 0

                if projectBool == 0 and dir_flag == 1:

                    break


            if projectBool:

                error, self.outputList = project_folder_check(path)

                if not error:

                    self.central_widget.setCurrentWidget(self.submitjobWidget)

                elif error:

                    self.submitProjectFlag = 1

                    self.projectErrorCheck()

            else:

                if dir_flag:

                    errorbox = QMessageBox()

                    errorbox.setText('File structure is not setup correctly. Please select a single run folder or clean project directory')

                    errorbox.setWindowTitle('Error in selection')

                    errorbox.exec_()
                
                else:

                    error,cac = single_run_check(path, os.listdir(path))

                    if error:

                        self.errorDialog(cac)

                    else:

                        if len(cac.input.errors) > 0:

                            self.inputWidget.populateFields(path, cac)

                            self.central_widget.setCurrentWidget(self.inputWidget)

                            errors = ''

                            for ID, errormsg in cac.input.errors:

                                errors = errors + errormsg + '\n'

                            errorbox = QMessageBox()

                            errorbox.setText(errors)

                            errorbox.setWindowTitle('Error in input file')

                            errorbox.exec_()

                        else:

                            self.central_widget.setCurrentWidget(self.submitjobWidget)

        elif selectionOption == 3:

            self.central_widget.setCurrentWidget(self.downloadWidget)

        elif selectionOption == 4:

            self.central_widget.setCurrentWidget(self.convertWidget)

        if callerWidget == 1:

            self.central_widget.setCurrentWidget(self.selectionWidget)


    def downloadFiles(self):

        errorstat = 0

        successmsg = ''

        errormsg = ''

        if not self.downloadWidget.errormsg:

            for hostdir in self.downloadWidget.projectDirs:

                error, status = download_project(self.downloadWidget.server, self.downloadWidget.user, self.downloadWidget.password, 
                                                self.downloadWidget.local_dir, hostdir)


                if error:

                    errormsg = errormsg + status + '\n'

                    errorstat = 1
                
                else:

                    successmsg += status + '\n'

        else:
        
            for id,error in self.downloadWidget.errormsg:

                errormsg += error + '\n'

                errorstat = 1

        if errorstat:

            errorBox = QMessageBox()

            errorBox.setText(errormsg)

            errorBox.setWindowTitle("Error in Download")

            errorBox.exec_()

        else:

            if self.downloadWidget.convertNum > 0:

                successBox = QMessageBox()

                successBox.setText("Successful download to: " + successmsg + 'Please press ok to continue with conversion to dump. This may take a while.')

                successBox.setWindowTitle("Successful Download")         

                successBox.exec_()

            else:

                self.finalMessageBox("Successful download to " + successmsg)

        for i in range(0,self.downloadWidget.convertNum):

            directory = self.downloadWidget.convertProjectDirs[i]

            error,time_steps = extract_timestep(directory)

            if error:

                errorbox = QMessageBox()

                errorbox.setText(time_steps)

                errorbox.setWindowTitle('Error in vtk to dump conversion')

                errorbox.exec_()

            else:

                errormsg = ''

                successmsg = ''

                for param in self.downloadWidget.convertProjectParams:

                    if not isinstance(param,str):

                        param = str(param) 

                    param = str(param)

                for step in time_steps:

                    error, msg = converter(directory, step, self.downloadWidget.convertProjectParams[i], 8, 1)

                self.finalMessageBox("Successful conversion of files")

    def convert(self):

        if len(self.convertWidget.errormsg) > 0:

            errormsg = ''

            for ident, error in self.convertWidget.errormsg:

                errormsg = errormsg + error + '\n'

            errorbox = QMessageBox()

            errorbox.setText(errormsg)

            errorbox.setWindowTitle('Error in vtk to dump conversion')

            errorbox.exec_()

        else:

            for i, paramList in enumerate(self.convertWidget.convertProjectParams):

                errorFlag = [0, 0]

                errorString = ['\tMissing coarse grained region for file {} in timestep {} ', '\tMissing atomistic region for file {} in timestep {}', '\tMore than 3 coarse grained files missing for project ', '\tMore than 3 atomistic files missing for project ']

                errormsg = 'Warning(s):'

                directory = self.convertWidget.path[i]

                error, time_steps = extract_timestep(directory)

                if error:

                    errorbox = QMessageBox()

                    errorbox.setText(time_steps)

                    errorbox.setWindowTitle('Error in vtk to dump conversion')

                    errorbox.exec_()

                else:

                    timesteps = []

                    for step in time_steps:

                        error, msg = converter(directory, step, paramList, 8, 1)

                        if error:

                            errorFlag[error-1] += 1

                            timesteps.append(step)
                        
                    dialogFlag = 0

                    for j,flag in enumerate(errorFlag):

                        if flag > 3:

                            errormsg += errorString[j+2] + self.convertWidget.path[i] + '\n'

                            dialogFlag = 1

                        elif flag:

                            for step in timesteps:

                                errormsg += errorString[j].format(self.convertWidget.path[i], step) + '\n'

                            dialogFlag = 1

                    if dialogFlag:

                        self.errorDialog(errormsg)

                    else: 

                        self.finalMessageBox('Successful conversion of all files')


    def submitjob(self):

        if self.submitjobWidget.errorvals:

            errormsg = ''

            for errID, error in self.submitjobWidget.errorvals:

                errormsg = errormsg + error + '\n'

            self.errorDialog(errormsg)

        else: 

            conn_err, connection = login(self.submitjobWidget.host, self.submitjobWidget.user, self.submitjobWidget.password)

            if not conn_err:

                error, errorvals = upload_project(self.selectionWidget.uploadDir, self.submitjobWidget.hostdir, connection, self.submitjobWidget.nodes, self.submitjobWidget.ppn, self.submitjobWidget.walltime, 
                                                  self.submitjobWidget.jobname, self.submitjobWidget.qname)

                if error:

                    self.errorDialog(errorvals)

                else:

                    self.finalMessageBox(errorvals[0])


    def projectErrorCheck(self):

        try:

            self.inputWidget.populateFields(self.selectionWidget.uploadDir + '/' +self.outputList[0][0], self.outputList[0][1])

            self.central_widget.setCurrentWidget(self.inputWidget)

            errormsg = ''

            for ident,error in self.outputList[0][1].input.errors:

                errormsg = errormsg + error + '\n'

            errorbox = QMessageBox()

            errorbox.setText(errormsg)

            errorbox.setWindowTitle('Error in input file')

            errorbox.exec_()

        except IndexError:

            self.central_widget.setCurrentWidget(self.submitjobWidget)


    def finalMessageBox(self, message):

            submitmsg = QMessageBox()

            submitmsg.setText(message)

            submitmsg.setWindowTitle("Success!")

            yesButton = submitmsg.addButton('Home', QMessageBox.YesRole)

            abortButton = submitmsg.addButton('Close', QMessageBox.NoRole)

            val = submitmsg.exec_()

            if submitmsg.clickedButton() == yesButton:

                self.inputWidget.refreshFields()

                self.ChoosePane(10,1)

            elif submitmsg.clickedButton() == abortButton:

                sys.exit()

    def errorDialog(self, message):

        errorbox = QMessageBox()

        errorbox.setWindowTitle('Error')

        errorbox.setText(message)

        errorbox.exec_()

def start_job_gui():

    app = QApplication([])

    window = PyCAC()

    window.setWindowIcon(QIcon(os.path.join(os.path.dirname(pycac.__file__), 'icon.png')))

    window.show()

    app.exec_()


