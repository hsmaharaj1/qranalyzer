from PyQt5 import uic, QtCore, QtWidgets, QtGui
import sys
import os
from cv2 import cv2
import numpy as np
import qrcode

class MWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MWindow, self).__init__()
        uic.loadUi("temp_new.ui", self)
        self.offset = None
        self.stop = False
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        # Handling the Events to create the effects on the Buttons
        self.closebtn.installEventFilter(self)
        self.minimize.installEventFilter(self)

        self.closebtn.clicked.connect(self.closefunc) 
        self.minimize.clicked.connect(self.minim)

        # For QR Analyzer
        self.create_btn.clicked.connect(self.create)
        self.open_btn.clicked.connect(self.fopen)
        self.copy_btn.clicked.connect(self.copy)
        


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)
    
    # Hovering Effect Testing
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            if object is self.closebtn:
                # print("Enter")
                self.closebtn.setText("X")
            if object is self.minimize:
                self.minimize.setText("_")
            self.stop = True
            return True
        elif event.type() == QtCore.QEvent.Leave:
            # print("Mouse is not over")
            self.closebtn.setText("")
            self.minimize.setText("")
            self.stop = False
        return False

    # Methods of Titlebar Buttons
    def closefunc(self):
        self.close()
    def minim(self):
        self.showMinimized()

    # Add Other Functions
    # For Generating QR Code
    def generate_qr(self, data):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("newqr.png")

    def create(self):
        global DATA
        DATA = self.data_box.toPlainText()
        self.generate_qr(DATA)
        self.dis_im = QtGui.QPixmap("./newqr.png")
        self.qr_display.setPixmap(self.dis_im)
        # print(DATA)

    # For reading QR
    def read_qr(self, image):
        global data_out
        img_r = cv2.imread(image)
        detect = cv2.QRCodeDetector()
        try:
            data_out, bbox, straight_qrcode = detect.detectAndDecode(img_r)
            if bbox is not None:
                self.text_data.append(data_out)
                _ = straight_qrcode
            else:
                self.text_data.append("No Data is Found")
        except:
            self.showDialog()

    def fopen(self):
        self.text_data.clear()
        try:
            img_file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
            self.read_qr(img_file[0])
            self.im = QtGui.QPixmap(img_file[0])
            self.qr_display.setPixmap(self.im)
        except:
            self.showDialog()

    def copy(self):
        QtWidgets.QApplication.clipboard().setText(data_out)
    
    def showDialog(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("Invalid Format of File Detected")
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

App = QtWidgets.QApplication(sys.argv)
window = MWindow()
window.show()
App.exec_()
