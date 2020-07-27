# import the necessary packages
from math import pi
import sys
import cv2
import numpy as np

file = 'test/card_01.png'

if len(sys.argv) == 2:
    file = sys.argv[1]

oframe = cv2.imread(file, cv2.IMREAD_COLOR)
#oframe = cv2.resize(oframe, (0,0), fx=0.5, fy=0.5)
frame = oframe.copy()
height, width = frame.shape[:2]
output = np.zeros((height,width,3), np.uint8)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray, (7, 7)) # improve the HoughCircles detection

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.1, 150)
circleAreas = []

# https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
# At least one circle is found ?
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # Create a mask to extract each circle from frame
    mask = np.zeros((height,width), np.uint8)
    for (x, y, r) in circles:
        circleAreas.append(pi * r**2)        
        # add a white circle to the mask
        cv2.circle(mask, (x, y), r-1, (255,255,255), -1)

    # Extract the circles with the mask
    extracted_data = cv2.bitwise_and(frame, frame, mask=mask)
    output = cv2.bitwise_or(output, extracted_data)

    # At this step, the cards are in the output
    # Convert to grayscale
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    # Make a binary treshold
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_TOZERO)
    # Find the minimum area of cards circle
    minCardArea = min(circleAreas)
    # Find all the contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=20)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)

    # Draw the bounding rect box of each contours
    for c, h in zip(contours, hierarchy[0]):
        # We draw only if we are in the card circle
        # AND if it's direct child of the card circle
        if 100 < cv2.contourArea(c) < minCardArea and hierarchy[0][h[3]][3] == -1:
            brect = cv2.boundingRect(c)

            # Now, we have to search template matching in the complete capture
            x,y,w,h = brect
            roi = frame[y:y+h,x:x+w]
            # Hide the current part to avoid matching with itself
            frame_hide = frame.copy()
            cv2.rectangle(frame_hide, brect, (0,0,0), -1)
            
            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(roi,None)
            kp2, des2 = sift.detectAndCompute(frame_hide,None)
            
            matches = flann.knnMatch(des1,des2,k=2)
            # ratio test as per Lowe's paper
            good = [1 for (m,n) in matches if m.distance < 0.26*n.distance]
            #print(len(good))
            '''
            # Need to draw only good matches, so create a mask
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.3*n.distance:
                    matchesMask[i]=[1,0]
            draw_params = dict(matchColor = (0,255,0),
                            singlePointColor = (255,0,0),
                            matchesMask = matchesMask,
                            flags = cv2.DrawMatchesFlags_DEFAULT)
            img3 = cv2.drawMatchesKnn(roi,kp1,frame_hide,kp2,matches,None,**draw_params)
            '''
            if len(good) > 0:
                cv2.rectangle(oframe, brect, (0,255,0), 2)
            #else:
            #    cv2.rectangle(oframe, brect, (244,157,42), 2)
            #cv2.imshow("roi", img3)

#cv2.imshow("output", np.hstack([frame, output]))
#cv2.namedWindow("Result", cv2.WINDOW_AUTOSIZE)
cv2.imshow("result", oframe)

cv2.waitKey(0)
cv2.destroyAllWindows()
