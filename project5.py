from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLineEdit)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import math
import numpy as np


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #打开图像按钮
        openButton = QPushButton("Open", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)
        # 图像区域
        self.source_image = QLabel(self)
        self.source_image.setAlignment(Qt.AlignCenter)
        self.openclose = QLabel(self)
        self.openclose.setAlignment(Qt.AlignCenter)
        source_image_txt = QLabel('Source Image', self)
        source_image_txt.setAlignment(Qt.AlignCenter)
        openclose_txt = QLabel('After Open or Close', self)
        openclose_txt.setAlignment(Qt.AlignCenter)

        # 图像窗口和文字的两个水平布局
        hbox_image = QHBoxLayout(self)
        hbox_image_txt = QHBoxLayout(self)
        hbox_image.addWidget(self.source_image)
        hbox_image.addWidget(self.openclose)
        hbox_image_txt.addWidget(source_image_txt)
        hbox_image_txt.addWidget(openclose_txt)
        # 容纳水平布局的垂直布局vbox_image
        vbox_image = QVBoxLayout(self)
        vbox_image.addLayout(hbox_image_txt, stretch=1)
        vbox_image.addLayout(hbox_image, stretch=6)

        # 灰度形态学处理方法的选择区域

        # 定义SE尺寸的区域
        self.kernel_size = QSlider(Qt.Horizontal, self)
        self.kernel_size.setMinimum(3)
        self.kernel_size.setMaximum(25)
        self.kernel_size.setValue(3)
        self.kernel_size.valueChanged[int].connect(self.changeSliderValue)
        self.aEdit = QLineEdit(self)
        self.aEdit.setText('3')
        self.aEdit.textChanged.connect(self.changeTextValue)
        # 两个下拉选择框，一个选择SE形状，一个选择灰度形态学操作        
        self.shp = QComboBox(self)
        self.shp.addItems(['rectangle', 'cross', 'ellipse'])
        self.shp.currentIndexChanged.connect(self.setkernelshape)
        self.opt = QComboBox(self)
        self.opt.addItems(['dilation', 'erosion', 'opening','closing'])
        # 进行操作的按钮
        button_conv = QPushButton("go", self)
        button_conv.setCheckable(True)
        button_conv.clicked[bool].connect(self.conv)

        # 创建选择框和按钮的两个水平布局
        hbox_SEinfo = QHBoxLayout(self)
        hbox_SEinfo.addWidget(self.shp)
        hbox_SEinfo.addWidget(self.opt)
        hbox_SEinfo.addWidget(self.kernel_size)
        hbox_SEinfo.addWidget(self.aEdit)
        hbox_gobuttion = QHBoxLayout(self)
        hbox_gobuttion.addWidget(button_conv)

        # 最终整体的布局
        vbox = QVBoxLayout(self)
        vbox.addWidget(openButton)
        vbox.addLayout(vbox_image)
        vbox.addLayout(hbox_SEinfo)
        vbox.addLayout(hbox_gobuttion)
        # 定义一个Widget，用来容纳整体的布局内容
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        #整个窗口大小
        self.setGeometry(700, 200, 700, 700)
        self.setWindowTitle('Project5')
        self.show()

        # 需要初始化的内容：一些self成员
        self.img_name = ''              #初始化图像名
        self.img_shape = (300, 300)     #初始化图形尺寸
        self.morphtype = cv.MORPH_RECT  #初始化结构元形状

        # 读取原始图像
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
                       
        # 进行灰度形态学操作
    def conv(self):
        img = cv.imread('./image_to_show/source.jpg', 0)
        kernelsize = int(self.kernel_size.value())                            # 核大小
        kernel = cv.getStructuringElement(self.morphtype,(kernelsize,kernelsize))   # 核形状
        #进行不同的操作
        if self.opt.currentText() == 'dilation':
            result = cv.dilate(img, kernel)
        elif self.opt.currentText() == 'erosion':
            result = cv.erode(img, kernel)  
        elif self.opt.currentText() == 'opening':
            temp = cv.erode(img, kernel) 
            result = cv.dilate(temp, kernel)
        elif self.opt.currentText() == 'closing':
            temp = cv.dilate(img, kernel)
            result = cv.erode(temp, kernel) 

        #结果保存和显示
        cv.imwrite("./image_to_show/result.jpg", result)
        pixmap_openclose = QPixmap('./image_to_show/result.jpg')
        self.openclose.setPixmap(pixmap_openclose)

        # 根据选择情况将不同SE形状赋给self.morphtype
    def setkernelshape(self):
        if self.shp.currentText() == 'rectangle':
            self.morphtype = cv.MORPH_RECT
        elif self.shp.currentText() == 'cross':
            self.morphtype = cv.MORPH_CROSS  
        elif self.shp.currentText() == 'ellipse':
            self.morphtype = cv.MORPH_ELLIPSE
               
        # 显示滑块控件当前位置值
    def changeSliderValue(self, value):
        self.aEdit.setText(str(value))
        # 将SE尺寸设置为当前值
    def changeTextValue(self, txt):
        self.kernel_size.setValue(int(txt))
                       
if __name__ == '__main__':
    # 判断是否有文件夹

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')


    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
