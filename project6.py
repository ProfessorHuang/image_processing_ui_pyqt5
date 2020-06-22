from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLineEdit)

from PyQt5.QtGui import (QPixmap,QImage)
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import math
import numpy as np
from time import sleep

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #打开图像按钮
        openButton = QPushButton("Open", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)
        #选择marker的按钮
        marker = QPushButton("Choose Marker", self)
        marker.setCheckable(True)
        marker.clicked[bool].connect(self.choosemarker)
        #选择模板的按钮
        template = QPushButton("Choose Template", self)
        template.setCheckable(True)
        template.clicked[bool].connect(self.choosetemplate)

        # 图像区域
        self.source_image = QLabel(self)
        self.source_image.setAlignment(Qt.AlignCenter)

        self.marker_image = QLabel(self)
        self.marker_image.setAlignment(Qt.AlignCenter)
        
        self.edge_image = QLabel(self)
        self.edge_image.setAlignment(Qt.AlignCenter)
        
        self.rec_image = QLabel(self)
        self.rec_image.setAlignment(Qt.AlignCenter)
        

        # 图像窗口和文字的水平布局
        hbox_image1 = QHBoxLayout(self)
        hbox_image1.addWidget(self.source_image)
        hbox_image1.addWidget(self.marker_image)
        
        hbox_image2 = QHBoxLayout(self)
        hbox_image2.addWidget(self.edge_image)
        hbox_image2.addWidget(self.rec_image)
        
        # 容纳水平布局的垂直布局vbox_image
        vbox_image = QVBoxLayout(self)
        vbox_image.addLayout(hbox_image1)
        vbox_image.addLayout(hbox_image2)

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
        self.opt.addItems(['edge detection','inner gradient','outer gradient','CBR','OBR','conditional dilation'])
        # 进行操作的按钮
        button_execute = QPushButton("execute", self)
        button_execute.setCheckable(True)
        button_execute.clicked[bool].connect(self.execute)

        # 创建选择框和按钮的两个水平布局
        hbox_SEinfo = QHBoxLayout(self)
        hbox_SEinfo.addWidget(self.opt)
        hbox_SEinfo.addWidget(self.shp)
        hbox_SEinfo.addWidget(self.kernel_size)
        hbox_SEinfo.addWidget(self.aEdit)

        hbox_buttion = QHBoxLayout(self)
        hbox_buttion.addWidget(openButton)
        hbox_buttion.addWidget(marker)
        hbox_buttion.addWidget(template)
        hbox_buttion.addWidget(button_execute)
        

        # 最终整体的布局
        vbox = QVBoxLayout(self)
        vbox.addLayout(vbox_image)
        vbox.addLayout(hbox_SEinfo)
        vbox.addLayout(hbox_buttion)

        # 定义一个Widget，用来容纳整体的布局内容
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        #整个窗口大小
        self.setGeometry(700, 200, 700, 700)
        self.setWindowTitle('灰度形态学高级')
        self.show()

        # 需要初始化的内容：一些self成员
        self.img_name = ''              #初始化图像名
        self.img_shape = (300, 300)     #初始化图形尺寸
        self.morphtype = cv.MORPH_RECT  #初始化结构元形状
        #self.kernelsize = int(self.kernel_size.value())                                  # 核大小
        #self.kernel = cv.getStructuringElement(self.morphtype,(kernelsize,kernelsize))   # 核形状

        # 读取原始图像
    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        img = cv.imread(self.img_name, 0)
        self.img_shape = img.shape
        if self.img_shape[0]>300 or self.img_shape[1]>300:
            img = cv.resize(img, (300, 300), interpolation=cv.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv.imwrite('./image_to_show/source.jpg', img)
        marker = QPixmap('./image_to_show/source.jpg')
        self.source_image.setPixmap(marker)
                       
        # 读取marker图像
    def choosemarker(self):
        self.markerimg_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        markerimg = cv.imread(self.markerimg_name, 0)
        self.markerimg_shape = markerimg.shape
        if self.markerimg_shape[0]>300 or self.markerimg_shape[1]>300:
            markerimg = cv.resize(markerimg, (300, 300), interpolation=cv.INTER_CUBIC)
            self.markerimg_shape = (300, 300)
        cv.imwrite('./image_to_show/marker.jpg', markerimg)
        markermap = QPixmap('./image_to_show/marker.jpg')
        self.marker_image.setPixmap(markermap)

        # 读取模板图像
    def choosetemplate(self):
        self.templateimg_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        templateimg = cv.imread(self.templateimg_name, 0)
        self.templateimg_shape = templateimg.shape
        if self.templateimg_shape[0]>300 or self.templateimg_shape[1]>300:
            templateimg = cv.resize(templateimg, (300, 300), interpolation=cv.INTER_CUBIC)
            self.templateimg_shape = (300, 300)
        cv.imwrite('./image_to_show/template.jpg', templateimg)
        templatemap = QPixmap('./image_to_show/template.jpg')
        self.source_image.setPixmap(templatemap)

        # 进行灰度形态学操作
    def execute(self):
        img = cv.imread('./image_to_show/source.jpg', 0)
        markerimg = cv.imread('./image_to_show/marker.jpg', 0)
        templateimg = cv.imread('./image_to_show/template.jpg', 0)
        kernelsize = int(self.kernel_size.value())                                  # 核大小
        kernel = cv.getStructuringElement(self.morphtype,(kernelsize,kernelsize))   # 核形状
        #进行不同的操作
        
        if self.opt.currentText() == 'edge detection':
            ero = cv.erode(img, kernel)
            dil = cv.dilate(img, kernel)
            result = dil - ero
            cv.imwrite("./image_to_show/edge.jpg", result)
            pixmap = QPixmap('./image_to_show/edge.jpg')
            self.edge_image.setPixmap(pixmap)
        elif self.opt.currentText() == 'inner gradient':
            ero = cv.erode(img, kernel)
            result = img - ero
            cv.imwrite("./image_to_show/gradient.jpg", result)
            pixmap = QPixmap('./image_to_show/gradient.jpg')
            self.edge_image.setPixmap(pixmap)
        elif self.opt.currentText() == 'outer gradient':
            dil = cv.dilate(img, kernel)
            result = dil - img 
            cv.imwrite("./image_to_show/gradient.jpg", result)
            pixmap = QPixmap('./image_to_show/gradient.jpg')
            self.edge_image.setPixmap(pixmap)
        elif self.opt.currentText() == 'OBR':
            result = self.O_R(kernelsize,img,cv.getStructuringElement(self.morphtype,(5,5)))
            cv.imwrite("./image_to_show/recon.jpg", result)
            pixmap = QPixmap('./image_to_show/recon.jpg')
            self.rec_image.setPixmap(pixmap)
        elif self.opt.currentText() == 'CBR':
            result = self.C_R(kernelsize,img,cv.getStructuringElement(self.morphtype,(5,5)))
            cv.imwrite("./image_to_show/recon.jpg", result)
            pixmap = QPixmap('./image_to_show/recon.jpg')
            self.rec_image.setPixmap(pixmap)
        elif self.opt.currentText() == 'conditional dilation':
            result = markerimg
            for num in range(1,500):
                result = cv.dilate(result,cv.getStructuringElement(self.morphtype,(3,3)) )
                result  = result&templateimg

            cv.imwrite("./image_to_show/conditinoal_dilation.jpg", result)
            pixmap = QPixmap('./image_to_show/conditinoal_dilation.jpg')
            self.rec_image.setPixmap(pixmap)
#####################################################################################################
#times是重复腐蚀膨胀的次数；f\g是输入的图像；b是结构元
#####################################################################################################
        #　测地膨胀
    def D_g(self,times,f,b,g):
        if times==0:
            return f
        if times==1:
            return np.min((cv.dilate(f,b,iterations=1),g),axis=0)
        return self.D_g(1,self.D_g(times-1,f,b,g),b,g)
 
    # 测地腐蚀
    def E_g(self,times,f,b,g):
        if times==0:
            return f
        if times==1:
            return np.max((cv.erode(f,b,iterations=1),g),axis=0)
        return self.E_g(1,self.E_g(times-1,f,b,g),b,g)
    
    # 膨胀重建
    def R_g_D(self,f,b,g):
        img = f
        while True:
            new = self.D_g(1,img,b,g)

            if (new==img).all():
                return img
            img = new
        
    # 腐蚀重建
    def R_g_E(self,f,b,g):
        img = f
        while True:
            new = self.E_g(1,img,b,g)

            if (new==img).all():
                return img
            img = new
 
    # 重建开操作
    def O_R(self,times,f,b,conn=np.ones((3,3))):
        picture=cv.erode(f,b,iterations=times)
        return self.R_g_D(picture,conn,f)
 
    # 重建闭操作
    def C_R(self,times,f,b,conn=np.ones((3,3))):
        picture = cv.dilate(f,b,iterations=times)
        return self.R_g_E(picture,conn,f)


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

