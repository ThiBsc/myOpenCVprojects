# import the necessary packages
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
cards = []

# https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
# At least one circle is found ?
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # Create a mask to extract each circle from frame
    mask = np.zeros((height,width), np.uint8)
    for (x, y, r) in circles:
        circleAreas.append(np.pi * r**2)
        # add a white circle to the mask
        cv2.circle(mask, (x, y), r-1, (255,255,255), -1)
        # extract card by card to use feature match with FLANN
        card_mask = np.zeros((height,width), np.uint8)
        cv2.circle(card_mask, (x, y), r-1, (255,255,255), -1)
        extracted_card = cv2.bitwise_and(frame, frame, mask=card_mask)
        card = np.zeros((height,width,3), np.uint8)
        cards.append(cv2.bitwise_or(card, extracted_card))

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

    for i in range(0, len(cards)-1):
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(cards[i],None)
        for j in range(i+1, len(cards)):
            kp2, des2 = sift.detectAndCompute(cards[j],None)
            matches = flann.knnMatch(des1,des2,k=2)
            # ratio test as per Lowe's paper
            matches = [(m,n) for (m,n) in matches if m.distance < 0.27*n.distance]
            '''
            # Need to draw only good matches, so create a mask
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                matchesMask[i]=[1,0]
            draw_params = dict(matchColor = (0,255,0),
                            singlePointColor = (255,0,0),
                            matchesMask = matchesMask,
                            flags = cv2.DrawMatchesFlags_DEFAULT)
            img_matches = cv2.drawMatchesKnn(cards[0],kp1,cards[1],kp2,matches,None,**draw_params)
            #'''
            
            # retrieve the boundingRect for each match
            for (m,n) in matches:
                p1 = kp1[m.queryIdx].pt
                p2 = kp2[m.trainIdx].pt

                for c, h in zip(contours, hierarchy[0]):
                    # We draw only if we are in the card circle
                    # AND if it's direct child of the card circle
                    if 100 < cv2.contourArea(c) < minCardArea and hierarchy[0][h[3]][3] == -1:
                        if cv2.pointPolygonTest(c,p1,True) >= 0 or cv2.pointPolygonTest(c,p2,True) >= 0:
                            cv2.rectangle(oframe, cv2.boundingRect(c), (0,255,0), 2)
                    

#cv2.imshow("output", np.hstack([frame, output]))
#cv2.namedWindow("Result", cv2.WINDOW_AUTOSIZE)
cv2.imshow("result", oframe)

cv2.waitKey(0)
cv2.destroyAllWindows()
