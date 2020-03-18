#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 18:25:16 2020
To detect shapes of a certain colour 
Colour detection using HSV seems to perfom best, but is currently written only
for videos
~~ TODO: To detect only shapes of a min area ~~
TODO: Introduce Settings variables for cleaner code
@author: mtc-20
"""

import cv2
import imutils

class ShapeDetector():
    def __init__(self):
        pass
    def detect(self, c):
        shape = 'None'
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.025*peri, True)
        if len(approx) == 3:
            shape = 'triangle'
        elif len(approx) == 4:
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w/float(h)
            shape = 'square' if ar >= 0.95 and ar <= 1.05 else 'rectangle'
        elif len(approx) == 5:
            shape = 'pentagon'
        elif 5<len(approx)<10:
            shape = 'polygon'
        else:
            shape = 'circle'
        
        print(shape)
        return shape
    
    def detectRect(self, c):
        shape = 'None'
#        rectCnt = []
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.025*peri, True)
        if len(approx) == 4:
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w/float(h)
            shape = 'square' if ar >= 0.95 and ar <= 1.05 else 'rectangle'
#            rectCnt = approx
#            print(rectCnt)
        
        
#        if shape != 'None':
#            print(shape) 
        return shape
    

image = cv2.imread('trapezium.png')


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)[1]
thresh = (255-thresh)
edges = cv2.Canny(gray,100,200)


cv2.imshow('gray', gray)
cv2.imshow('blurred', blurred)
cv2.imshow('thresh', thresh)
cv2.imshow('edges', edges)
cv2.waitKey(0)  
cv2.destroyAllWindows()


cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print(cnts, type(cnts))
cnts = imutils.grab_contours(cnts)
#print(cnts, type(cnts)) 
sd = ShapeDetector()    

for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / (M["m00"]+ 1e-7)))
    cY = int((M["m01"] / (M["m00"]+ 1e-7)))
    shape = sd.detect(c)
    cv2.drawContours(image, [c], -1, (255,0,0), 2)
    cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
cv2.imshow('result', image)
cv2.waitKey(0)
    
cv2.destroyAllWindows()

import numpy as np
minHSV = np.array([30, 60, 95]) # These work better for reflective
maxHSV = np.array([95, 245, 255]) 
image = cv2.imread('green_area_3.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, minHSV, maxHSV)
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
sd = ShapeDetector()    
for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / (M["m00"]+ 1e-7)))
    cY = int((M["m01"] / (M["m00"]+ 1e-7)))
    shape = sd.detectRect(c)
    area = cv2.contourArea(c)
    #print(area)
    if area > 10000:
        cv2.drawContours(image, [c], -1, (0,0,255), 3)
        print(area)
        if shape == 'rectangle' or shape == 'square':
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.025*peri, True)
            print('approx', approx)
            for p in approx:
                if p[0][0]>cX and p[0][1]<cY:
                    cv2.circle(image, (p[0][0],p[0][1]),3,(100,0,0),-1)
            #print(c)
#            rtPt = []
#            for pt in c:
#                print(pt)
#                print(pt[0][0], pt[0][1])
            cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
            cv2.circle(image, (cX,cY),3,(100,0,0),-1)
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

for p in approx:
    print(p[0][0], p[0][1])
""" 
Video
"""
import numpy as np
from hsv_tracker import hsv_trackbar

#MINHUNTCOLOR = (20,75,100) # Minimum RGB values for our coloured line
#MAXHUNTCOLOR = (105, 255, 130) 

#MINASHSV = np.array([np.array(MINHUNTCOLOR)])
#MAXASHSV = np.array([np.array(MAXHUNTCOLOR)])
#minHSV = cv2.cvtColor(MINASHSV, cv2.COLOR_BGR2HSV)
#maxHSV = cv2.cvtColor(MAXASHSV, cv2.COLOR_BGR2HSV)

# The HSV range has to be manually found using hsv_tracker.py
# Testing done to detect green of signs
minHSV = np.array([30, 60, 95]) # These work better for reflective
maxHSV = np.array([95, 245, 255]) 
#minHSV = np.array([45, 105, 105]) # TOTRY: [30,60,95]
#maxHSV = np.array([95, 245, 255])

minHSV, maxHSV = hsv_trackbar('green')
[minHSV2, maxHSV2] = np.loadtxt('green.out').astype(int) # To be moved to settings file

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvMask = cv2.inRange(hsv, minHSV, maxHSV)
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    blurred = cv2.GaussianBlur(gray, (17,17), 0)
#    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
#    thresh = (255-thresh)
#    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(hsvMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
    sd = ShapeDetector()    
    for c in cnts:
#        rectCnt = None
        M = cv2.moments(c)
        cX = int((M["m10"] / (M["m00"]+ 1e-7)))
        cY = int((M["m01"] / (M["m00"]+ 1e-7)))
        shape = sd.detectRect(c)
#        print('rectCnt', rectCnt)
        area = cv2.contourArea(c)
        #print(area)
        if area > 10000:
            #cv2.drawContours(frame, [c], -1, (0,0,255), 3)
#            print(area)
            if shape == 'rectangle' or shape == 'square':
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.025*peri, True)
#                print('approx', approx)
                for p in approx:
                    if p[0][0]>cX and p[0][1]<cY:
                        cv2.circle(frame, (p[0][0],p[0][1]),5,(150,0,0),-1)
#                print(c)
                cv2.putText(frame, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                cv2.circle(frame, (cX,cY),5,(150,0,0),-1)
    cv2.imshow('result', frame)
#    cv2.imshow('thresh', thresh)
    cv2.imshow('hsvMask', hsvMask)
    k = cv2.waitKey(1)
    if k%256 == 27:
        break
cap.release()
cv2.destroyAllWindows()
