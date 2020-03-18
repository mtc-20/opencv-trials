#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 19:33:34 2020

@author: mtc-20
"""

import cv2
import math
import numpy as np
import glob

# Settings
MINHUNTCOLOR = (0,0,0) # Minimum RGB values for our coloured line
MAXHUNTCOLOR = (100, 100, 100) 
TARGETLINES = (255, 0, 0)
TARGETPOINTS =(255, 255, 0)
TARGETPOINTSIZE = 3

ROITOP = 95
#ROIRIGHT = 920
ROIH = 224 - ROITOP
ERODESIZE = 5
TARGETY1 = int(ROIH * 0.9)
TARGETY2 = int(ROIH * 0.6)

OVERLAYORING = True

# Function Definitions
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
        if i < 5 or i > (width -5):
            pass
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




#for name in glob.glob('Change_name/*.jpg'):
#    print (name)
#
#for file in glob.glob("Change_name"):
#    print()


# Test for image
    
image = cv2.imread('Change_name/111.jpg')
minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))
lineMask = cv2.inRange(image[ROITOP:, :], minBGR, maxBGR)

if ERODESIZE > 1:
    erodeKernel = np.ones((ERODESIZE, ERODESIZE), np.uint8)
    lineMask   = cv2.erode(lineMask, erodeKernel)
    
# Find the line sections in our two locations
sectionsY1 = SweepLine(lineMask, TARGETY1)
sectionsY2 = SweepLine(lineMask, TARGETY2)
# Pick the largest sections and take their center positions
if len(sectionsY1) > 0:
    X1 = sectionsY1[0][1]
else:
    X1 = None
if len(sectionsY2) > 0:
    X2 = sectionsY2[0][1] - 5
else:
    X2 = None
    
if OVERLAYORING:
    displayImage = image[ROITOP:, :].copy()
    # Darken areas not matching the mask
    blue, green, red = cv2.split(displayImage)
    red  [lineMask == 0] //= 3
    green[lineMask == 0] //= 3
    blue [lineMask == 0] //= 3
    displayImage = cv2.merge([blue, green, red])

# from mask
#else:
displayImage_grey = cv2.merge([lineMask, lineMask, lineMask])
displayImage_grey //= 2
    
# Draw line between points
if X1 != None and X2 != None:
    cv2.line(displayImage, (X1, TARGETY1), (X2, TARGETY2), TARGETLINES, 1)
    cv2.line(displayImage_grey, (X1, TARGETY1), (X2, TARGETY2), TARGETLINES, 1)
if X1 != None:
    cv2.circle(displayImage, (X1, TARGETY1), TARGETPOINTSIZE, TARGETPOINTS, 1)
if X2 != None:
    cv2.circle(displayImage, (X2, TARGETY2), TARGETPOINTSIZE, TARGETPOINTS, 1)
    cv2.circle(displayImage_grey, (X2, TARGETY2), TARGETPOINTSIZE, TARGETPOINTS, 1)
    
cv2.imshow('mask', displayImage_grey)   
#cv2.imshow('linemask', lineMask)
cv2.imshow('linemask_erode', lineMask)
cv2.imshow('result', displayImage)
cv2.imshow('original', image)
cv2.waitKey(0)
cv2.destroyAllWindows()




