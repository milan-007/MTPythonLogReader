#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
import logging

from src import LogReader
import info as f

from PySide2.QtCore import Qt, QCoreApplication, Signal, QIODevice, QTimer, qDebug

from PySide2.QtWidgets import QApplication

from PySide2.QtNetwork import QLocalServer, QLocalSocket


class SingleApplication(QApplication):


    messageAvailable = Signal(object)

    def __init__(self, argv, key):
        super().__init__(argv)
        self.m_socket = QLocalSocket()
        self.m_socket.connectToServer(key, QIODevice.WriteOnly)
        self._running = self.m_socket.waitForConnected(1000)

    def isRunning(self):
        return self._running


class SingleApplicationWithMessaging(SingleApplication):
    def __init__(self, argv, key):
        super().__init__(argv, key)
        self._key = key
        self._timeout = 1000
        self._serverError = False
        if not self.isRunning():
            self._server = QLocalServer(self)
            self._server.newConnection.connect(self.handleMessage)
            if not self._server.listen(self._key):
                self._server.removeServer(self._key)
                if not self._server.listen(self._key):
                    logging.error("Server  could not listen")
                    self._serverError = True

    def handleMessage(self):
        #qDebug("Handle")
        socket = self._server.nextPendingConnection()
        if socket.waitForReadyRead(self._timeout):
            #qDebug("před čtením")
            m = socket.readAll().data().decode('utf-8')
            # qDebug(m)
            self.messageAvailable.emit(m)
            socket.disconnectFromServer()
        else:
            qDebug(socket.errorString())

    def sendMessage(self, message):
        if self.isRunning():
            socket = QLocalSocket(self)
            socket.connectToServer(self._key, QIODevice.WriteOnly)
            qDebug("Connected")
            if not socket.waitForConnected(self._timeout):
                print(socket.errorString())
                return False
            if not isinstance(message, bytes):
                message = message.encode('utf-8')
            socket.write(message)
            qDebug(f"Odesláno: {message}")
            if not socket.waitForBytesWritten(self._timeout):
                print(socket.errorString())
                return False
            socket.disconnectFromServer()
            return True
        return False


def setAppPath(launcher: str):
    return os.path.dirname(launcher)


def setAppAttributes(a: QApplication):
    a.setApplicationName(f.applicationName)
    a.setOrganizationName(f.organisationName)
    a.setOrganizationDomain(f.web)
    pass


def setLogger(logPath: str, logFileName: str):
    logPath = os.path.join(f.appPath, logPath)
    os.makedirs(logPath, exist_ok=True)
    logFilePath = os.path.join(logPath, logFileName)
    logging.basicConfig(
        filename=logFilePath,
        format="%(asctime)s [%(levelname)s] %(module)s: %(lineno)d\
        %(funcName)s:  %(message)s",
        level=logging.DEBUG,
        datefmt='%d %H:%M:%S',
        filemode="w"
    )
    logger = logging.getLogger(f.applicationName)
    pass


if __name__ == '__main__':
    arg = sys.argv
#    if len(arg) < 2:
#    # finta
#        arg = [
#        '/home/milan/projects/python/LogRaederMT/launcher',
#        '/home/milan/projects/python/Download/logs/VideoSubtitle reader.log'
#        ]
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = SingleApplicationWithMessaging(arg, f.applicationName)
    setAppAttributes(app)
    os.environ['PYTHONUNBUFFERED'] = "TRUE"
    if app.isRunning():
        m = 'app is already running, but no message sent'
        if len(arg) > 1:
            m = arg[1]
        app.sendMessage(m)
        sys.exit()

    f.appPath = setAppPath(arg[0])
    setLogger("logs", "MTLogReader.log")
    f.QRCImagePath = ":/"
    file = "" if len(arg) < 2 else arg[1]
    window = LogReader.LogReader(file)
    app.messageAvailable.connect(window.handleMessage)
    window.show()
    if app._serverError:
        window.error("Unable to start communication server")
    sys.exit(app.exec_())
