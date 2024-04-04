import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

from vwb import VideoThread

# class VideoThread(QtCore.QThread):
#     changePixmap = QtCore.pyqtSignal(QtGui.QImage)

#     def run(self):
#         cap = cv2.VideoCapture(0)  

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = frame.shape
#             bytesPerLine = ch * w
#             convertToQtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
#             p = convertToQtFormat.scaled(380, 300, QtCore.Qt.KeepAspectRatio)
#             self.changePixmap.emit(p)
#             self.msleep(30)  # Adjust the delay as needed

#         cap.release()


class Ui_Whiteboard_GUI(object):

    _vwb_width = 1450
    _vwb_height = 850

    def __init__(self):
        # self.setupUi()
        pass

    def setupUi(self, Whiteboard_GUI):
        Whiteboard_GUI.setObjectName("Whiteboard_GUI")
        Whiteboard_GUI.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(Whiteboard_GUI)
        self.centralwidget.setObjectName("centralwidget")

        self.whiteboard = QtWidgets.QLabel(self.centralwidget)
        self.whiteboard.setGeometry(QtCore.QRect(10, 50, self._vwb_width, self._vwb_height))
        self.whiteboard.setFrameShape(QtWidgets.QFrame.Box)
        self.whiteboard.setFrameShadow(QtWidgets.QFrame.Raised)
        self.whiteboard.setObjectName("whiteboard")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1580, 10, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.Red = QtWidgets.QPushButton(self.centralwidget)
        self.Red.setGeometry(QtCore.QRect(1580, 70, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Red.setFont(font)
        self.Red.setObjectName("Red")

        self.Green = QtWidgets.QPushButton(self.centralwidget)
        self.Green.setGeometry(QtCore.QRect(1580, 130, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Green.setFont(font)
        self.Green.setObjectName("Green")

        self.Blue = QtWidgets.QPushButton(self.centralwidget)
        self.Blue.setGeometry(QtCore.QRect(1580, 190, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Blue.setFont(font)
        self.Blue.setObjectName("Blue")

        self.Eraser = QtWidgets.QPushButton(self.centralwidget)
        self.Eraser.setGeometry(QtCore.QRect(1580, 250, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Eraser.setFont(font)
        self.Eraser.setObjectName("Eraser")

        self.Clear_Screen = QtWidgets.QPushButton(self.centralwidget)
        self.Clear_Screen.setGeometry(QtCore.QRect(1580, 310, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Clear_Screen.setFont(font)
        self.Clear_Screen.setObjectName("Clear_Screen")
        
        self.Camera = QtWidgets.QLabel(self.centralwidget)
        self.Camera.setGeometry(QtCore.QRect(1500, 700, 380, 201))
        self.Camera.setObjectName("Camera")


        Whiteboard_GUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Whiteboard_GUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        Whiteboard_GUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Whiteboard_GUI)
        self.statusbar.setObjectName("statusbar")
        Whiteboard_GUI.setStatusBar(self.statusbar)

        self.startVWB()

        self.retranslateUi(Whiteboard_GUI)
        QtCore.QMetaObject.connectSlotsByName(Whiteboard_GUI)
        pass

    def upgrade_frames(self,frame_data):
        self.whiteboard.setPixmap(frame_data["vwb_frame"])
        # self.Camera.setPixmap(frame_data["camera_frame"])
        pass
        
    def startVWB(self):
        self.vwb = VideoThread()
        self.vwb.frame_signal.connect(self.upgrade_frames)
        self.vwb.start()
        pass

    def set_image(self, image):
        self.Camera.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, Whiteboard_GUI):
        _translate = QtCore.QCoreApplication.translate
        Whiteboard_GUI.setWindowTitle(_translate("Whiteboard_GUI", "Whiteboard_GUI"))
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
    Whiteboard_GUI = QtWidgets.QMainWindow()
    ui = Ui_Whiteboard_GUI()
    ui.setupUi(Whiteboard_GUI)
    Whiteboard_GUI.show()
    sys.exit(app.exec_())
