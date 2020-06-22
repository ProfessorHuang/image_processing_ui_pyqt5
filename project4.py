from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2
import numpy as np
import skimage.morphology as sm

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.source = QLabel(self)
        self.source.setAlignment(Qt.AlignCenter)

        self.processed = QLabel(self)
        self.processed.setAlignment(Qt.AlignCenter)
    
        openButton = QPushButton("Open Image", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)

        exeButton = QPushButton("Execute", self)
        exeButton.setCheckable(True)
        exeButton.clicked[bool].connect(self.execute)

        self.distanceType= QComboBox(self)
        self.distanceType.addItems([ 'euclidean', 'chessboard', 'city block'])

        self.opt = QComboBox(self)
        self.opt.addItems(['distance transform','skeleton','skeleton restoration'])

        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.source)
        hbox1.addWidget(self.processed)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.opt)
        hbox2.addWidget(self.distanceType)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(openButton)
        hbox3.addWidget(exeButton)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1,stretch=6)
        vbox.addLayout(hbox2,stretch=1)
        vbox.addLayout(hbox3,stretch=1)
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 560, 500)
        self.setWindowTitle('二值形态学高级')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        self.img = cv2.imread(self.img_name, 0)
        res,self.img = cv2.threshold(self.img,0,255,cv2.THRESH_OTSU)
        self.img_shape = self.img.shape
        if self.img_shape[0]>300 or self.img_shape[1]>300:
            self.img = cv2.resize(self.img, (300, 300), interpolation=cv2.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv2.imwrite('./image_to_show/source4.jpg', self.img)
        pixmap_source = QPixmap('./image_to_show/source4.jpg')
        self.source.setPixmap(pixmap_source)

    def execute(self):
        if self.opt.currentText() == 'distance transform':
            self.distance_transform()
        elif self.opt.currentText() == 'skeleton':
            self.skeleton()
        elif self.opt.currentText() == 'skeleton restoration':
            self.skeleton_restoration()

    def distance_transform(self):
        if self.distanceType.currentText() == 'euclidean':
            self.dis_type = cv2.DIST_L2
        elif self.distanceType.currentText() == 'chessboard':
            self.dis_type = cv2.DIST_C
        elif self.distanceType.currentText() == 'city block':
            self.dis_type = cv2.DIST_L1
        dis_map = cv2.distanceTransform(self.img,distanceType=self.dis_type, maskSize=3)
        dis_map = np.uint8(dis_map)
        dis_map_norm = ((dis_map-dis_map.min())/(dis_map.max()-dis_map.min())*255).astype(np.uint8)
        self.DT = dis_map_norm

        cv2.imwrite('./image_to_show/distance_transform.jpg', dis_map_norm)
        pixmap_dis_trans = QPixmap('./image_to_show/distance_transform.jpg')
        self.processed.setPixmap(pixmap_dis_trans)

    def skeleton(self):
        skeleton,distance_transform  = sm.medial_axis(self.img, return_distance=True)
        self.s_k = skeleton
        self.Dis_Trans = distance_transform
        cv2.imwrite('./image_to_show/skeleton.jpg', (255*skeleton).astype(np.uint8))
        pixmap_sk = QPixmap('./image_to_show/skeleton.jpg')
        self.processed.setPixmap(pixmap_sk)
        
    def skeleton_restoration(self):
        self.distance_transform()
        skeleton_res = 255*sm.reconstruction(self.s_k,self.Dis_Trans).astype(np.uint8)
        cv2.imwrite('./image_to_show/skeleton restoration.jpg', skeleton_res)
        pixmap_sk_res = QPixmap('./image_to_show/skeleton restoration.jpg')
        self.processed.setPixmap(pixmap_sk_res)


if __name__ == '__main__':

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')

    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
