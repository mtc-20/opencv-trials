#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:09:39 2019

@author: mtc-20
"""

import cv2
import imutils

## for selecting video in command line
#import argparse
#ap = argparse.ArgumentParser()
#ap.add_argument('-v','--video', help='path to the video file')
#args = vars(ap.parse_args())
#cam = cv2.VideoCapture(args['video'])

cam = cv2.VideoCapture(0)

while True:
    (grabbed, frame) = cam.read()
    status = "No target"
    
    if not grabbed:
        print("[INFO]: Nothing to read")
        break
                    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01*peri, True)
        
        if len(approx)>= 4 and len(approx) <= 6:
            (x,y,w,h) = cv2.boundingRect(approx)
            aspectratio = w/float(h)
            
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area/float(hullArea)
            
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.8
            keepAspectRatio = aspectratio >= 0.8 and aspectratio <= 1.2
            
            if keepDims and keepSolidity and keepAspectRatio:
                cv2.drawContours(frame,[approx], -1, (0,0,200), 4)
                status = "Targets detected"
                    
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
                (startX, endX) = (int(cX - (w*0.15)), int(cX + (w*0.15)))
                (startY, endY) = (int(cX - (h*0.15)), int(cX + (h*0.15)))
                cv2.line(frame, (startX, cY), (endX, cY), (0,0,255), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0,0,255), 3)
                
            
    cv2.putText(frame, status, (20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 2)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()