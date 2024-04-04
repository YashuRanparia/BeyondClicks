import logging as log
import math
import os
import sys
import time

import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector as htm
from PIL import Image, ImageQt
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QHBoxLayout,
                             QLabel, QPushButton, QStyledItemDelegate,
                             QTreeView, QVBoxLayout, QWidget)

import MyHandTrackingModule as htm

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)


from PyQt5.QtCore import QThread, QTimer, pyqtSignal


class VideoThread(QThread):

    frame_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.brushThickness = 15
        self.eraserThickness = 50
        self.delay = 15
        self.counter = 0
        self.drawColor = (0, 0, 255)
        pass

    def run(self):
        log.info("run()")
        white_img = np.full((720,1280,3),(255,255,255), dtype=np.uint8)
        self.vwb_img = cv2.cvtColor(white_img, cv2.COLOR_RGB2BGR)
    

        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        actual_width = cap.get(3)
        actual_hight = cap.get(4)
        log.info("Actual resolution: " + str(actual_width) + " x " + str(actual_hight))

        detector = htm.handDetector(detectionCon=0.85)

        xp, yp = 0, 0
        # imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        imgCanvas = np.full((720,1280,3),(255,255,255), dtype=np.uint8)
        # imgCanvas = cv2.cvtColor(imgCanvas, cv2.COLOR_RGB2BGR)

        fps = cap.get(cv2.CAP_PROP_FPS)
        print("FPS: ",fps)

        kernel = np.ones((5, 5), np.uint8)

        canvas = None

        # Threshold for noise
        noiseth = 800
        ptr = 0
        while True:
            start = time.time()
            success, self.image = cap.read()
            
            self.vwb_img = np.full((720,1280,3),(255,255,255), dtype=np.uint8)
            # self.vwb_img = cv2.cvtColor(white_img, cv2.COLOR_RGB2BGR)
            log.info("Frame: " + str(ptr+1))
            ++ptr

            #Saving the first frame for debugging purpose <-----------------------------
            if not os.path.exists("saved_image.jpg"):
                filename = 'saved_image.jpg'
                cv2.imwrite(filename, self.image)
                imgsa = Image.open('saved_image.jpg')
                imgsa.save('saved_image.jpg')

            if(success):
                self.image = cv2.flip(self.image, 1)
                img = detector.findHands(self.image)
                camera_frame = img
                lmList = detector.findPosition(img, draw=False)

            if (len(lmList) != 0):
                x0, y0 = lmList[4][1:]  #thumb
                x1, y1 = lmList[8][1:]  #Fore-finger
                x2, y2 = lmList[12][1:] #Middle-Finger

                #center point of the tip
                x = (x0+x1)//2
                y = (y0+y1)//2

                #Calculate the distance of the thumb tip and index tip
                dis = math.sqrt(((x1-x0) ** 2) + ((y1-y0) ** 2))
                print("Distance: ",dis)

                # check when fingers up
                fingers = detector.fingersUp()

                # selection mode - two fingers up
                condition = fingers[1] and fingers[2]

                # Writting condition
                condition2 = (dis < 60) and not fingers[2] and not fingers[3] and not fingers[4]

                #Clear board
                condition3 = fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]

                # if condition:
                #     xp, yp = 0, 0
                #     print("Selection time")

                #     if y1 < 115:
                #         if 250 < x1 < 400:
                #             self.header = self.overlayList[0]
                #             self.drawColor = (0, 0, 255)
                #         elif 470 < x1 < 640:
                #             self.header = self.overlayList[1]
                #             self.drawColor = (255, 0, 0)
                #         elif 690 < x1 < 845:
                #             self.header = self.overlayList[2]
                #             self.drawColor = (0, 255, 0)
                #         elif 880 < x1 < 1050:
                #             self.header = self.overlayList[3]
                #             self.drawColor = (0, 0, 0)
                #         elif 1080 < x1 < 1280:
                #             imgCanvas.fill(0)
                #     cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), self.drawColor, cv2.FILLED)

                if condition2:
                    cv2.circle(img, (x, y), 12, self.drawColor, cv2.FILLED)
                    print("Drawing time")
                    if xp == 0 and yp == 0:
                        xp, yp = x, y

                    if self.drawColor == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x, y), self.drawColor, self.eraserThickness)
                        cv2.line(imgCanvas, (xp, yp), (x, y), self.drawColor, self.eraserThickness)

                    else:
                        cv2.line(img, (xp, yp), (x, y), self.drawColor, self.brushThickness)
                        cv2.line(imgCanvas, (xp, yp), (x, y), self.drawColor, self.brushThickness)
                    xp, yp = x, y

                else:
                    xp = 0
                    yp = 0

                # if condition3:
                #     imgCanvas.fill(0)
                #     cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), self.drawColor, cv2.FILLED)
                    
                self.buttonPressed = True

            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, imgInv)
            img = cv2.bitwise_or(img, imgCanvas)


            vwb_rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(np.asarray(vwb_rgbImage), mode='RGB')
            qt_img = ImageQt.ImageQt(image)

            vwb_frame = QPixmap.fromImage(qt_img)

            cam_rgbImage = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(np.asarray(cam_rgbImage), mode='RGB')
            qt_img2 = ImageQt.ImageQt(img2)

            cam_frame = QPixmap.fromImage(qt_img2)

            # vwb_frame = self.to_Pixmap(img)
            # camera_frame = self.toPixmap(camera_frame)

            end = time.time()
            processing_time = end - start
            logg.info("Processing Time: " + str(processing_time))
            if processing_time < (1000 / fps):
                delay = int((1000 / fps) - processing_time) - 10
                time.sleep(delay / 1000)
                logg.info("Delay: " + str(delay))

            
            frame_data = {
                "vwb_frame": vwb_frame,
                "camera_frame": cam_frame
            }

            self.frame_signal.emit(frame_data)
                

    def to_Pixmap(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(np.asarray(img_rgb), mode='RGB')
        qt_img = ImageQt.ImageQt(im)

        pixmap = QPixmap.fromImage(qt_img)
        return pixmap
    

    def paramsInit(self):
        self.brushThickness = 15
        self.eraserThickness = 50
        self.delay = 15
        self.counter = 0
        self.buttonPressed = False
        self.drawColor = (0, 0, 255)


class VWBView(QWidget):
    
    def __init__(self):
        super().__init__()

        self.paramsInit()
        self.initUI()
        pass


    def initUI(self):
        h = 900
        w = 1600

        self.setGeometry(80,50,w,h)
        # self.showMaximized()
        self.setWindowTitle("Virtual Writting Board")

        self.label = QLabel()
        self.btn = QPushButton("Click Me", self)

        self.btn.clicked.connect(self.start)

        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.label)

        self.setLayout(layout)
        pass

    #Upgrade frames in View -> QLabel
    def upgrade_frame(self,frame_data):
        log.info("Upgrading frame.....")
        self.label.setPixmap(frame_data["vwb_frame"])
        log.info("Frame Upgraded!")
        pass

    #Start thread for capturing visuals
    def start(self):
        self.video = VideoThread()
        self.video.frame_signal.connect(self.upgrade_frame)
        self.video.start()

    #Params Initialization
    def paramsInit(self):
        self.brushThickness = 15
        self.eraserThickness = 50
        self.drawColor = (0, 0, 255)


    def setup(self):
        pass


if __name__ == "__main__":

    app = QApplication(sys.argv)
    demo = VWBView()
    demo.show()
    sys.exit(app.exec_())