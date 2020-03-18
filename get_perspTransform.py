#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 16:38:30 2020

@author: mtc-20
"""

import cv2
import numpy as np

image = cv2.imread('sample_4.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h,w,d = image.shape
top = int(h*0.6)

roi = gray[top:h,0:w]
hr,wr = roi.shape

#src = np.float32([[0,0], [wr,0 ], [wr, hr], [0,hr]])
#src = np.float32([[,top], [wr,top ], [wr, h], [0,hr]])
#dst = np.float32([[0,top], [wr,top ], [wr, h], [0,hr]])

src = np.float32([[280, 540], [920, 540], [w, h], [0,h]])
dst = np.float32([[0,0], [640,0 ], [640, 180], [0, 180]])
#print("ROI h:{} w:{}".format(hr,wr))

M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(image, M, (640, 180))
 

cv2.imshow('frame', image)
cv2.imshow('ROI', roi)
cv2.imshow('Warp', warped)
cv2.waitKey(0)
cv2.destroyAllWindows()