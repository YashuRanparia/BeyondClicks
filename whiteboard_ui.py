import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QHBoxLayout,
                             QLabel, QPushButton, QStyledItemDelegate,
                             QTreeView, QVBoxLayout, QWidget)

from vwb import VideoThread


class WhiteBoardUI(QWidget):

    _vwb_width = 1450
    _vwb_height = 850

    def __init__(self):
        super().__init__()
        self.setupUi()
        pass

    def setupUi(self):
        h = 1080
        w = 1920
        self.setGeometry(0,0,w,h)
        self.setWindowTitle("Virtual Writing Board")

        self.setObjectName("Whiteboard_GUI")
        self.resize(1920, 1080)
        

        self.whiteboard = QtWidgets.QLabel(self)
        self.whiteboard.setGeometry(QtCore.QRect(10, 50, self._vwb_width, self._vwb_height))
        self.whiteboard.setFrameShape(QtWidgets.QFrame.Box)
        self.whiteboard.setFrameShadow(QtWidgets.QFrame.Raised)
        self.whiteboard.setObjectName("whiteboard")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(1580, 10, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.Red = QtWidgets.QPushButton(self)
        self.Red.setGeometry(QtCore.QRect(1580, 70, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Red.setFont(font)
        self.Red.setObjectName("Red")

        self.Green = QtWidgets.QPushButton(self)
        self.Green.setGeometry(QtCore.QRect(1580, 130, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Green.setFont(font)
        self.Green.setObjectName("Green")

        self.Blue = QtWidgets.QPushButton(self)
        self.Blue.setGeometry(QtCore.QRect(1580, 190, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Blue.setFont(font)
        self.Blue.setObjectName("Blue")

        self.Eraser = QtWidgets.QPushButton(self)
        self.Eraser.setGeometry(QtCore.QRect(1580, 250, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Eraser.setFont(font)
        self.Eraser.setObjectName("Eraser")

        self.Clear_Screen = QtWidgets.QPushButton(self)
        self.Clear_Screen.setGeometry(QtCore.QRect(1580, 310, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Clear_Screen.setFont(font)
        self.Clear_Screen.setObjectName("Clear_Screen")
        
        self.Camera = QtWidgets.QLabel(self)
        self.Camera.setGeometry(QtCore.QRect(1500, 700, 380, 201))
        self.Camera.setObjectName("Camera")

        self.startVWB()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        pass

    def upgrade_frames(self,frame_data):
        camera_view_width = 380
        camera_view_height = 240

        self.whiteboard.setPixmap(frame_data["vwb_frame"])
        
        camera_frame_pixmap = frame_data["camera_frame"]
        
        new_size = QSize(camera_view_width, camera_view_height)
        resized_frame_pixmap = camera_frame_pixmap.scaled(new_size, Qt.KeepAspectRatio)
        self.Camera.setPixmap(resized_frame_pixmap)
        pass
        
    def startVWB(self):
        self.vwb = VideoThread()
        self.vwb.frame_signal.connect(self.upgrade_frames)
        self.vwb.start()
        pass

    def set_image(self, image):
        self.Camera.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.whiteboard.setText(_translate("Whiteboard_GUI", "TextLabel"))
        self.pushButton.setText(_translate("Whiteboard_GUI", "Pencil"))
        self.Red.setText(_translate("Whiteboard_GUI", "Red"))
        self.Green.setText(_translate("Whiteboard_GUI", "Green"))
        self.Blue.setText(_translate("Whiteboard_GUI", "Blue"))
        self.Eraser.setText(_translate("Whiteboard_GUI", "Eraser"))
        self.Clear_Screen.setText(_translate("Whiteboard_GUI", "Clear Screen"))
        self.Camera.setText(_translate("Whiteboard_GUI", "Camera"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WhiteBoardUI()
    ui.show()
    sys.exit(app.exec_())
