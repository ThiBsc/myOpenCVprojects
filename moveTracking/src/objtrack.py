import cv2
import os, sys, time, getopt, datetime
import numpy as np

'''
You can change these following values
to tune the detection
'''
binThresh = 40
cannyThresh = 150
# Don't touch maxValue
maxValue = 255
'''
You can change these following values
to configure the display
'''
width, height = (640, 480)
inputfile = ''
'''
Change these following values
to set delay (minute) between notifications alert
and the trigger threshold
'''
delay = 5
areaThresh = 10000
lastAlert = None

def canSendAlert():
    global lastAlert
    if lastAlert is None or (lastAlert is not None and ((datetime.datetime.utcnow() - lastAlert).seconds//60)%60 > delay):
        lastAlert = datetime.datetime.utcnow()
        return True
    else:
        return False

def startTracking(useTelegram=False, chat_id='', dic_fun={}, action=0):

    cap = cv2.VideoCapture()

    # Camera: open(0), File open("file.mp4")
    cap.open(0 if not inputfile else inputfile)

    if cap.isOpened():
        ret, prev = cap.read()
        prev = cv2.resize(prev, (width, height))
        print('Press \'q\' to terminate')

    while (cap.isOpened()):

        ret, frame = cap.read()

        if ret == False:
            break
        
        frame = cv2.resize(frame, (width, height))
        # Make a diff between 2 frame
        diff = cv2.absdiff(prev, frame)
        # Convert to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # Make a binary treshold
        ret, thresh = cv2.threshold(gray, binThresh, maxValue, cv2.THRESH_BINARY)
        # Apply a dilation
        elem = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
        dilat = cv2.dilate(thresh, elem, iterations=1)
        # Apply a blur twice
        gblur = cv2.blur(dilat, (5,5))
        gblur = cv2.blur(gblur, (5,5))
        # Canny the blur
        canny = cv2.Canny(gblur, cannyThresh, cannyThresh*2, apertureSize=3)
        # Find the contours
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the bounding rect box of each contours
        totalArea = 0
        for c in contours:
            brect = cv2.boundingRect(c)
            cv2.rectangle(prev, brect, (0,255,0), 2)
            totalArea += cv2.contourArea(c)
        
        '''
        This section is only use when the program
        is run from telegram.py
        This part can be improve
        '''
        if useTelegram:
            if totalArea > areaThresh and canSendAlert():
                concatened = cv2.vconcat((frame, prev))
                cv2.imwrite('alert.jpg', concatened)
                dic_fun['alert'](chat_id)
            # capture
            if action.value == 1:
                cv2.imwrite('capture.jpg', frame)
                dic_fun['capture'](chat_id)
            # record 5 seconds video
            elif action.value == 2:
                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter('record.mp4', fourcc, 20.0, (width,height))
                nframe, fps = (0, 20)
                prev = 0

                while nframe < fps*5:
                    time_elapsed = time.time() - prev
                    if time_elapsed > 1./fps:
                        out.write(frame)
                        prev = time.time()
                        nframe += 1
                    res, frame = cap.read()

                out.release()
                dic_fun['video'](chat_id)
            # stop
            elif action.value == 3:
                break
        else: # Show only when use without telegram
            cv2.imshow('Tracking', prev)

        # Set the current as previous
        prev = frame

        # Change the value in waitKey to change the frame rate
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    print('Stop tracking')

    cap.release()
    cv2.destroyAllWindows()


'''
Manage the program arguments
'''
if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:",["width=","height="])
    except getopt.GetoptError:
        print('objtrack.py [-i movie.mp4]')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('objtrack.py [-i movie.mp4]')
            sys.exit()
        elif opt == '-i':
            inputfile = arg
        elif opt == '--width':
            width = int(arg)
        elif opt == '--height':
            height = int(arg)
    
    startTracking()
