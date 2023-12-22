# This Python file uses the following encoding: utf-8
import sys
import os
import logging
import pprint

from PySide2.QtCore import QFile, QDir, QFileSystemWatcher, QFileInfo,\
    QCoreApplication, Qt, QPoint,\
    Slot, Signal, qDebug

from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget,\
    QLabel, QGridLayout

from src import utils, settings

import info as i


class LogReader(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QSingleApplication Demo")
        self.defineActions()
        self.setupUI()
        pass

    def setupUI(self):
        cw = QWidget()
        cw.setLayout(self.myLayout())
        self.setCentralWidget(cw)

    def myLayout(self):
        self.label = QLabel()
        self.label.setText("Pokus")
        mainGrid = QGridLayout()
        mainGrid.addWidget(self.label, 1, 1)
        return mainGrid

    def defineActions(self):

        self.actExit = self.createAction(
           "exit", self.exitApp,
           self.tr("Exit program"),
           self.tr("Exits the program")
        )
        self.actExit.setShortcut("Ctrl+X")
        pass

    def createAction(self, icon, do, text: str = "", tooltip: str = ""):
        action = QAction(utils.getIcon(icon), text, self)
        action.setStatusTip(tooltip)
        action.triggered.connect(do)
        return action

    def handleMessage(self, message):
        self.label.setText(message)
        self.activateWindow()
        pass

    def tr(self, text):
        trs = QApplication.translate("MainWindow", text)
        if trs is None:
            trs = text
        return trs



def setAppAttributes(a: QApplication):
    a.setApplicationName(i.applicationName)
    a.setOrganizationName(i.organisationName)
    a.setOrganizationDomain(i.web)





#def main(arg: list):
#    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
#    app = QSingleApplication([])
#    setAppAttributes(app)
#    # appPath = os.path.dirname(__file__)
#    i.appPath = setAppPath(arg[0])
#    setLogger("logs", "LogReader.log")

#    window = LogReader()
#    app.singleStart(window)
#    sys.exit(app.exec_())

#    filename = ""
#    if len(arg) > 1:
#        filename = arg[1]
#        logger.debug(filename)
#        if not utils.filename.exists():
#            filename = ""


    #window = LogReader()
    #window.show()
    #sys.exit(app.exec_())


