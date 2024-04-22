# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MessageBox, SplitFluentWindow, FluentTranslator, setThemeColor
from qfluentwidgets import FluentIcon as FIF
from  view.picture_mode import PictureModeInterface
from  view.video_mode import VideoModeInterface

class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        # self.picturemodeInterface = PictureModeInterface(self)
        self.videomodeInterface = VideoModeInterface(self)
        setThemeColor('#FF7744')
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # add sub interface
        # self.addSubInterface(self.picturemodeInterface, FIF.PHOTO, '图片模式')
        self.addSubInterface(self.videomodeInterface, FIF.VIDEO, '视频模式')
        self.navigationInterface.setExpandWidth(280)

    def initWindow(self):
        self.resize(1000, 765)
        self.setWindowIcon(QIcon('logo/detetion.png'))
        self.setWindowTitle('纸板缺陷检测系统')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)

    # install translator
    # translator = FluentTranslator()
    # app.installTranslator(translator)

    w = Window()
    w.show()
    app.exec_()
