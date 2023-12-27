# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QFileInfo,\
    QDir,\
    QFile

from PySide2.QtGui import QIcon, QColor


from PySide2.QtWidgets import QStyle, QApplication

import logging
import pprint
import info as f


def fileExists(fileName: str) -> bool:
    fi = QFileInfo(fileName)
    return fi.exists and fi.isFile()


def smoothUrl(url: str) -> str:
    rules = {'/': "_", ".": "_", "?": "-", "=": "#"}
    fileName = url.split("//", 1)[1]
    for k, v in rules.items():
        fileName = fileName.replace(k, v)
    return fileName

def setItemColor(item, color = None, bg = None):
    logging.debug(f"Item : {pprint.pformat(str(item))}")
    pal = item.palette()
    if color:
        pal.setColor(item.foregroundRole(), QColor(color))
    if bg:
        pal.setColor(item.backgroundRole(), QColor(bg))
    item.setPalette(pal)


def getIcon(iconName):
    if QFile.exists(iconName):
        return QIcon(iconName)
    # print(f.QRCImagePath)
    if not iconName.startswith(f.QRCImagePath):
        rc_iconName = f.QRCImagePath + iconName
        if QFile.exists(rc_iconName):
            return QIcon(rc_iconName)
    defaultIcon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
    return QIcon.fromTheme(iconName, defaultIcon)


# if __name__ == "__main__":
#     pass
