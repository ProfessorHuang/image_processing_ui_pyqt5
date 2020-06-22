from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import matplotlib.pyplot as plt
import math

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl_source = QLabel(self)
        self.lbl_source.setAlignment(Qt.AlignCenter)
        self.lbl_hist = QLabel(self)
        self.lbl_hist.setAlignment(Qt.AlignCenter)
        self.lbl_autoThres = QLabel(self)
        self.lbl_autoThres.setAlignment(Qt.AlignCenter)
        self.lbl_manualThres = QLabel(self)
        self.lbl_manualThres.setAlignment(Qt.AlignCenter)

        openButton = QPushButton("Open", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)
        thresButton = QPushButton("ManualThresh", self)
        thresButton.setCheckable(True)
        thresButton.clicked[bool].connect(self.manualThres)

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setMinimum(0)
        self.sld.setMaximum(255)
        self.sld.setValue(100)
        self.sld.valueChanged[int].connect(self.changeSliderValue)
        self.aEdit = QLineEdit(self)
        self.aEdit.setText('100')
        self.aEdit.textChanged.connect(self.changeTextValue)

        self.cb = QComboBox()
        self.cb.addItems(['otsu', 'entropy'])
        autoThresButton = QPushButton("auto", self)
        autoThresButton.setCheckable(True)
        autoThresButton.clicked[bool].connect(self.autoThres)
   
        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.lbl_source)
        hbox1.addWidget(self.lbl_hist)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.lbl_autoThres)
        hbox2.addWidget(self.lbl_manualThres)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(openButton)
        hbox3.addStretch(1)
        hbox3.addWidget(self.cb)
        hbox3.addWidget(autoThresButton)
        hbox3.addStretch(1)
        hbox3.addWidget(self.sld)
        hbox3.addWidget(self.aEdit)
        hbox3.addWidget(thresButton)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 700, 700)
        self.setWindowTitle('直方图与阈值化')
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

        hist = cv.calcHist([img], [0], None, [256], [0, 256])
        plt.figure(figsize=(3, 3))
        plt.hist(hist, bins=100, color='black')
        plt.xlim([0, 256])
        plt.savefig('./image_to_show/hist.png')
        img_hist = cv.imread('./image_to_show/hist.png')
        img_hist_scaled = cv.resize(img_hist, self.img_shape, interpolation=cv.INTER_CUBIC)
        cv.imwrite('./image_to_show/img_hist.jpg', img_hist_scaled)


        self.Otsu(img)
        self.Entropy(img)

        pixmap_source = QPixmap('./image_to_show/source.jpg')
        self.lbl_source.setPixmap(pixmap_source)

        pixmap_hist = QPixmap('./image_to_show/img_hist.jpg')
        self.lbl_hist.setPixmap(pixmap_hist)


    def Otsu(self, img):
        ret, binary_img = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
        binary_img = cv.resize(binary_img, self.img_shape, interpolation=cv.INTER_CUBIC)
        cv.imwrite("./image_to_show/autoThres.jpg", binary_img)

    def Entropy(self, img):
        H_last = 0  # 上一个H总熵
        best_k = 0  # 最佳阈值
        hist = cv.calcHist([img], [0], None, [256], [0, 256])  # 255*1的灰度直方图的数组
        # for i in range(256):
        #   p.insert(i, hist[i][0] / img.size)
        for k in range(1, 256):
            H_b = 0  # black的熵，前景的平均信息量
            H_w = 0  # white的熵，背景的平均信息量
            num_b = sum(hist[0:k])[0]
            num_w = sum(hist[k:256])[0]
            if num_b == 0 or num_w == 0:
                continue

            assert (num_w == img.size - num_b)
            for i in range(k):
                p = hist[i][0] / num_b
                if abs(p - 1.0) < 1e-6:
                    p = 1 - 1e-6
                if abs(p) > 1e-6:
                    H_b = H_b - p * math.log(p)

            for i in range(k, 256):
                p = hist[i][0] / num_w
                if abs(p - 1.0) < 1e-6:
                    p = 1 - 1e-6
                if abs(p) > 1e-6:
                    H_w = H_w - p * math.log(p)

            H = H_b + H_w
            if H > H_last:
                H_last = H
                best_k = k
        ret, binary_img = cv.threshold(img, best_k, 255, cv.THRESH_BINARY)
        binary_img = cv.resize(binary_img, self.img_shape, interpolation=cv.INTER_CUBIC)
        cv.imwrite("./image_to_show/autoThres.jpg", binary_img)

    def manualThres(self):
        img = cv.imread(self.img_name, 0)
        thres = self.sld.value()
        ret, binary_img = cv.threshold(img, thres, 255, cv.THRESH_BINARY)
        binary_img = cv.resize(binary_img, self.img_shape, interpolation=cv.INTER_CUBIC)
        cv.imwrite("./image_to_show/manualThres.jpg", binary_img)

        pixmap_manualThres = QPixmap('./image_to_show/manualThres.jpg')
        self.lbl_manualThres.setPixmap(pixmap_manualThres)

    def autoThres(self):
        img = cv.imread(self.img_name, 0)
        if self.cb.currentText() == 'otsu':
            self.Otsu(img)
        if self.cb.currentText() == 'entropy':
            self.Entropy(img)

        pixmap_autoThres = QPixmap('./image_to_show/autoThres.jpg')
        self.lbl_autoThres.setPixmap(pixmap_autoThres)



    def changeSliderValue(self, value):
        self.aEdit.setText(str(value))

    def changeTextValue(self, txt):
        self.sld.setValue(int(txt))





if __name__ == '__main__':
    # 判断是否有文件夹

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')


    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())

