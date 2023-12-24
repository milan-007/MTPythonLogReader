# This Python file uses the following encoding: utf-8
import sys
import os
import logging
import pprint

from PySide2.QtCore import QFile, QDir, QFileSystemWatcher, QFileInfo,\
    QCoreApplication, Qt, QPoint,\
    qDebug


from PySide2.QtWidgets import QApplication, QMainWindow,\
    QWidget, QTabWidget, QLabel, QMessageBox, QLineEdit, QPushButton,\
    QAction, QToolBar,\
    QGridLayout, QFrame

from src import utils, settings, tab




class LogReader(QMainWindow):

    initValues = {
        "mwg": {
            "key": "windows/mainWindow/geometry", "value": ""
            },
    }
    def __init__(self, file):
        super().__init__()
        self.settings = settings.Settings(self.initValues)
        self.setWindowTitle("QSingleApplication Demo")
        savedGeometry = self.settings.getValueByAbbreviature("mwg")
        if savedGeometry:
            self.restoreGeometry(savedGeometry)

        self.defineActions()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar())
        self.setupUI()
        self.watcher = QFileSystemWatcher()
        qDebug(f"{file}")
        self.tabs = []
        if file:
            self.fileName = file if utils.fileExists(file) else ""
        else:
            self.fileName = ""
        qDebug(f"self.fileName:  {self.fileName}")
        if self.fileName:
            self.addTab()

        #
        pass

    def setupUI(self):
        cw = QWidget()
        cw.setLayout(self.myLayout())
        self.setCentralWidget(cw)

    def myLayout(self):

        self.qleSearchText = QLineEdit()

        self.qpbForward = QPushButton()
        self.qpbForward.setIcon(utils.getIcon("arrow-up"))
        self.qpbForward.setMaximumWidth(20)

        self.qpbBackward = QPushButton()
        self.qpbBackward.setIcon(utils.getIcon("arrow-down"))
        self.qpbBackward.setMaximumWidth(20)

        framegrid = QGridLayout()
        i = 0
        framegrid.addWidget(self.qleSearchText, i, 0, 1, 3)
        framegrid.addWidget(self.qpbForward, i, 4)
        framegrid.addWidget(self.qpbBackward, i, 5)

        self.qfSearch = QFrame()
        self.qfSearch.setVisible(False)
        self.qfSearch.setFrameShadow(QFrame.Raised)
        self.qfSearch.setFrameShape(QFrame.Box)
        self.qfSearch.setLayout(framegrid)



        self.label = QLabel()
        self.label.setText("Pokus")
        self.qTabW = QTabWidget()

        mainGrid = QGridLayout()
        mainGrid.addWidget(self.label, 1, 1)
        mainGrid.addWidget(self.qTabW, 2, 0, 10, 10)
        mainGrid.addWidget(self.qfSearch, 13, 0, 1, 10)
        return mainGrid

    def defineActions(self):

        self.actExit = self.createAction(
           "exit", self.exitApp,
           self.tr("Exit program"),
           self.tr("Exits the program")
        )
        self.actExit.setShortcut("Ctrl+X")

        self.actAddTab = self.createAction(
            "tab-new", self.addTab,
            self.tr("Add tab"),
            self.tr("Add tab to existing tab(s)")
        )

        self.actSearch = self.createAction(
            "edit-find", self.search,
            self.tr("Search"),
            self.tr("Search in text")
        )
        pass

    def createAction(self, icon, do, text: str = "", tooltip: str = ""):
        action = QAction(utils.getIcon(icon), text, self)
        action.setStatusTip(tooltip)
        action.triggered.connect(do)
        return action

    def toolbar(self):
        toolbar = QToolBar("Main toolbar")
        toolbar.setOrientation(Qt.Horizontal)
        toolbar.setMovable(True)
        toolbar.setAllowedAreas(
                    Qt.LeftToolBarArea | Qt.RightToolBarArea | Qt.TopToolBarArea)
        toolbar.addAction(self.actSearch)
        return toolbar


    def exitApp(self):
        self.close()
        pass

    def addTab(self):
        tabCreator = tab.Tab(self.fileName)
        newTab = tabCreator.tab()
        # print(newTab)
        tabName = os.path.basename(self.fileName)
        self.qTabW.addTab(newTab, tabName)
        for i in range(self.qTabW.count()):
            file = self.qTabW.widget(i).fileName
            qDebug(f"a: {file}")
        pass

    def search(self):
        self.qfSearch.setVisible(True)
        self.qleSearchText.setFocus()

    def handleMessage(self, message):
        self.label.setText(message)
        if message:
            self.fileName = message if utils.fileExists(message) else ""
        else:
            self.fileName = ""

        if self.fileName:
            found = False
            for i in range(self.qTabW.count()):
                openedFile = self.qTabW.widget(i).fileName
                if self.fileName == openedFile:
                    found = True
                    self.qTabW.setCurrentIndex(i)
        if not found:
            self.addTab()

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowState(Qt.WindowState.WindowActive)
        pass

    def closeEvent(self, event):
        self.settings.setValueByAbbreviature("mwg", self.saveGeometry())
        event.accept()
        pass

    def error(self, text):
        QMessageBox.critical(
            self,
            self.tr("Warning :"),
            text)

    def tr(self, text):
        trs = QApplication.translate("MainWindow", text)
        if trs is None:
            trs = text
        return trs


#def setAppAttributes(a: QApplication):
#    a.setApplicationName(i.applicationName)
#    a.setOrganizationName(i.organisationName)
#    a.setOrganizationDomain(i.web)





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


