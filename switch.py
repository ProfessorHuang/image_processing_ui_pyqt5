import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QHBoxLayout, QVBoxLayout, QWidget
import project1
import project2
import project3
import project4
import project5
import project6


class mainWindow(QMainWindow):

    sig_1 = pyqtSignal()
    sig_2 = pyqtSignal()
    sig_3 = pyqtSignal()
    sig_4 = pyqtSignal()
    sig_5 = pyqtSignal()
    sig_6 = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(300, 200)
        self.setWindowTitle('image_processing_ui')

        self.btn_1 = QPushButton(self)
        self.btn_1.setText('project1')
        self.btn_1.clicked.connect(self.slot_btn_1)
        self.sig_1.connect(self.sig_1_slot)

        self.btn_2 = QPushButton(self)
        self.btn_2.setText('project2')
        self.btn_2.clicked.connect(self.slot_btn_2)
        self.sig_2.connect(self.sig_2_slot)

        self.btn_3 = QPushButton(self)
        self.btn_3.setText('project3')
        self.btn_3.clicked.connect(self.slot_btn_3)
        self.sig_3.connect(self.sig_3_slot)

        self.btn_4 = QPushButton(self)
        self.btn_4.setText('project4')
        self.btn_4.clicked.connect(self.slot_btn_4)
        self.sig_4.connect(self.sig_4_slot)

        self.btn_5 = QPushButton(self)
        self.btn_5.setText('project5')
        self.btn_5.clicked.connect(self.slot_btn_5)
        self.sig_5.connect(self.sig_5_slot)

        self.btn_6 = QPushButton(self)
        self.btn_6.setText('project6')
        self.btn_6.clicked.connect(self.slot_btn_6)
        self.sig_6.connect(self.sig_6_slot)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.btn_1)
        vbox.addWidget(self.btn_2)
        vbox.addWidget(self.btn_3)
        vbox.addWidget(self.btn_4)
        vbox.addWidget(self.btn_5)
        vbox.addWidget(self.btn_6)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

      

    def slot_btn_1(self):
        self.sig_1.emit()

    def sig_1_slot(self):
        self.t = project1.mainWindow()
        self.t.show()


    def slot_btn_2(self):
        self.sig_2.emit()

    def sig_2_slot(self):
        self.t = project2.mainWindow()
        self.t.show()


    def slot_btn_3(self):
        self.sig_3.emit()

    def sig_3_slot(self):
        self.t = project3.mainWindow()
        self.t.show()


    def slot_btn_4(self):
        self.sig_4.emit()
        
    def sig_4_slot(self):
        self.t = project4.mainWindow()
        self.t.show()


    def slot_btn_5(self):
        self.sig_5.emit()
        
    def sig_5_slot(self):
        self.t = project5.mainWindow()
        self.t.show()


    def slot_btn_6(self):
        self.sig_6.emit()
        
    def sig_6_slot(self):
        self.t = project6.mainWindow()
        self.t.show()

def ui_main():
    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    ui_main()
