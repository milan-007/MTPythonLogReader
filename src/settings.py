# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QSettings, QSize
import logging


class Settings(QSettings):

    def __init__(self, initValues):
        QSettings.__init__(self)
        logging.debug("Start settings")
        self.initValues = initValues
        self.setValues()
        pass

    def setValues(self):
        keys = []
        keys = self.allKeys()
        # logging.debug(keys)
        for dk, v in self.initValues.items():
            if v["key"] not in keys:
                self.setValue(v["key"], v["value"])
        pass

    def getValueByAbbreviature(self, abbr: str):
        return self.value(self.initValues[abbr]["key"])

    def setValueByAbbreviature(self, abbr: str, value):
        self.setValue(self.initValues[abbr]["key"], value)

    def writeList(self, group, key, values):
        self.remove(group)
        self.beginWriteArray(group)
        for i in range(len(values)):
            self.setArrayIndex(i)
            self.setValue(key,values[i])
        self.endArray()
        pass

    def readList(self, group, key):
        size = self.beginReadArray(group)
        output = []
        for i in range(size):
            self.setArrayIndex(i)
            value = self.value(key)
            output.append(value)
        self.endArray()
        return output


    def hasGroup(self, key):
        return len(self.childGroups(key)) > 0

#        keys = self.childKeys()
#        if self.hasGroup(key):


#        logging.debug(f"keys : {keys}")
#        # self.beginWriteArray(key)
#        # for i in range(key.size):
#        pass

