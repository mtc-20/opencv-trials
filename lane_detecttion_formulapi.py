#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:15:40 2020

@author: mtc-20
"""

import cv2
import math
import numpy as np

# Settings
MINHUNTCOLOR = (0,0,0) # Minimum RGB values for our coloured line
MAXHUNTCOLOR = (150, 150, 150) 
TARGETLINES = (255, 0, 0)
TARGETPOINTS =(255, 255, 0)
TARGETPOINTSIZE = 3

ROITOP = 260
ROIRIGHT = 920
ROIH = 640 - ROITOP
ERODESIZE = 5
TARGETY1 = int(ROIH * 0.9)
TARGETY2 = int(ROIH * 0.4)

OVERLAYORING = True

def SweepLine(image, Y):
    # Grab the line of interest
    line = image[Y, :]
    width = len(line)
    #print (width)
    # Work out where the changes are
    changed = np.where(line[:-1] != line[1:])[0]
    #print(changed)
    # Set an initial state with an edge at the start of the line
    current = line.item(0)
    prevPosition = 0
    sectionsFound = []
    # Sweep over the list of changes
    for i in changed:
        # Filter out changes at the edge of the image
        # These can be messy from the camera
#        if i < 2 or i > (width -3):
#            pass
        if current:
            # End of high section - add to list
            size = i - prevPosition
            location = int(size/2) + prevPosition
            sectionsFound.append([size, location])
            prevPosition = i
        else:
            # End of low section, mark the next start point
            prevPosition = i
        
        current = not current
        # If we finished on a high section generate a final section for it
        # This includes the whole line being active!
        if current:
            size = width - prevPosition
            location = int(size/2) + prevPosition
            sectionsFound.append([size, location])
        
        # Finally sort by size and return
        sectionsFound.sort()
        sectionsFound.reverse()
        
        return sectionsFound
            

## Initialization
#image = cv2.imread('sample_3.png')
#
## Process image to get a lineMask image (boolean)
#minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
#maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))
#lineMask = cv2.inRange(image[ROITOP:, 160:ROIRIGHT], minBGR, maxBGR)
#
#
#
## Erode the mask to remove noise
#if ERODESIZE > 1:
#    erodeKernel = np.ones((ERODESIZE, ERODESIZE), np.uint8)
#    lineMask   = cv2.erode(lineMask, erodeKernel)
#    
## Find the line sections in our two locations
#sectionsY1 = SweepLine(lineMask, TARGETY1)
#sectionsY2 = SweepLine(lineMask, TARGETY2)
#print("foudn Y1: ", sectionsY1)
## Pick the largest sections and take their center positions
#if len(sectionsY1) > 0:
#    X1 = sectionsY1[0][1]
#else:
#    X1 = None
#if len(sectionsY2) > 0:
#    X2 = sectionsY2[0][1] - 65
#else:
#    X2 = None
#print ("P1: (%i, %i) P2: (%i, %i)" %(X1, TARGETY1, X2, TARGETY2))
## Generate display image 
## (overlay)
#if OVERLAYORING:
#    displayImage = image[ROITOP:, 160:ROIRIGHT].copy()
#    # Darken areas not matching the mask
#    blue, green, red = cv2.split(displayImage)
#    red  [lineMask == 0] //= 3
#    green[lineMask == 0] //= 3
#    blue [lineMask == 0] //= 3
#    displayImage = cv2.merge([blue, green, red])
#
## from mask
##else:
#displayImage_grey = cv2.merge([lineMask, lineMask, lineMask])
#displayImage_grey //= 2
#    
## Draw line between points
#if X1 != None and X2 != None:
#    cv2.line(displayImage, (X1, TARGETY1), (X2, TARGETY2), TARGETLINES, 1)
#    cv2.line(displayImage_grey, (X1, TARGETY1), (X2, TARGETY2), TARGETLINES, 1)
#if X1 != None:
#    cv2.circle(displayImage, (X1, TARGETY1), TARGETPOINTSIZE, TARGETPOINTS, 1)
#if X2 != None:
#    cv2.circle(displayImage, (X2, TARGETY2), TARGETPOINTSIZE, TARGETPOINTS, 1)
#    cv2.circle(displayImage_grey, (X2, TARGETY2), TARGETPOINTSIZE, TARGETPOINTS, 1)
#    
#cv2.imshow('mask', displayImage_grey)   
#cv2.imshow('linemask', lineMask)
##cv2.imshow('linemask_erode', lineMask)
#cv2.imshow('result', displayImage)
#cv2.imshow('original', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


def draw_heading(image):
    minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
    maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))
    lineMask = cv2.inRange(image[ROITOP:, :], minBGR, maxBGR)
    
    if ERODESIZE > 1:
        erodeKernel = np.ones((ERODESIZE, ERODESIZE), np.uint8)
        lineMask   = cv2.erode(lineMask, erodeKernel)
    
    sectionsY1 = SweepLine(lineMask, TARGETY1)
    sectionsY2 = SweepLine(lineMask, TARGETY2)
    if sectionsY1 is None:
        X1 = None
    elif len(sectionsY1) > 0:
        X1 = sectionsY1[0][1]
    else:
        X1 = None
    if sectionsY2 is None:
        X2 = None
    elif len(sectionsY2) > 0:
        X2 = sectionsY2[0][1] - 55 #65
    else:
        X2 = None
#    print("P1: ({},{}) P2: ({},{})".format(X1, TARGETY1, X2, TARGETY2))
    

    if OVERLAYORING:
        displayImage = image[ROITOP:, :].copy()
        # Darken areas not matching the mask
        blue, green, red = cv2.split(displayImage)
        red  [lineMask == 0] //= 3
        green[lineMask == 0] //= 3
        blue [lineMask == 0] //= 3
        displayImage = cv2.merge([blue, green, red])
    else:
        displayImage = cv2.merge([lineMask, lineMask, lineMask])
        displayImage //= 2
    text = 'Nada'    
    if X1 != None and X2 != None:
        rad = math.atan2(TARGETY1 - TARGETY2, X1 - X2)
        deg = round(math.degrees(rad)-90, 3)
        print(round(rad,3), deg)
#        text = '{}'.format(round(rad,3))
        text = '{}'.format(deg)
#        if X1>X2:
#            text = 'left'
#        elif X1<X2:
#            text = 'right'
#        else: 
#            text = 'straight'
        cv2.line(displayImage, (X1, TARGETY1), (X2, TARGETY2), TARGETLINES, 1)
#    if X1 != None:
#        cv2.circle(displayImage, (X1, TARGETY1), TARGETPOINTSIZE, TARGETPOINTS, 1)
#    if X2 != None:
#        cv2.circle(displayImage, (X2, TARGETY2), TARGETPOINTSIZE, TARGETPOINTS, 1)
    
    #cv2.putText(displayImage, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        
    #cv2.imshow('mask', displayImage_grey)   
    #cv2.imshow('linemask', lineMask)
    #cv2.imshow('linemask_erode', lineMask)
#    cv2.imshow('result', displayImage)
#    cv2.imshow('original', image)
#    cv2.waitKey()
#    cv2.destroyAllWindows()
    return displayImage

""" 
Video
"""
cap = cv2.VideoCapture("new_video(1).avi")
#out = cv2.VideoWriter('out_new_again.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,380))
print(cap.get(3), cap.get(4))
#cap.set(5, 20)
minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break
    lineMask = draw_heading(image)
    #lineMask = cv2.cvtColor(lineMask,cv2.COLOR_RGB2BGR)
#    cv2.line(image, (10, 10), (50, 50), (0,200,200), 1)
#    out.write(lineMask)
    cv2.imshow('linemask', lineMask)
    
    k = cv2.waitKey(1)
    if k%256 == 27:
        break
cap.release()
cv2.destroyAllWindows()
#out.release()    
