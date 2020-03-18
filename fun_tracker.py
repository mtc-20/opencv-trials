#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:10:18 2020

Taken from Pyimagesearch

@author: mtc-20
"""
import cv2
import imutils
from collections import deque
import numpy as np
from hsv_tracker import hsv_trackbar

minHSV = np.array([30, 60, 95]) # These work better for reflective
maxHSV = np.array([95, 245, 255]) 
pts = deque(maxlen= 200)
counter = 0
(dX, dY) = (0, 0)
direction = ""
minHSV, maxHSV = hsv_trackbar()
cap = cv2.VideoCapture(0)
ctr = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, minHSV, maxHSV)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts)>0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius>10:
            cv2.circle(frame, (int(x),int(y)), int(radius), (150,0,255), 2)
            cv2.circle(frame, center, 5, (150,0,255), -1)
    pts.appendleft(center)
    
    for i in range(1, len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(64/float(i+1))*2.5)
        cv2.line(frame, pts[i-1],pts[i], (150,0,255), thickness)
        
        if counter>= 10 and  i==1 and pts[-10] is not None:
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = '', ''
            
            if np.abs(dX)>20:
                dirX = 'East' if np.sign(dX)==1 else 'West'
                
            if np.abs(dY)>20:
                dirY = 'North' if np.sign(dY)==1 else 'South'
                
            if dirX != '' and dirY != '':
                direction = "{}-{}".format(dirY, dirX)
                
            else:
                direction = dirX if dirX != '' else dirY
        
        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 2)
        cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 5), 1)
     
    counter += 1
    cv2.imshow('tracker', frame)
    k = cv2.waitKey(1)
    if k%256==27:
        break
    if k == 32:
        cv2.imwrite('Ana_{}.png'.format(ctr), frame)
        ctr +=1

cap.release()
cv2.destroyAllWindows()
    