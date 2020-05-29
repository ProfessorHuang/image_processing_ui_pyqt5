from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2
import matplotlib.pyplot as plt
import math

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.source = QLabel(self)
        self.source.setAlignment(Qt.AlignCenter)
        source_txt = QLabel('Source Image', self)
        source_txt.setAlignment(Qt.AlignCenter)

        self.binary = QLabel(self)
        self.binary.setAlignment(Qt.AlignCenter)
        binary_txt = QLabel('Binary Image', self)
        binary_txt.setAlignment(Qt.AlignCenter)

        self.processed = QLabel(self)
        self.processed.setAlignment(Qt.AlignCenter)
        processed_txt = QLabel('Processed Image', self)
        processed_txt.setAlignment(Qt.AlignCenter)


        openButton = QPushButton("Open Image", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)

        thresholdButton = QPushButton("Threshold", self)
        thresholdButton.setCheckable(True)
        thresholdButton.clicked[bool].connect(self.threshold)

        exeButton = QPushButton("Execute", self)
        exeButton.setCheckable(True)
        exeButton.clicked[bool].connect(self.execute)

        self.ksSlide = QSlider(Qt.Horizontal, self)
        self.ksSlide.setMinimum(5)
        self.ksSlide.setMaximum(15)
        self.ksSlide.setValue(5)
        self.ksSlide.valueChanged[int].connect(self.changeSliderValue)
        self.ksEditor = QLineEdit(self)
        self.ksEditor.setText('5')
        self.ksEditor.textChanged.connect(self.changeTextValue)


        self.kernel_shape = QComboBox(self)
        self.kernel_shape.addItems([ 'ellipse', 'cross', 'rectangle'])
        self.kernel_shape.currentIndexChanged.connect(self.setKernelShape)
        self.SE_shape = cv2.MORPH_ELLIPSE #default

        self.opt = QComboBox(self)
        self.opt.addItems(['dilation', 'erosion', 'opening', 'closing'])

        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(openButton)
        hbox1.addWidget(thresholdButton)
        hbox1.addWidget(exeButton)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.kernel_shape, Qt.AlignLeft)
        hbox2.addWidget(self.opt, Qt.AlignLeft)
        hbox2.addWidget(self.ksSlide,Qt.AlignRight)
        hbox2.addWidget(self.ksEditor, Qt.AlignRight)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(source_txt)
        hbox3.addWidget(binary_txt)
        hbox3.addWidget(processed_txt)

        hbox4 = QHBoxLayout(self)
        hbox4.addWidget(self.source)
        hbox4.addWidget(self.binary)
        hbox4.addWidget(self.processed)


        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1,stretch=1)
        vbox.addLayout(hbox2,stretch=1)
        vbox.addLayout(hbox3,stretch=1)
        vbox.addLayout(hbox4,stretch=6)
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 1000, 500)
        self.setWindowTitle('Project 3')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        self.img = cv2.imread(self.img_name, 0)
        self.img_shape = self.img.shape
        if self.img_shape[0]>300 or self.img_shape[1]>300:
            self.img = cv2.resize(self.img, (300, 300), interpolation=cv2.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv2.imwrite('./image_to_show/source.jpg', self.img)

        pixmap_source = QPixmap('./image_to_show/source.jpg')
        self.source.setPixmap(pixmap_source)

    def threshold(self):
        ret, thr = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU)
        self.binary_img = thr
        cv2.imwrite('./image_to_show/thr.jpg', thr)
        pixmap_binary = QPixmap('./image_to_show/thr.jpg')
        self.binary.setPixmap(pixmap_binary)

    def execute(self):
        kernel_size = int(self.ksSlide.value())
        kernel = cv2.getStructuringElement(self.SE_shape, (kernel_size, kernel_size))
        if self.opt.currentText() == 'dilation':
            processed_img = cv2.dilate(self.binary_img,kernel)
        elif self.opt.currentText() == 'erosion':
            processed_img = cv2.erode(self.binary_img,kernel)
        elif self.opt.currentText() == 'opening':
            processed_img = cv2.dilate(cv2.erode(self.binary_img,kernel),kernel)
        elif self.opt.currentText() == 'closing':
            processed_img = cv2.erode(cv2.dilate(self.binary_img,kernel),kernel)
        cv2.imwrite('./image_to_show/processed_img.jpg',processed_img)
        pixmap_pro = QPixmap('./image_to_show/processed_img.jpg')
        self.processed.setPixmap(pixmap_pro)

    def setKernelShape(self):
        if self.kernel_shape.currentText() == 'rectangle':
            self.SE_shape = cv2.MORPH_RECT
        elif self.kernel_shape.currentText() == 'cross':
            self.SE_shape = cv2.MORPH_CROSS
        elif self.kernel_shape.currentText() == 'ellipse':
            self.SE_shape = cv2.MORPH_ELLIPSE

    def changeSliderValue(self, value):
        self.ksEditor.setText(str(value))

    def changeTextValue(self, txt):
        self.ksSlide.setValue(int(txt))


if __name__ == '__main__':

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')


    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())