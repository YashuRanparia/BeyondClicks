import logging as log
import os
import sys

import aspose.pydrawing as drawing
import aspose.slides as slides
import cv2
import numpy as np
import win32com.client
from cvzone.HandTrackingModule import HandDetector as htm
from fitz import fitz
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QLabel, QListWidget, QMainWindow,
                             QPushButton, QStackedWidget, QTextEdit,
                             QVBoxLayout, QWidget)

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)

class SmartPresentation:

    def __init__(self) -> None:

        #params
        self.width, self.height = 900, 720
        self.gestureThreshold = 300
        self.maxZoomFactor = 2
        self.minZoomFactor = 1
        self.zoomFactor = 1
        print("Params initiallized Successfully!")

        #HandTracker
        self.detector = htm(detectionCon=0.8, maxHands=1)
        print("HandTracker instance created successfully!")
        pass

    def saveSlides(self,pdf_path):
        output_format = 18  # 17 corresponds to PNG format

        # pdf_path = "presentation.pdf"
        # presentation.SaveAs(pdf_path, FileFormat=32)

        pdf_doc = fitz.open(pdf_path)

        for page_num in range(len(pdf_doc)):  # Loop through each page (slide)
            page = pdf_doc[page_num]
            zoom = 2
            slide_image = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom))  # Extract the page image
            slide_image.save(f"slide_{page_num + 1}.png")

        # for slide in presentation.Slides:
        #     print(type(slide))
        #     # Specify the path and filename for the output image
        #     image_path = f"slide_{slide.SlideIndex}.pdf"
        
        #     # Save the slide as an image using the chosen format
        #     slide.Export(image_path, "JPG")
        pass

    def initPresentation(self, path):
        self.Application = win32com.client.Dispatch("PowerPoint.Application")
        self.Presentation = self.Application.Presentations.Open(path)
        print(self.Presentation.Name)

        pdf_path = "C:\\Users\\yashu\\Desktop\\FFE_Mentorship_Program\\Session_1\\presen1.pdf"
        self.Presentation.SaveAs(pdf_path, FileFormat=32)

        self.saveSlides(pdf_path)
        self.Presentation.SlideShowSettings.Run()

        self.setup()
        self.start()


    def setup(self):

        # Variables
        self.imgList = []
        self.delay = 30
        self.buttonPressed = False
        self.counter = 0
        self.drawMode = False
        self.imgNumber = 20
        self.delayCounter = 0
        self.annotations = [[]]
        self.annotationNumber = -1
        self.annotationStart = False

        print("Variable initiallization done Successfully!")
        # pptLength = len(self.Presentation.slides)
        # print("Total Slides : ", pptLength)

    def start(self):
        print("Started")
        #camera must be ready
        cap = cv2.VideoCapture(0)
        cap.set(3, self.width)
        cap.set(4, self.height)
        print("Camera Setup Done Successfully!")

        while True:
            success, image = cap.read()
            imgCurrent = image.copy()
            image = cv2.flip(image, 1)
            hands, img = self.detector.findHands(image)

            if(hands and self.buttonPressed is False):
                hand = hands[0]
                lmList = hand["lmList"]
                fingers = self.detector.fingersUp(hand)

                #condition for next
                condition = not fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]

                #condition for previous
                condition_prev = fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]

                #condition for close
                condition_close = fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]

                if(condition):
                    print("Next")
                    self.buttonPressed = True
                    if self.imgNumber > 0:
                        self.Presentation.SlideShowWindow.View.Next()
                        self.annotations = [[]]
                        self.annotationNumber = -1
                        self.annotationStart = False
                elif(condition_prev):
                    print("Previous")
                    self.buttonPressed = True
                    if self.imgNumber > 0:
                        self.Presentation.SlideShowWindow.View.Previous()
                        self.imgNumber += 1
                        self.annotations = [[]]
                        self.annotationNumber = -1
                        self.annotationStart = False
                elif(condition_close):
                    self.close()
                    break
            else:
                self.annotationStart = False

            if self.buttonPressed:
                self.counter += 1
                if self.counter > self.delay:
                    self.counter = 0
                    self.buttonPressed = False

            for i, annotation in enumerate(self.annotations):
                for j in range(len(annotation)):
                    if j != 0:
                        cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)
 
            cv2.imshow("Image", img)
 
            # key = cv2.waitKey(1)
            # if key == ord('q'):
            #     break

    def close(self):

        self.Presentation.Close()
        print("Presentation Closed Successfully!")

        self.Application.Quit()
        print("Application Closed Successfully!")
        pass

class sp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        pass

    def initUI(self):
        h = 1080
        w = 1920
        self.setGeometry(0,0,w,h)
        self.setWindowTitle("Smart Presentation")

        self.setObjectName("Smart_Presentation")
        self.resize(1920, 1080)

        self.presentation_window = QLabel(self)
        self.presentation_window.setGeometry(20,20,1280,720)
        self.presentation_window.setFrameShape(QtWidgets.QFrame.Box)
        self.presentation_window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.presentation_window.setObjectName("presentation_window")

        self.presenter()
        
        pass

    def presenter(self):
        slide_path = "C:\\Users\\yashu\\Desktop\\SGP_4\\SGP4\\slide_1.png"

        try:
            
            image = cv2.imread(slide_path)
            log.info("img read")

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(np.asarray(image), mode='RGB')
            qt_img = ImageQt.ImageQt(image)
            qpixmap = QPixmap.fromImage(qt_img)

            height = 720
            width = 1280

            new_size = QSize(width, height)
            resized_frame_pixmap = qpixmap.scaled(new_size, Qt.KeepAspectRatio)
            
            log.info("converted")

            self.presentation_window.setPixmap(resized_frame_pixmap)
            log.info("set")
            pass
        except Exception as e:
            print(f"Error loading or converting image: {e}")

        # return qpixmap
    pass


if __name__ == "__main__":
    
    smp = SmartPresentation()
    file_path = "C:\\Users\\yashu\\Desktop\\FFE_Mentorship_Program\\Session_1\\Speed of COVID-19 Vaccine Development.pptx"
    smp.initPresentation(file_path)

    # app = QtWidgets.QApplication(sys.argv)
    # ui = sp()
    # ui.show()
    # sys.exit(app.exec_())
    
    pass