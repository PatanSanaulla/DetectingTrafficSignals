import cv2
import numpy as np
import imutils


image = cv2.imread('trafficSign01.jpg')

height = (image.shape[0])
width = (image.shape[1])

#print(height)
#print(width)

hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV', hsvImage)

#blankImage = np.zeros(shape=[height, width, 1], dtype=np.uint8)
#cv2.imshow('Blank', blankImage)

#for x in range(0, height-1):
 #   for y in range(0, width-1):

threshold = cv2.inRange(hsvImage, (75, 130, 130), (85, 160, 150))
cv2.imshow('Threshold', threshold)

contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#print(contours)

if len(contours) == 0:
    print('No green signal found')
else:
    c = max(contours, key=cv2.contourArea)
    ((x,y), radius) = cv2.minEnclosingCircle(c)
    image = cv2.circle(image, (int(x),int(y)), int(radius), (0, 0, 255), 2)

cv2.imshow('final Image', image)
#cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
cv2.waitKey(0)
cv2.destroyAllWindows()