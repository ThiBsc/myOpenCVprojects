#!/usr/bin/env python3
import cv2
import numpy as np
import hsvrange as hsv

# Init range for detection
colorRange = hsv.HsvRange([81, 100, 20], [130, 255, 255], 'Blue')

# Use the camera
cap = cv2.VideoCapture()
# Camera: open(0), File open("file.mp4")
cap.open(0)

if cap.isOpened():
    ret, prev = cap.read()
    print('Press \'q\' to terminate')

while (cap.isOpened()):

    ret, frame = cap.read()
    if ret is False:
        break

    # Get mirrored
    frame = cv2.flip(frame, 1)
    # Convert to HSV
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create the mask
    lower = np.array(colorRange.lowerHSV)
    upper = np.array(colorRange.upperHSV)
    mask = cv2.inRange(hsvFrame, lower, upper)

    # Find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter noisy contours
    contours = [c for c in contours if 500 < cv2.contourArea(c) < 10000]

    # Draw the bounding rect box of each contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=1)
    for c in contours:
        brect = cv2.boundingRect(c)
        x = int(brect[0] + (brect[2] / 2))
        y = int(brect[1] + (brect[3] / 2))
        radius = int(brect[2]/2) + 3
        cv2.circle(frame, (x, y), 2, (0, 0, 255), thickness=2)
        #cv2.circle(frame, (x, y), radius, (0, 255, 0), thickness=2)
        #cv2.rectangle(frame, brect, (0, 255, 0), 2)

    cv2.imshow('Output', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
