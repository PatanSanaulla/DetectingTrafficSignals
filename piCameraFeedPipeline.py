import cv2
import numpy as np
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def findGreenLight(image):
    height = (image.shape[0])
    width = (image.shape[1])
    
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('HSV', hsvImage)
    
    #threshold = cv2.inRange(hsvImage, (75, 145, 120), (85, 170, 140))
    #threshold = cv2.inRange(hsvImage, (75, 100, 130), (85, 160, 150))
    threshold = cv2.inRange(hsvImage, (65, 60, 60), (85, 255, 255))
    #cv2.imshow('Threshold', threshold)
    
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #print(contours)

    if len(contours) == 0:
        print('No green signal found')
    else:
        c = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        image = cv2.circle(image, (int(x),int(y)), int(radius), (0, 0, 255), 2)

    return image
    
#cv2.drawContours(image, contours
# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))
# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('trafficLights01.avi', fourcc, 10, (640, 480))
# write frame to video file

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    # grab the current frame
    image = frame.array
    image = cv2.rotate(image, cv2.ROTATE_180)
    # show the frame to our screen
    cv2.imshow("Frame", image)
    
    processedImage = findGreenLight(image)
    out.write(processedImage)
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # press the 'q' key to stop the video stream
    if key == ord("q"):
        break
    
#cv2.waitKey(0)
#cv2.destroyAllWindows()
