from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import urllib.request
import sys
import os
from os import path
import pafy
import humanize
from pytube import Playlist
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
        self.setFixedSize(551,285)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        #Youtube downloader buttons
        self.pushButton_6.clicked.connect(self.Download_YT_Video)
        self.pushButton_13.clicked.connect(self.Get_YT_Video)
        self.pushButton_5.clicked.connect(self.Save_Browse)
        #Youtube playlist downloader buttons
        self.pushButton_12.clicked.connect(self.Playlist_Download)
        self.pushButton_11.clicked.connect(self.Playlist_Browse)

    def Handel_Browse(self):
        save_Location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_Location[0]))

    #thread
    def Handel_Progress(self, blocknum, blocksize, totalsize):
        # self.thread = QThread(parent=self)
        # self.thread.start()
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
            QMessageBox.information(self, "Download error", "The download failed")
            return

        QMessageBox.information(self, "Download Completed", "The download finished")
        self.progressBar.setValue(int(0))
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

######################Youtube Downloader############

    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_6.setText(save)

    def Get_YT_Video(self):
        video_url = self.lineEdit_5.text()
        if video_url == "":
            QMessageBox.warning(self, "Data Error", "Provide a valid video url")
        else:
            video = pafy.new(video_url)
            streams = video.allstreams
            for stream in streams:
                size = humanize.naturalsize(stream.get_filesize())
                quality = "{} {} {}".format(stream.mediatype, stream.quality, size)
                self.comboBox.addItem(quality)
                #QApplication.processEvents()

    def Download_YT_Video(self):
        video_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()
        if video_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error", "Provide a valid video url")
        else:
            video = pafy.new(video_url)
            streams = video.allstreams
            quality = self.comboBox.currentIndex()
            down = streams[quality].download(filepath=save_location, callback=self.Video_progress)
            QMessageBox.information(self, "Download Completed", "The video download finished")
            self.progressBar_3.setValue(int(0))
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.comboBox.clear()

    def Video_progress(self, total, recived, ratio, speed, eta):
        read = recived

        if total > 0:
            download_percentage = read * 100 / total
            self.progressBar_3.setValue(int(download_percentage))
            QApplication.processEvents()  # not responding solve


#######################Playlist

    def Playlist_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_11.setText(save)

    def Playlist_Download(self):
        playlist_url = self.lineEdit_12.text()
        save_location = self.lineEdit_11.text()

        if playlist_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")
        else:
            playlist_video = Playlist(playlist_url)
            videos_number = len(playlist_video.video_urls)
            self.lcdNumber.display(videos_number)

        os.chdir(save_location)
        if os.path.exists(playlist_video.title):
            os.chdir(playlist_video.title)
        else:
            os.mkdir(playlist_video.title)
            os.chdir(playlist_video.title)

        current_video_downloaded = 1

        QApplication.processEvents()

        for video in playlist_video.videos:
            self.lcdNumber_2.display(current_video_downloaded)
            video.register_on_progress_callback(self.Playlist_progress)
            video.streams.get_lowest_resolution().download()
            QApplication.processEvents()
            current_video_downloaded +=1
        QMessageBox.information(self, "Download Completed", "The video download finished")
        self.progressBar_6.setValue(int(0))
        self.lcdNumber.display(int(0))
        self.lcdNumber_2.display(int(0))
        self.lineEdit_12.setText('')
        self.lineEdit_11.setText('')

    def Playlist_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        if total_size > 0:
            bytes_download = total_size - bytes_remaining
            precentage_of_complete = bytes_download / total_size * 100
            self.progressBar_6.setValue(int(precentage_of_complete))
            QApplication.processEvents()

    def Video_progress(self, total, recived, ratio, speed, eta):
        read = recived

        if total > 0:
            download_percentage = read * 100 / total
            self.progressBar_3.setValue(int(download_percentage))
            QApplication.processEvents()  # not responding solve

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    pafy.set_api_key('AIzaSyAYHWC3pdqHmXkSznaBzzA9Q04YwL1JFww')
    main()
