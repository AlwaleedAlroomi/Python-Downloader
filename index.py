from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import urllib.request
import sys
import os
from os import path

ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()

    def Handel_UI(self):
        self.setWindowTitle('Python Downloader')
        self.setFixedSize(526,285)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)

    def Handel_Browse(self):
        pass

    def Handel_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize  > 0:
            download_percentage = read * 100 / totalsize
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()  #not responding solve

    def Download(self):
        url = self.lineEdit.text()
        saveLocation = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, saveLocation, self.Handel_Progress)
        except Exception:
            QMessageBox.information(self, "Download error", "The download failed", button=event.accept())
            return

        QMessageBox.information(self, "Download Completed", "The download finished")
        self.progressBar.setValue(int(0))
        self.lineEdit.setText('')
        self.pushButton_2.setText('')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
