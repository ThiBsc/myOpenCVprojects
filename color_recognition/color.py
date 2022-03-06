#!/usr/bin/env python3
import cv2
import numpy as np
import hsvrange as hsv

# Init range for detection
redLowRange = hsv.HsvRange([0, 75, 20], [10, 255, 255], 'Red')
orangeRange = hsv.HsvRange([11, 100, 20], [27, 255, 255], 'Orange')
yellowRange = hsv.HsvRange([28, 50, 20], [37, 255, 255], 'Yellow')
greenRange = hsv.HsvRange([38, 20, 20], [80, 255, 255], 'Green')
blueRange = hsv.HsvRange([81, 100, 20], [130, 255, 255], 'Blue')
pinkRange = hsv.HsvRange([131, 20, 20], [169, 255, 255], 'Pink')
redHighRange = hsv.HsvRange([170, 80, 20], [180, 255, 255], 'Red')

detectableRanges = [
    redLowRange,
    redHighRange,
    orangeRange,
    yellowRange,
    greenRange,
    blueRange,
    pinkRange,
]

def averageHsvColor(img):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avgColorPerRow = np.average(hsvImg, axis=0)
    avgColors = np.average(avgColorPerRow, axis=0)
    return avgColors

# Use the camera
cap = cv2.VideoCapture()
# Camera: open(0), File open("file.mp4")
cap.open(0)

if cap.isOpened():
    ret, prev = cap.read()
    print('Press \'q\' to terminate')

while (cap.isOpened()):

    ret, frame = cap.read()
    if ret == False:
        break

    # Get mirrored
    frame = cv2.flip(frame, 1)
    # Extract the detection area
    detectionArea = frame[0:50, 0:50]
    hsvColor = averageHsvColor(detectionArea)
    # Draw the detection area
    cv2.rectangle(frame, (0, 0), (50, 50), (0, 0, 0), 2)

    hsvRange = next((range for range in detectableRanges if range.isInRange(hsvColor)), None)
    if hsvRange is not None:
        cv2.putText(frame, str(hsvRange), (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)

    cv2.imshow('Output', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




