# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QFileInfo,\
    QDir,\
    QFile

from PySide2.QtGui import QIcon


from PySide2.QtWidgets import QStyle, QApplication


def fileExists(fileName: str) -> bool:
    fi = QFileInfo(fileName)
    return fi.exists and fi.isFile()


def smoothUrl(url: str) -> str:
    rules = {'/': "_", ".": "_", "?": "-", "=": "#"}
    fileName = url.split("//", 1)[1]
    for k, v in rules.items():
        fileName = fileName.replace(k, v)
    return fileName


def getIcon(iconName):
    if QFile.exists(iconName):
        return QIcon(iconName)
    defaultIcon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
    return QIcon.fromTheme(iconName, defaultIcon)


# if __name__ == "__main__":
#     pass
