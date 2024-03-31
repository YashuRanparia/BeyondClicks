import os

import aspose.pydrawing as drawing
import aspose.slides as slides
import cv2
import numpy as np
import win32com.client
from cvzone.HandTrackingModule import HandDetector as htm


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

    def initPresentation(self, path):
        self.Application = win32com.client.Dispatch("PowerPoint.Application" )
        self.Presentation = self.Application.Presentations.Open(path)
        print(self.Presentation.Name)
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


if __name__ == "__main__":
    
    smp = SmartPresentation()
    file_path = "C:\\Users\\yashu\\Desktop\\FFE_Mentorship_Program\\Session_1\\Speed of COVID-19 Vaccine Development.pptx"
    smp.initPresentation(file_path)