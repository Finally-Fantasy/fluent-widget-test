# coding:utf-8

from PyQt5.QtWidgets import QWidget, QFileDialog
from view.Ui_VideoMode import Ui_VideoMode
from PyQt5.QtCore import  QUrl
from PyQt5.QtWidgets import QWidget

class VideoModeInterface(Ui_VideoMode, QWidget):
    video = ''

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.choose_video.clicked.connect(self.openVideo)
        self.choose_all.clicked.connect(self.playVideo)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.videoWidget)

    def openVideo(self):
        self.video = QFileDialog.getOpenFileName(self, 'Open file', '/home')

    def playVideo(self):
        self.videoWidget.setVideo(QUrl.fromLocalFile(r"D:/Users/kp/Videos/ccc/test.mp4"))
        self.videoWidget.play()
