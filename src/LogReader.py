# This Python file uses the following encoding: utf-8
import sys
import os
import logging
import pprint
import info as f

from PySide2.QtCore import QFile, QDir, QFileSystemWatcher, QFileInfo,\
    QCoreApplication, Qt, QPoint,\
    qDebug


from PySide2.QtWidgets import QApplication, QMainWindow,\
    QWidget, QTabWidget, QLabel, QMessageBox, QLineEdit, QPushButton, QFileDialog,\
    QAction, QToolBar, QMenu, QStatusBar,\
    QGridLayout, QFrame

from src import utils, settings, tab


class LogReader(QMainWindow):

    initValues = {
        "mwg": {
            "key": "windows/mainWindow/geometry", "value": ""
        }
    }

    def __init__(self, file):
        super().__init__()
        self.settings = settings.Settings(self.initValues)
        self.setWindowTitle(f.applicationName)
        self.setStatusBar(QStatusBar(self))
        savedGeometry = self.settings.getValueByAbbreviature("mwg")
        if savedGeometry:
            self.restoreGeometry(savedGeometry)

        self.setupUI()
        self.fwatcher = QFileSystemWatcher()
        self.fwatcher.fileChanged.connect(self.fileWasChanged)
        # qDebug(f"{file}")

        self.maxRecentFiles = 10
        self.recentFiles = self.settings.readList("Recent", "file")
        self.recentFiles = list(set(self.recentFiles))

        logging.debug(f"recent : {self.recentFiles}")

        self.defineActions()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar())
        self.menu()

        if file:
            self.fileName = file if utils.fileExists(file) else ""
        else:
            self.fileName = ""
        # qDebug(f"self.fileName:  {self.fileName}")
        if self.fileName:
            self.addTab()

        #
        # self.settings.writeToArray("Recent", "s", "d", "r")
        pass

    def setupUI(self):
        cw = QWidget()
        cw.setLayout(self.myLayout())
        self.setCentralWidget(cw)

    def myLayout(self):
        self.qleSearchedText = QLineEdit()
        self.qleSearchedText.textChanged.connect(self.searchedTextchanged)
        self.qpbForward = QPushButton()
        self.qpbForward.setIcon(utils.getIcon("arrow-up"))
        self.qpbForward.setMaximumWidth(20)

        self.qpbBackward = QPushButton()
        self.qpbBackward.setIcon(utils.getIcon("arrow-down"))
        self.qpbBackward.setMaximumWidth(20)

        self.qpbHide = QPushButton()
        self.qpbHide.setIcon(utils.getIcon("dialog-close"))
        self.qpbHide.setMaximumWidth(20)


        framegrid = QGridLayout()
        i = 0
        framegrid.addWidget(self.qleSearchedText, i, 0, 1, 3)
        framegrid.addWidget(self.qpbForward, i, 4)
        framegrid.addWidget(self.qpbBackward, i, 5)
        framegrid.addWidget(self.qpbHide, i, 6)

        self.qfSearch = QFrame()
        self.qfSearch.setVisible(False)
        self.qfSearch.setFrameShadow(QFrame.Raised)
        self.qfSearch.setFrameShape(QFrame.Box)
        self.qfSearch.setLayout(framegrid)

        self.qTabW = QTabWidget()
        self.qTabW.setTabsClosable(True)
        self.qTabW.currentChanged.connect(self.qtabW_currentChanged)
        self.qTabW.tabCloseRequested.connect(self.qTabW_tabcloseR)

        mainGrid = QGridLayout()
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
        self.actSearch.setShortcut("Ctrl+F")
        self.actSearch.setVisible(False)

        self.actOpenDocument = self.createAction(
            "document-open", self.openFile,
            self.tr("Open document"),
            self.tr("Open new document")
        )
        self.actOpenDocument.setShortcut("Ctrl+O")

        self.actOpenRecent = self.createAction(
            "document-open-recent", None,
            self.tr("Open recent document"),
            self.tr("Open previously opened document")
        )
        self.openRecent_submenu()



        # self.recentFiles(self.actOpenRecent)

        self.actCloseDocument = self.createAction(
            "edit-find", self.closeTab,
            self.tr("Close"),
            self.tr("Close current document")
        )
        self.actCloseDocument.setShortcut("Ctrl+W")
        pass

    def createAction(self, icon, do, text: str = "", tooltip: str = ""):
        action = QAction(utils.getIcon(icon), text, self)
        action.setStatusTip(tooltip)
        action.triggered.connect(do)
        return action

    def openRecent_submenu(self):
        if recmenu := self.recentOpened():
            logging.debug("instaluji nové menu")
            self.actOpenRecent.setMenu(recmenu)
        else:
            self.actOpenRecent.setVisible(False)

    def recentOpened(self):
        menu = QMenu()
        # logging.debug(f"Recent files : {self.recentFiles}")
        for file in self.recentFiles:
            if self.isOpened(file) is False:
                action = QAction(os.path.basename(file), self)
                action.setToolTip(file)
                action.setStatusTip(file)
                # logging.debug(f"přidávám : {file}")
                menu.addAction(action)
            else:
                continue
        menu.triggered.connect(self.recent_activated)
        return menu
        pass

    def toolbar(self):
        toolbar = QToolBar("Main toolbar")
        toolbar.setOrientation(Qt.Horizontal)
        toolbar.setMovable(True)
        toolbar.setAllowedAreas(
                    Qt.LeftToolBarArea | Qt.RightToolBarArea | Qt.TopToolBarArea)
        toolbar.addAction(self.actSearch)
        toolbar.addAction(self.actOpenRecent)
        return toolbar

    def menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(self.tr("&File"))
        fileMenu.addAction(self.actOpenDocument)
        fileMenu.addAction(self.actOpenRecent)
        fileMenu.addAction(self.actExit)

        editMenu = mainMenu.addMenu(self.tr("&Edit"))
        editMenu.addAction(self.actSearch)

        pass

    def exitApp(self):
        self.close()
        pass

    def recent_activated(self, action):
        self.fileName = action.toolTip()
        logging.info(self.fileName)
        # logging.debug(f"activated {action.toolTip()}")
        if utils.fileExists(self.fileName):
            self.addTab()
        else:
            self.recentFiles.remove(self.fileName)
            self.error(self.tr("File already does not exists !"))
        pass

    def isOpened(self, file):
        for i in range(self.qTabW.count()):
            opened = self.qTabW.widget(i).fileName
            if opened == file:
                return i
        return False

    def addTab(self):
        # logging.debug(f"{self.recentFiles}")
        self.recentFiles.insert(0, self.fileName)
        # logging.debug(f"{self.recentFiles}")
        self.recentFiles = list(dict.fromkeys(self.recentFiles))
        rv = self.cutRecentList(self.recentFiles)
        logging.debug(f"{pprint.pformat(self.recentFiles)}")

        self.settings.writeList("Recent", "file", self.recentFiles[:self.maxRecentFiles])
        tabCreator = tab.Tab(self.fileName)
        newTab = tabCreator.tab()
        newTab.colorChange.connect(self.qle_changeColor)
        # print(newTab)
        tabName = os.path.basename(self.fileName)
        ci = self.qTabW.addTab(newTab, tabName)
        self.qTabW.setTabToolTip(ci, self.fileName)
        self.qTabW.setCurrentIndex(ci)
        self.fwatcher.addPath(self.fileName)
        self.openRecent_submenu()
        self.actSearch.setVisible(True)
        pass

    def cutRecentList(self, recent: list)-> list:
        logging.debug("vstupuju")

    def search(self):
        self.qfSearch.setVisible(True)
        self.qTabW.widget(self.currActiveTab).searchStatus = True
        self.qleSearchedText.setFocus()
        pass

    def searchedTextchanged(self):
        self.qTabW.widget(self.currActiveTab).search(self.qleSearchedText.text())
        pass

    def qle_changeColor(self, color):
        logging.debug(color)


    def handleMessage(self, message):
        self.label.setText(message)
        if message:
            self.fileName = message if utils.fileExists(message) else ""
        else:
            self.fileName = ""

        if self.fileName:
            i = self.isOpened(self.fileName)
            if i is False:
                self.addTab()
            else:
                self.qTabW.setCurrentIndex(i)
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()
            self.setWindowState(Qt.WindowState.WindowActive)
        pass

    def qtabW_currentChanged(self, index):
        logging.debug(f"Tab změněn: {index}")
        self.currActiveTab = index
        if index >= 0:
            tabWg = self.qTabW.widget(index)
            self.qfSearch.setVisible(tabWg.searchStatus)
            logging.debug(f"Hledaný text : {tabWg.searchedText}")
            self.qleSearchedText.setText(tabWg.searchedText)
        else:
            self.actSearch.setVisible(False)
            self.qfSearch.setVisible(False)
        pass

    def qTabW_tabcloseR(self, index):
        file = self.qTabW.widget(index).fileName
        self.fwatcher.removePath(file)
        self.qTabW.removeTab(index)
        self.openRecent_submenu()

        pass

    def closeTab(self):
        self.qTabW.removeTab(self.currActiveTab)
        pass

    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open file"),
            None,
            self.tr("Any file (*)"),
            options=QFileDialog.DontUseNativeDialog
            )
        # print( type( fileName ), fileName )
        if(self.fileName):
            self.addTab()
        pass

    def fileWasChanged(self, path):
        print(path)
        index = self.isOpened(path)
        logging.debug(f" index = {index}")
        if index is False:
            self.fwatcher.removePath(path)
            return
        else:
            self.qTabW.widget(index).addText()
        pass

    def closeEvent(self, event):
        self.settings.setValueByAbbreviature("mwg", self.saveGeometry())
        self.settings.writeList("Recent", "file", self.recentFiles[:10])
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




