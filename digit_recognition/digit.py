#!/usr/bin/env python3
import cv2
import numpy as np

SCALE = 3
THICK = 5
WHITE = (255, 255, 255)

# generate the digit set
digits = []
for digit in map(str, range(10)):
    (width, height), bline = cv2.getTextSize(digit, cv2.FONT_HERSHEY_SIMPLEX,
                                             SCALE, THICK)
    digits.append(np.zeros((height + bline, width), np.uint8))
    cv2.putText(digits[-1], digit, (0, height), cv2.FONT_HERSHEY_SIMPLEX,
                SCALE, WHITE, THICK)
    x0, y0, w, h = cv2.boundingRect(digits[-1])
    digits[-1] = digits[-1][y0:y0+h, x0:x0+w]

def detect(img):
    # dilate the draw
    elem = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6), (3, 3))
    dilat = cv2.dilate(img, elem, iterations=3)
    # find contours of the drawed digit
    cnts, hierarchy = cv2.findContours(dilat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # only one contour is possible in this case
    x,y,w,h = cv2.boundingRect(cnts[0])
    roi = dilat[y:y+h, x:x+w]
    # iterate over all digits to find the best match
    percent_white_pix = 0
    digit = -1
    for i, d in enumerate(digits):
        scaled_roi = cv2.resize(roi, d.shape[:2][::-1])
        # d AND (scaled_roi XOR d)
        #bitwise = cv2.bitwise_xor(d, cv2.bitwise_and(scaled_roi, d))
        bitwise = cv2.bitwise_and(d, cv2.bitwise_xor(scaled_roi, d))
        # the match is given by the highest loss of white pixel
        before = np.sum(d == 255)
        matching = 100 - (np.sum(bitwise == 255) / before * 100)
        #print(i, matching)
        #cv2.imshow('digit_%d' % i, bitwise)
        if percent_white_pix < matching:
            percent_white_pix = matching
            digit = i
    
    return digit

''' Drawing with mouse '''

# https://stackoverflow.com/questions/28340950/opencv-how-to-draw-continously-with-a-mouse
drawing = False # true if mouse is pressed
pt1_x , pt1_y = None , None

# mouse callback function
def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y
        cv2.rectangle(img, (0,0,512,512), (0,0,0), -1)

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)
            pt1_x,pt1_y=x,y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)
        digit = detect(img)
        
        cv2.putText(img, 'It is a %d' % digit, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        #cv2.imshow('digit', digit)
        #cv2.waitKey(0)

img = np.zeros((360,512,1), np.uint8)
cv2.namedWindow('test draw')
cv2.setMouseCallback('test draw',line_drawing)

while(1):
    cv2.imshow('test draw',img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

''' End drawing with mouse '''

#cv2.imshow('digits', digits)
cv2.destroyAllWindows()

