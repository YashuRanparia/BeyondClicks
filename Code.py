import os

import aspose.pydrawing as drawing
import aspose.slides as slides
import cv2
import numpy as np
import win32com.client

import HandTrackingModule as htm

Application = win32com.client.Dispatch("PowerPoint.Application" )
Presentation = Application.Presentations.Open("C:\\Users\\yashu\\OneDrive\\Desktop\\FFE_Mentorship_Program\\Session_1\\Speed of COVID-19 Vaccine Development.pptx")
print(Presentation.Name)
Presentation.SlideShowSettings.Run()

# Parameters
width, height = 900, 720
gestureThreshold = 300
maxZoomFactor = 2
minZoomFactor = 1
zoomFactor = 1


# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = htm.handDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 20
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
pptLength = len(Presentation.slides)
print("Total Slides : ", pptLength)


while True:
    # Get image frame
    success, image = cap.read()
    imgCurrent = image.copy()
    # Find the hand and its landmarks

    image = cv2.flip(image, 1)
    # find hand landmarks
    img = detector.findHands(image)
    lmList = detector.findPosition(img, draw=False)

    if(len(lmList) != 0 and buttonPressed is False):
        #Check which fingures are up
        fingers = detector.fingersUp()

        #condition for next
        condition = fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]

        #condition for previous
        condition_prev = fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]

        if(condition):
            print("Next")
            buttonPressed = True
            if imgNumber > 0:
                Presentation.SlideShowWindow.View.Next()
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False

        elif(condition_prev):
            print("Previous")
            buttonPressed = True
            if imgNumber >0 :
                Presentation.SlideShowWindow.View.Previous()
                imgNumber += 1
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False
 
    else:
        annotationStart = False
 
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False
 
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)
 
    cv2.imshow("Image", img)
 
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

