#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
import sys
import os
import logging

from PySide2.QtGui import QTextCursor, QColor, QScreen, QTextDocument
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextBrowser
from PySide2.QtCore import QFile, Slot, QFileSystemWatcher, QFileInfo, QCoreApplication, Qt, QPoint
from PySide2.QtUiTools import QUiLoader

import warning

class Reader(QMainWindow):
    def __init__(self):
        super(Reader, self).__init__()
        self.load_ui()
        self.fwatcher = QFileSystemWatcher()
        self.fwatcher.fileChanged.connect(self.fileWasChanged)
        self.flength = 0
        self.renewed = False

        self.warn = warning.Warning(self)
        self.debuglvl = {
        "NOTSET": ['gray', ''],
        "DEBUG": ['blue', '']  ,
        "INFO": ['green', ''],
        "WARNING": ['orenge', ''],
        "ERROR": ['red', ''],
        "CRITICAL": ['white', 'red']
        }


    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        # center window
        point = self.ui.frameGeometry()
        # print(point)
        screenCenterPoint = QScreen.availableGeometry(
            QApplication.primaryScreen()).center()
        # print( screenCenterPoint )
        point.moveCenter(screenCenterPoint)

        self.ui.move(point.topLeft())

        self.ui.action_Open_file.triggered.connect(self.readFile)
        self.ui.action_Search.triggered.connect(self.doSearch)
        self.ui.qpb_SearchClose.clicked.connect(self.closeSearch)
        self.ui.qpb_SearchBw.clicked.connect(self.searchBw)
        self.ui.qpb_SearchFw.clicked.connect(self.searchFw)
        self.ui.qle_SearchText.textChanged.connect(self.searchTextchanged)
        self.ui.searchFrame.setVisible(False)

        palette = self.ui.qle_SearchText.palette()
        self.ui.qle_SearchText.setAutoFillBackground(True)

        self.qle_SearchTextOriginalBg = palette.color(self.ui.qle_SearchText.backgroundRole())
        self.qle_SearchTextColorChanged = False
        self.ui.show()

    @Slot()
    def readFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open file"),
            None,
            self.tr("Any file (*)"),
            options=QFileDialog.DontUseNativeDialog
            )
        # print( type( fileName ), fileName )
        if(fileName):
            self.readAndWatchFile(fileName)

    def doSearch(self):
        self.ui.searchFrame.setVisible(True)
        self.ui.qle_SearchText.setFocus()

    def closeSearch(self):
        self.ui.searchFrame.setVisible(False)

    def searchBw(self):
        # self.ui.textBrowser.moveCursor(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
        self.search(self.ui.qpb_SearchBw, False)
        pass

    def searchFw(self):
        self.search(self.ui.qpb_SearchFw)
        pass

    def searchTextchanged(self):
        self.ui.textBrowser.moveCursor(QTextCursor.Start, QTextCursor.MoveAnchor)
        self.search(self.ui.qle_SearchText)


    def search(self, widget, forward: bool=True):
        text = self.ui.qle_SearchText.text()
        if text:
            way = None
            if not forward:
                way = QTextDocument.FindBackward

            if way is None:
                rv = self.ui.textBrowser.find(text)
            else:
                rv = self.ui.textBrowser.find(text, way)
            if not rv:
                pos = widget.mapToGlobal(QPoint(10, -20))
                self.warn.msg(self.tr("Not found"), 1, "", 1000, pos)
                if not self.qle_SearchTextColorChanged:
                    self.setqleBg(self.ui.qle_SearchText, "#ffc5d0")
                    self.qle_SearchTextColorChanged = True
            else:
                if self.qle_SearchTextColorChanged:
                    self.setqleBg(self.ui.qle_SearchText, self.qle_SearchTextOriginalBg)
                    self.qle_SearchTextColorChanged = False

    def readAndWatchFile(self, fname: str):
        watchedFiles = self.fwatcher.files()
        logger.debug(watchedFiles)
        if watchedFiles:
            self.fwatcher.removePaths(watchedFiles)
        self.fwatcher.addPath(fname)
        self.fname = fname
        logger.debug(fname)
        self.fillBrowser()

    def fillBrowser(self):
        content = ""
        with open(self.fname, "r") as fh:
            info = QFileInfo(self.fname)
            flength = info.size()
            # print("Length: ", flength, "Saved: ", self.flength)
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
                line = self.loggerConvert(line)
                # print(line)
                content += line
        # print("All: ", content)
        if self.flength > 0:
            self.ui.textBrowser.append(content)
        else:
            self.ui.textBrowser.setHtml(content)
        self.flength = flength

    @Slot(str)
    def fileWasChanged(self, path):
        #        print(type(path))
        #        print(self.fwatcher.files())
        self.fillBrowser()

    def loggerConvert(self, line):
#        encLine = str.encode(line)
#        dict = [encLine[i:i+1] for i in range(len(encLine))]
#        print(dict)
        pos = line.index(chr(32))
        #print(pos)
        line = line.replace(chr(32), "&nbsp;")
        for lvl in self.debuglvl.keys():
            if any ( x in line for x in [ '['+lvl+']', ' '+lvl+' ']) :
                if self.debuglvl[lvl][1]:
                    spanb = f'<span style="background-color:{self.debuglvl[lvl][1]}>'
                    spane = '</span>'
                else:
                    spanb = ''
                    spane = ''
                line = line.replace(lvl, spanb+self.setcolor( self.debuglvl[lvl][0]+spane, lvl))
                break;
        # line.replace(" ", "&nsp;")
        line = line + "<br>"
        #print("&nbsp;"+line)
        return line

    def setcolor( self, color, text):
        rv = '<font color="'+color+'">' + text + '</font>'
        return rv

    def setqleBg(self, item, color):
        pal = item.palette()
        pal.setColor(item.backgroundRole(), QColor(color))
        item.setPalette(pal)

    def tr(self, text):
        trs = QApplication.translate("MainWindow", text)
        if trs is None:
            trs = text
        return trs

if __name__ == "__main__":
    logFilename = os.path.dirname(__file__) + "/logreader.log"
    logging.basicConfig(
        filename=logFilename,
        format="%(asctime)s [%(levelname)s] %(module)-20s\
        %(funcName)s:  %(message)s",
        level=logging.DEBUG,
        datefmt='%d %H:%M:%S',
        filemode="w"
        )
    logger = logging.getLogger("logger")

    filename = ''
#    filename = '/home/milan/projects/python/Download/logs/VideoSubtitle reader.log'
    logger.debug(sys.argv)

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        logger.debug(filename)

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])


    widget = Reader()
    if filename:
        widget.readAndWatchFile(filename)
    # widget.ui.show()
    sys.exit(app.exec_())
