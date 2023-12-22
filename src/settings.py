# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QSettings, QSize
import logging

class Settings(QSettings):

    initValues = {
    "mwg": {
        "key": "windows/mainWindow/geometry", "value": ""
        },
    "afg":{
        "key": "windows/addFile/geometry", "value": ""
        },
    }

    def __init__(self):
        logging.debug("Start app settings")
        QSettings.__init__(self)
        self.setValues()
        pass

    def setValues(self):
        keys = []
        keys = self.allKeys()
        # logging.debug(keys)
        for dk, v in self.initValues.items():
            if v["key"] not in keys:
                self.setValue(v["key"], v["value"])

    def getValueByAbbreviature(self, abbr: str):
        return self.value(self.initValues[abbr]["key"])

    def setValueByAbbreviature(self, abbr: str, value):
        self.setValue(self.initValues[abbr]["key"], value)
