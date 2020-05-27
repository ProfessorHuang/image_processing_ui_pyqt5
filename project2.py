from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLineEdit)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        openButton = QPushButton("Open", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)

        # 放置原图和卷积后图像的区域
        self.source_image = QLabel(self)
        self.source_image.setAlignment(Qt.AlignCenter)
        self.feature_map = QLabel(self)
        self.feature_map.setAlignment(Qt.AlignCenter)
        source_image_txt = QLabel('Source Image', self)
        source_image_txt.setAlignment(Qt.AlignCenter)
        feature_map_txt = QLabel('After Convolution', self)
        feature_map_txt.setAlignment(Qt.AlignCenter)
        hbox_image = QHBoxLayout(self)
        hbox_image_txt = QHBoxLayout(self)
        hbox_image.addWidget(self.source_image)
        hbox_image.addWidget(self.feature_map)
        hbox_image_txt.addWidget(source_image_txt)
        hbox_image_txt.addWidget(feature_map_txt)

        vbox_image = QVBoxLayout(self)
        vbox_image.addLayout(hbox_image_txt, stretch=1)
        vbox_image.addLayout(hbox_image, stretch=6)



        # 卷积核的输入区域，大小为3×3，最终放在vbox_conv中
        self.conv_number1 = QLineEdit('0.11', self)  #  默认值设置为0.33
        self.conv_number2 = QLineEdit('0.11', self)
        self.conv_number3 = QLineEdit('0.11', self)
        self.conv_number4 = QLineEdit('0.11', self)
        self.conv_number5 = QLineEdit('0.11', self)
        self.conv_number6 = QLineEdit('0.11', self)
        self.conv_number7 = QLineEdit('0.11', self)
        self.conv_number8 = QLineEdit('0.11', self)
        self.conv_number9 = QLineEdit('0.11', self)

        hbox_conv_line1 = QHBoxLayout(self)
        hbox_conv_line2 = QHBoxLayout(self)
        hbox_conv_line3 = QHBoxLayout(self)        

        hbox_conv_line1.addWidget(self.conv_number1)
        hbox_conv_line1.addWidget(self.conv_number2)
        hbox_conv_line1.addWidget(self.conv_number3)
        hbox_conv_line2.addWidget(self.conv_number4)
        hbox_conv_line2.addWidget(self.conv_number5)
        hbox_conv_line2.addWidget(self.conv_number6)
        hbox_conv_line3.addWidget(self.conv_number7)
        hbox_conv_line3.addWidget(self.conv_number8)
        hbox_conv_line3.addWidget(self.conv_number9)

        vbox_conv = QVBoxLayout(self)
        vbox_conv.addLayout(hbox_conv_line1)
        vbox_conv.addLayout(hbox_conv_line2)
        vbox_conv.addLayout(hbox_conv_line3)

        # 经典卷积核的选择
        self.cb = QComboBox(self)
        self.cb.addItems(['Roberts1', 'Roberts2', 'Prewitt1', 'Prewitt2', 'Sobel1', 'Sobel2'])
        self.cb.currentIndexChanged.connect(self.change_conv_filter)
        button_conv = QPushButton("conv", self)
        button_conv.setCheckable(True)
        button_conv.clicked[bool].connect(self.conv)
        
        hbox_select_conv = QHBoxLayout(self)
        hbox_select_conv.addWidget(self.cb)
        hbox_select_conv.addWidget(button_conv)


        # 最终整体的布局
        vbox = QVBoxLayout(self)
        vbox.addWidget(openButton)
        vbox.addLayout(vbox_image)
        vbox.addLayout(vbox_conv)
        vbox.addLayout(hbox_select_conv)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    

        self.setGeometry(700, 200, 700, 700)
        self.setWindowTitle('Project2')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        img = cv.imread(self.img_name, 0)
        self.img_shape = img.shape
        if self.img_shape[0]>300 or self.img_shape[1]>300:
            img = cv.resize(img, (300, 300), interpolation=cv.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv.imwrite('./image_to_show/source.jpg', img)

        pixmap_source = QPixmap('./image_to_show/source.jpg')
        self.source_image.setPixmap(pixmap_source)

    def conv(self):
        img = cv.imread('./image_to_show/source.jpg', 0)
        conv_filter = np.zeros([3,3])
        conv_filter[0][0] = self.conv_number1.text()
        conv_filter[0][1] = self.conv_number2.text()
        conv_filter[0][2] = self.conv_number3.text()
        conv_filter[1][0] = self.conv_number4.text()
        conv_filter[1][1] = self.conv_number5.text()
        conv_filter[1][2] = self.conv_number6.text()
        conv_filter[2][0] = self.conv_number7.text()
        conv_filter[2][1] = self.conv_number8.text()
        conv_filter[2][2] = self.conv_number9.text()

        feature = cv.filter2D(img, -1, conv_filter)
        cv.imwrite("./image_to_show/feature_map.jpg", feature)
        pixmap_feature_map = QPixmap('./image_to_show/feature_map.jpg')
        self.feature_map.setPixmap(pixmap_feature_map)

    def change_conv_filter(self):
        if self.cb.currentText() == 'Roberts1':
            self.conv_number1.setText('-1')
            self.conv_number2.setText('0')
            self.conv_number3.setText('0')
            self.conv_number4.setText('0')
            self.conv_number5.setText('1')
            self.conv_number6.setText('0')
            self.conv_number7.setText('0')
            self.conv_number8.setText('0')
            self.conv_number9.setText('0')
        elif self.cb.currentText() == 'Roberts2':
            self.conv_number1.setText('0')
            self.conv_number2.setText('-1')
            self.conv_number3.setText('0')
            self.conv_number4.setText('1')
            self.conv_number5.setText('0')
            self.conv_number6.setText('0')
            self.conv_number7.setText('0')
            self.conv_number8.setText('0')
            self.conv_number9.setText('0')
        elif self.cb.currentText() == 'Prewitt1':
            self.conv_number1.setText('-1')
            self.conv_number2.setText('-1')
            self.conv_number3.setText('-1')
            self.conv_number4.setText('0')
            self.conv_number5.setText('0')
            self.conv_number6.setText('0')
            self.conv_number7.setText('1')
            self.conv_number8.setText('1')
            self.conv_number9.setText('1')
        elif self.cb.currentText() == 'Prewitt2':
            self.conv_number1.setText('-1')
            self.conv_number2.setText('0')
            self.conv_number3.setText('1')
            self.conv_number4.setText('-1')
            self.conv_number5.setText('0')
            self.conv_number6.setText('1')
            self.conv_number7.setText('-1')
            self.conv_number8.setText('0')
            self.conv_number9.setText('1')
        elif self.cb.currentText() == 'Sobel1':
            self.conv_number1.setText('-1')
            self.conv_number2.setText('-2')
            self.conv_number3.setText('-1')
            self.conv_number4.setText('0')
            self.conv_number5.setText('0')
            self.conv_number6.setText('0')
            self.conv_number7.setText('1')
            self.conv_number8.setText('2')
            self.conv_number9.setText('1')
        elif self.cb.currentText() == 'Sobel2':
            self.conv_number1.setText('-1')
            self.conv_number2.setText('0')
            self.conv_number3.setText('1')
            self.conv_number4.setText('-2')
            self.conv_number5.setText('0')
            self.conv_number6.setText('2')
            self.conv_number7.setText('-1')
            self.conv_number8.setText('0')
            self.conv_number9.setText('1')
            


if __name__ == '__main__':
    # 判断是否有文件夹

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')


    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
