from imutils import perspective
import cv2
import math, sys, getopt
import numpy as np


def scanFile(file, color=False, pdf=False):
    # read image
    oframe = cv2.imread(file, cv2.IMREAD_COLOR)
    frame = oframe.copy()

    # Convert to grayscale and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    # Make a binary treshold (adjust if the paper is not correctly detected)
    ret, thresh = cv2.threshold(blur, 115, 255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh', thresh)

    # find the contours of the document
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv2.contourArea(c) > 500]

    scan = None
    for c in cnts:
        # correction of the paper deformation to have four corner points
        epsilon = 0.1*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        #print(approx)
        if len(approx) == 4:
            pts1 = []
            cv2.polylines(frame,[approx],True,(190, 123, 68), 3)
            for point in approx:
                (x, y) = point[0]
                cv2.circle(frame, (x, y), 2, (0,255,0), 5)
                pts1.append([x, y])

            # order the points in clockwise order and calculate width & height
            pts1_cw = perspective.order_points(np.array(pts1))
            w_top = math.sqrt( (pts1_cw[0][0] - pts1_cw[1][0])**2 + (pts1_cw[0][1] - pts1_cw[1][1])**2 )
            w_bottom = math.sqrt( (pts1_cw[3][0] - pts1_cw[2][0])**2 + (pts1_cw[3][1] - pts1_cw[2][1])**2 )
            width = int(max(w_top, w_bottom))
            h_left = math.sqrt( (pts1_cw[0][0] - pts1_cw[3][0])**2 + (pts1_cw[0][1] - pts1_cw[3][1])**2 )
            h_right = math.sqrt( (pts1_cw[1][0] - pts1_cw[2][0])**2 + (pts1_cw[1][1] - pts1_cw[2][1])**2 )
            height = int(max(h_left, h_right))
            
            # create a image from the corner points
            pts1 = np.array([pts1_cw[0], pts1_cw[1], pts1_cw[3], pts1_cw[2]], dtype="float32")
            pts2 = np.array([[0,0], [width, 0], [0, height], [width, height]], dtype="float32")
            # fix the image perspective
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            scan = cv2.warpPerspective(oframe, matrix, (width, height))
            if color is False:
                gray = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
                ret, scan = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
            
            #cv2.imshow('frame', frame)
            #cv2.imshow('scan', scan)
        else:
            # it is probably not a paper
            continue
    return scan


'''
Manage the program arguments
'''
if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help','color','pdf'])
    except getopt.GetoptError:
        print('scanner.py [option] image')
        sys.exit()
    
    file = args[-1]
    bColor = False
    bPDF = False
    for opt, arg in opts:
        if opt in ('-h', '--help') or len(args) < 1:
            print('scanner.py [option] image')
            sys.exit()
        elif opt == '--color':
            bColor = True
        elif opt == '--pdf':
            bPDF = True
            print('PDF output not implement yet')
    
    scan = scanFile(file, color=bColor, pdf=bPDF)
    #scan = cv2.resize(scan, (0,0), fx=0.6, fy=0.6)

    cv2.imshow('scan', scan)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
