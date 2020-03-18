#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:14:36 2019

@author: mtc-20
"""

import cv2
import imutils
import numpy as np

'''
#import argparse
#ap = argparse.ArgumentParser()
##ap.add_argument('-v','--video', help = 'Path to video')
#ap.add_argument('-i','--image', help='Path to image')
#args = vars(ap.parse_args())
#image = cv2.imread(args['image'])

image = cv2.imread('23.png')
outpút = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

if circles is not None:
    print(len(circles))
    circles = np.round(circles[0,:]).astype('int')
    
    for (x,y,r) in circles:
        cv2.circle(outpút, (x,y), r, (0,255,0), 2)
        
        
cv2.imshow("Output", outpút)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("[INFO]: No feed")
        break
    
    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.1, 100)
    
    if circles is not None:
        circles = np.round(circles[0,:]).astype('int')
        
        for (x,y,r) in circles:
            cv2.circle(frame, (x,y), r, (0,200,0), 3)
            cv2.rectangle(frame, (x-5, y-5), (x+5, y+5), (0,128,255), -1)
            cv2.rectangle(frame, (x-r, y-r), (x+r, y+r), (0,0,255), 3)
            
    cv2.imshow("Output", frame)
    cv2.imshow("Gray", gray)
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()