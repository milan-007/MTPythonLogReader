# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QWidget, QDialog, QLabel, QTextBrowser, QGridLayout, QSizePolicy
from PySide2.QtGui import QPalette,\
    QColor
from PySide2.QtCore import \
    QTimer,\
    Qt


class Warning(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.textArea = QLabel()
        self.textArea.setAutoFillBackground(True)
        centralWidget = QWidget()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.textArea)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumWidth(20)

        self.parent = parent

        # self.add(centralWidget)
        self.setLayout(mainLayout)
        self.textArea.setText("pokus")

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.warnClose)
        self.timer.setInterval(500)
        pass

    def msg(self, text: str, level: int=0, color="", period: int=0, pos=False):
        if level == 0:
            bg = "#fdfdfd"
            delay = 500
        if level == 1:
            bg = "#fff94a"
            delay = 2000
        if level > 1:
            bg = "#ffaba5"
            delay = 5000
        color = color if color else bg
        delay = period if period else delay
        if pos:
            # print(pos)
            self.move(pos)
        self.timer.setInterval(delay)
        pal = self.textArea.palette()
        pal.setColor(self.textArea.backgroundRole(), QColor(bg))
        self.textArea.setPalette(pal)
        self.textArea.setText(text)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        #self.setMaximumHeight(height)
        self.timer.start()
        self.show()
        pass

    def warnClose(self):
        self.close()

