# coding:utf-8
import os
import glob
from tqdm import tqdm
import numpy as np
from PIL import Image
import cv2
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal
from view.Ui_PictureMode import Ui_PictureMode
from view.yolo import YOLO
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt5 import uic, QtCore
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager

class FolderWorker(QRunnable):
    finished = pyqtSignal()

    def __init__(self, folder, yolo, picture_show):
        super().__init__()
        self.folder = folder
        self.yolo = yolo
        self.picture_show = picture_show


    def run(self):
        img_names = os.listdir(self.folder)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith('.jpg'):
                image_path  = os.path.join(self.folder, img_name)
                image       = Image.open(image_path)
                r_image     = self.yolo.detect_image(image)
                if not os.path.exists('img_out/'):
                    os.makedirs('img_out/')
                r_image.save(os.path.join('img_out/', img_name.replace(".jpg", ".png")))

        pictures = glob.glob(os.path.join('img_out/', '*.png'))
        self.picture_show.clear()
        for picture in pictures:
            pixmap = QPixmap(picture)
            self.picture_resize(pixmap)


    def picture_resize(self, pixmap):
        if pixmap.width() > pixmap.height():
            pixmap = pixmap.scaledToWidth(675)
        else:
            pixmap = pixmap.scaledToHeight(675)
        # 创建一个灰色的背景
        background = QPixmap(675, 675)
        background.fill(QColor('gray'))
        # 将调整大小后的图片绘制到背景上
        painter = QPainter(background)
        painter.drawPixmap((675 - pixmap.width()) // 2, (675 - pixmap.height()) // 2, pixmap)
        painter.end()
        self.picture_show.addImage(background)

    def createSuccessInfoBar(self):
        InfoBar.success(
            title='success',
            content="所有图片都已识别完毕",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=1000,
            parent=self
        )


class PictureModeInterface(Ui_PictureMode, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # set the icon of button
        self.choose_one.clicked.connect(self.openPicture)
        self.choose_all.clicked.connect(self.openFolder)
        self.yolo = YOLO()
        self.threadpool = QThreadPool()

    def openPicture(self):
        picture = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if picture[0]:
            image = Image.open(picture[0])
            detect_picture = self.yolo.detect_image(image)
            detect_picture = np.array(detect_picture)
            detect_picture = cv2.cvtColor(detect_picture, cv2.COLOR_BGR2RGB)  # 加入这一行
            height, width, channel = detect_picture.shape
            self.picture_show.clear()
            qimage = QImage(detect_picture.data, width, height, 3*width, QImage.Format_RGB888).rgbSwapped()

            pixmap = QPixmap.fromImage(qimage)
            self.picture_resize(pixmap)

    def createCustomInfoBar(self):
        w = InfoBar.new(
            icon = FluentIcon.SYNC,
            title = '识别中',
            content="正在处理文件夹中的所有图片...",
            orient = Qt.Horizontal,
            isClosable = True,
            position = InfoBarPosition.BOTTOM,
            duration = 2000,
            parent = self
        )



    def picture_resize(self, pixmap):
        if pixmap.width() > pixmap.height():
            pixmap = pixmap.scaledToWidth(675)
        else:
            pixmap = pixmap.scaledToHeight(675)
        # 创建一个灰色的背景
        background = QPixmap(675, 675)
        background.fill(QColor('gray'))
        # 将调整大小后的图片绘制到背景上
        painter = QPainter(background)
        painter.drawPixmap((675 - pixmap.width()) // 2, (675 - pixmap.height()) // 2, pixmap)
        painter.end()
        self.picture_show.addImage(background)

    def openFolder(self):
        for filename in os.listdir('img_out/'):
            file_path = os.path.join('img_out/', filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        folder = QFileDialog.getExistingDirectory(self, 'Open Directory', '/home')

        if folder:
            self.createCustomInfoBar()
            worker = FolderWorker(folder, self.yolo, self.picture_show)
            self.threadpool.start(worker)

