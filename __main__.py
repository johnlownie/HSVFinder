# import packages
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time

# set the video stream
vs = VideoStream(src=0).start()

# allow the camera or video file to load
time.sleep(2.0)

#initialize some variables
def nothing(x):
    pass
lowH = 0
lowS = 0
lowV = 0
highH = 179
highS = 255
highV = 255

cv2.namedWindow('HSV Scale')

# create trackbars for changing HSV values
cv2.createTrackbar('lowH',  'HSV Scale', lowH , 180, nothing)
cv2.createTrackbar('highH', 'HSV Scale', highH, 180, nothing)

cv2.createTrackbar('lowS' , 'HSV Scale', lowS , 255, nothing)
cv2.createTrackbar('highS', 'HSV Scale', highS, 255, nothing)

cv2.createTrackbar('lowV' , 'HSV Scale', lowV , 255, nothing)
cv2.createTrackbar('highV', 'HSV Scale', highV, 255, nothing)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # if we are viewing a video and did not grab a frame, we are at end of video
    if frame is None:
        break

    lowH = cv2.getTrackbarPos('lowH', 'HSV Scale')
    lowS = cv2.getTrackbarPos('lowS', 'HSV Scale')
    lowV = cv2.getTrackbarPos('lowV', 'HSV Scale')

    highH = cv2.getTrackbarPos('highH', 'HSV Scale')
    highS = cv2.getTrackbarPos('highS', 'HSV Scale')
    highV = cv2.getTrackbarPos('highV', 'HSV Scale')

    lower = np.array([lowH, lowS, lowV])
    upper = np.array([highH, highS, highV])

    # resize the frame, blur it, and convert it to the HSV colour space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then erode and dilate
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # show the fram to our screen and increment the frame counter
    cv2.imshow('Frame:', mask)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# stop the stream and close windows
vs.stop()
cv2.destroyAllWindows()
