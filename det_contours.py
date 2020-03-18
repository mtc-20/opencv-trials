#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:44:28 2020

@author: mtc-20
"""

#for contour in contours:
#    print(contour[0][0], type(contour[0][0]), len(contour))

import cv2


# Initialization
#cap=cv2.VideoCapture('J_shape_wideangle.avi')
#cap.set(3, 640)
#cap.set(4, 480)
ctr = 0

#### Video
#while(cap.isOpened()):
#    ret, frame=cap.read()
#    if ret == True:
#        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#        h,w,d = frame.shape
#        top = int(h*0.6)
#        gray[0:top, 0:w] = 0 
#        ret, thresh = cv2.threshold(gray, 127, 255, 0)
#        edges = cv2.Canny(thresh, 10, 150, apertureSize=3)
#        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        cv2.polylines(frame, contours, False, (255, 0, 0), 2)
#        for x,y in contours[0][0]:
#            print(x,y)
#        
#        
##        print(contours[0][0], type(contours))
#
##        cv2.imshow('canny', edges)
##        cv2.imshow('thresh', thresh)
#        cv2.imshow('frame',frame)
#        k = cv2.waitKey(1)
#        if k%256 == 27:
#            print("[INFO] ESC hit, closing...")
#            break
#        elif k%256 == 32:
#            cv2.imwrite('sample_{}.png'.format(ctr), frame)
#            ctr += 1
#    else:
#        print("[INFO] File not found or corrupted; closing...")
#        break
#    
## Close everything here
#cv2.destroyAllWindows()
#cap.release()

## Image

image = cv2.imread('sample.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h,w,d = image.shape
top = int(h*0.6)
gray[0:top, 0:w] = 0 
ret, thresh = cv2.threshold(gray, 127, 255, 0)
edges = cv2.Canny(thresh, 10, 150, apertureSize=3)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.polylines(image, contours, False, (255, 0, 0), 2)
for contour in contours:
   # print(contour)
    for c in contour:
        for pt in c:
            print(pt)
    print('next')
#print(contours, type(contours[0]), len(contours[0]))
cv2.imshow('image', image)
cv2.imshow('canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()