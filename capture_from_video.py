#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 19:33:34 2020

@author: mtc-20
"""

import cv2

cap = cv2.VideoCapture(0)
ctr = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k%256==27:
        break
    elif k%256==32:
        cv2.imwrite('green_area_{}.png'.format(ctr),frame)
        print("Written green_area_{}".format(ctr))
        ctr += 1
        
cap.release()
cv2.destroyAllWindows()

