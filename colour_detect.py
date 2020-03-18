#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:35:19 2019

@author: mtc-20
"""

import numpy as np
import cv2

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red':(0,80,80),
         'green':(35,21,62),
         'blue':(97,100,117),
         'yellow':(23,59,119),
         #'orange':(10,100,20)
         }

upper = {'red':(20,255,255), 
         'green':(55,255,255),
         'blue':(117,255,255),
         'yellow':(43,255,255),
         #'orange':(30,255,255)
         }

# define standard colors for circle around the object
colors = {'red':(0,0,255),
          'green':(0,255,0),
          'blue':(255,0,0),
          'yellow':(0,255,217),
          #'orange':(0,140,255)
          }

font = cv2.FONT_HERSHEY_SIMPLEX
ctr = 0
while True:
    # grab the current frame
    frame = cv2.imread('21.png')

    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv,lower[key],upper[key])
        if ctr==0:
            cv2.imwrite('mask_inrange.jpg', mask)
        mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        if ctr==0:
            cv2.imwrite('mask_open.jpg', mask)
        mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
        if ctr==0:
            cv2.imwrite('mask_close.jpg', frame)
            ctr += 1
        
        #Calculate percentage of pixel colors
        output = cv2.countNonZero(mask)
        res = np.divide(float(output),mask.shape[0]*int(mask.shape[1] / 128))
        percent_colors = np.multiply((res),400) / 10000
        percent=(np.round(percent_colors*100,2))

        cnts = cv2.findContours(mask.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame,(int(x),int(y)),int(radius),colors[key],2)
                cv2.putText(frame,
                            str(percent) + '% ' +key+ ' r:' + str(radius),
                            (int(x-radius),int(y-radius)),
                            font,
                            0.6,
                            colors[key],
                            2)
#    cv2.imwrite('Colors_3.jpg', frame)
    cv2.imshow("Frame",frame)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

#print(c)
cv2.destroyAllWindows()