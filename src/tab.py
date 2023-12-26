# This Python file uses the following encoding: utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtGui import QTextCursor, QTextDocument
from src import utils


class Tab(QtWidgets.QWidget):

    colorChanged = Signal(bool)

    def __init__(self, fileName):
        super().__init__()
        self.flength = 0
        self.renewed = False
        self.debuglvl = {
            "NOTSET": ['gray', ''],
            "DEBUG": ['blue', '']  ,
            "INFO": ['green', ''],
            "WARNING": ['orenge', ''],
            "ERROR": ['red', ''],
            "CRITICAL": ['white', 'red']
        }
        self.fileName = fileName
        self.searchStatus = False
        self.searchText = ""
        self.searchTextBackground = True
        self.logStyle = "logging"

        pass

    def tab(self):
        self.qtbView = QtWidgets.QTextBrowser(self)
        self.addText()
        self.qf = QtWidgets.QFrame()
        self.qf.setFrameShape(QtWidgets.QFrame.Box)

        grid = QtWidgets.QGridLayout(self)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.qtbView, 1, 1, 10, 10)
        self.setLayout(grid)
        return self

    def addText(self):
        content = ""
        with open(self.fileName, "r") as fh:
            info = QtCore.QFileInfo(self.fileName)
            flength = info.size()
            if self.renewed is True:
                content = '<font color="red"> File was renewed</font><br>'
                content += "==============================================<br>"
                self.renewed = False
            if flength < self.flength:
                self.flength = 0
                self.renewed = True
            if self.flength > 0:
                fh.seek(self.flength)
            while True:
                line = fh.readline()
                if not line:
                    break
                if self.logStyle == "logging":
                    line = self.convertLogging(line)
                    # print(line)
                content += line
            # print("All: ", content)
        if self.flength > 0:
            self.qtbView.append(content)
        else:
            self.qtbView.setHtml(content)
        self.flength = flength
        pass

    def convertLogging(self, line):
        line = line.replace(chr(32), "&nbsp;")
        for lvl in self.debuglvl.keys():
            if any(x in line for x in ['['+lvl+']', ' '+lvl+' ']):
                if self.debuglvl[lvl][1]:
                    spanb = f'<span style="background-color:{self.debuglvl[lvl][1]}>'
                    spane = '</span>'
                else:
                    spanb = ''
                    spane = ''
                    line = line.replace(lvl, spanb+self.setcolor(self.debuglvl[lvl][0]+spane, lvl))
                break
                    # line.replace(" ", "&nsp;")
        line = line + "<br>"
                    #print("&nbsp;"+line)
        return line

    def setcolor( self, color, text):
        rv = '<font color="'+color+'">' + text + '</font>'
        return rv

    def search(self, text, backward = None):
        print(text)
        flags = QTextDocument.FindFlags()
        if backward:
            flags = flags | QTextDocument.FindBackward
        self.searchText = text
        rv = self.qtbView.find(text, flags)
        pass





