#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:15:14 2020

This script is written specifically to detect the lanes in the J-shaped track for AUTOTRAC 2020
Tested on videos taken from the robot cameras. Logically should work for any track
that employs a black lane and white boundaries/surroundings

@author: mtc-20
"""

import cv2
import numpy as np
import math

# Initialization
image = cv2.imread("frame_4.png")
height, width, channel = image.shape
#print ("Height: ", height, "Width: ", width)



# Settings
CROPTOP = int(height*0.7)
CROPBOTTOM = int(height*1.0)
CROPLEFT = 160
CROPRIGHT = 1120
cropped = image[CROPTOP:CROPBOTTOM, CROPLEFT:CROPRIGHT]


MINHUNTCOLOR = (0,0,0) # Minimum RGB values for our coloured line
MAXHUNTCOLOR = (100, 100, 100) 
minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))


ERODESIZE = 5





# Function Definition

# Scan line for changes
def SweepLine(mask, y):
    found = []
    # Grab the line of interest
    line = mask[y, :]
    # Get numpy to give us a list of the positions where the line changes in value
    changed = np.where(line[:-1] != line[1:])[0]
    # Remove changes too close to the edge of the image
    for i in changed:
        if i < 2:
            pass
        elif i > (width - 3):
            pass
        else:
            found.append(i)
    # Return the found values
    return found



# The values of try1, try2, try3 are used to attempt a match with target
# Any matches are added to existing lists matched1, matched2, matched3
# Any values which cannot be matched are added to the existing list unmatched
def FindMatches(y, target, try1,  match, unmatched):
    maxSeperation = int(width * 0.05)
    # Loop over all the values in target:
    while len(target) > 0:
        # Remove the next value from the list of targets
        xt = target.pop()
        matched = False
        # See if try1 can match it
        if try1:
            for x1 in try1:
                if abs(x1 - xt) < maxSeperation:
                    # Matched, work out the point and add it
                    matched = True
                    try1.remove(x1)
                    x = (xt + x1) / 2
                    match.append((x, y))
                    break
            if matched:
                continue

        # No matches
        unmatched.append((xt, y))
        
def DrawCross(image, XY, size, RGB):
    crossSize = size
    width = image.shape[1]
    height = image.shape[0]
    # Build the list of points to change
    points = []
    for i in range(-crossSize, crossSize + 1):
        points.append((XY[0] + i, XY[1]))
        points.append((XY[0], XY[1] + i))
    # Change the points on the image
    for point in points:
        x = int(point[0])
        y = int(point[1])
        if (x >= 0) and (y >= 0) and (x < width) and (y < height):
            image.itemset((y, x, 0), RGB[2])
            image.itemset((y, x, 1), RGB[1])
            image.itemset((y, x, 2), RGB[0])
            

        
# Create Mask

lineMask = cv2.inRange(cropped, minBGR, maxBGR)
## Erode the mask to remove noise
#if ERODESIZE > 1:
#    erodeKernel = np.ones((ERODESIZE, ERODESIZE), np.uint8)
#    lineMask_e   = cv2.erode(lineMask, erodeKernel)

# Create slices for scanning
grid = 100
scanLines = []
for i in range(grid):
    # Work out the position in the original image
    position = (i / float(grid)) * height
    position = int(position)
    # Work out the cropped position
    if position < CROPTOP:
        # Above our cropped region
        pass
    elif position >= CROPBOTTOM:
        # Below our cropped region
        pass
    else:
        # In the cropped region, correct and add to our list
        croppedY = int(position - CROPTOP)
        scanLines.append(croppedY)
# Show the list of positions
print(len(scanLines))
#print(SweepLine(lineMask, 223))

match = []
unmatched = []
for y in scanLines:
    # scan the line
    edge = SweepLine(lineMask, y)
    # match them
    FindMatches(y,edge,edge, match, unmatched)
    others = edge[:]
    for x in others:
        unmatched.append((x,y))
print(match, len(match))
print(len(edge), len(unmatched))
pointImage = cropped[:,:,:]
for point in match:
    DrawCross(pointImage, point, 2, (255,255,0))
for point in unmatched:
    DrawCross(pointImage, point, 5, (255,0,0))
    
# Find lane offset
#targetY = (CROPBOTTOM - CROPTOP)*0.4
#offsetIndex = 0
#offsetErrorY = abs(targetY - match[0][1])
#for i in range(len(match)):
#    errorY = abs(targetY - match[i][1])
#    if errorY < offsetErrorY:
#        offsetIndex = i
#        offsetErrorY = errorY
#offsetPoint = match[offsetIndex]
#DrawCross(pointImage, offsetPoint, 6, (10,10,200))

targetY = (CROPBOTTOM - CROPTOP)*0.4
offsetIndex = 0
offsetErrorY = abs(targetY - unmatched[0][1])
for i in range(len(unmatched)):
    errorY = abs(targetY - unmatched[i][1])
    if errorY < offsetErrorY:
        offsetIndex = i
        offsetErrorY = errorY
offsetPoint = unmatched[offsetIndex]
print(offsetPoint[0]-250)

DrawCross(pointImage, (offsetPoint[0]-250,offsetPoint[1]), 6, (10,10,200))   

targetX = (CROPRIGHT-CROPLEFT)/2.0
# Deepends on targetY value and resolution. Worked it out by getting a photo at
# the correct size with two straight edges in shot and measuring the 
# X difference at the target Y position.
laneWidth = 550

offsetX = offsetPoint[0] - targetX
offsetX = offsetX / laneWidth
print (offsetX)

#trackOffset = lineOffset + offsetX
#print (trackOffset)

# Current Angle of track
dXdY = []
for i in range(1, len(unmatched)):
    dX = float(unmatched[i-1][0] - unmatched[i][0])
    dY = float(unmatched[i-1][1] - unmatched[i][1])
    dXdY.append((dX, dY))
    #cv2.line(pointImage, (unmatched[i-1][0], unmatched[i-1][1]), (unmatched[i-1][0],unmatched[i][1]), (0,255,0), 1) # dY
    #cv2.line(pointImage, (unmatched[i-1][0], unmatched[i-1][1]), (unmatched[i][0],unmatched[i-1][1]), (0,255,0), 1) # dX
gradient = 0
for changes in dXdY:
    if changes[1] != 0:
        gradient += changes[0]/changes[1]
    else:
        pass
gradient /= len(dXdY)
# Gradient Correction factor due to perspectoive warp
# In order to correct for this error we need to measure the error in a 0° image.
correctionFactor = 2.6/0.25
correction = correctionFactor*offsetX
gradient -= correction
#angle = math.atan(gradient)*180/math.pi
angle = math.atan(gradient)
deg = math.degrees(angle)

# Track curvature
gradient2 = 0.0
if dXdY[0][1]==0:
    lastG = 0
else:
    lastG = dXdY[0][0] / dXdY[0][1]
for i in range(1, len(dXdY)):
    if dXdY[i][1] != 0:
        nextG = dXdY[i][0] / dXdY[i][1]
        changeG = lastG - nextG
        gradient2 += changeG / dXdY[i][1]
        lastG = nextG
gradient2 /= len(dXdY)



  
# Display
cv2.imshow('pointImage', pointImage)
cv2.imshow('image', image)
cv2.imshow('lineMask', lineMask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save file
#cv2.imwrite('pointImage.png', pointImage)


""" 
Video
"""
cap = cv2.VideoCapture('new_video(1).avi')
out = cv2.VideoWriter('lane_detection_10.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 10, (640,640))
height = cap.get(4)
width = cap.get(3)
print(height, width)
ctr = 0
# Settings
CROPTOP = int(height*0.7)
CROPBOTTOM = int(height*1.0)
CROPLEFT = 0 #160
CROPRIGHT = 640 #1120



MINHUNTCOLOR = (0,0,0) # Minimum RGB values for our coloured line
MAXHUNTCOLOR = (150, 150, 150) 
minBGR = np.array((MINHUNTCOLOR[2], MINHUNTCOLOR[1], MINHUNTCOLOR[0]))
maxBGR = np.array((MAXHUNTCOLOR[2], MAXHUNTCOLOR[1], MAXHUNTCOLOR[0]))


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cropped = frame[CROPTOP:CROPBOTTOM, CROPLEFT:CROPRIGHT]
    lineMask = cv2.inRange(cropped, minBGR, maxBGR)
    grid = 100
    scanLines = []
    for i in range(grid):
        # Work out the position in the original image
        position = (i / float(grid)) * height
        position = int(position)
        # Work out the cropped position
        if position < CROPTOP:
            # Above our cropped region
            pass
        elif position >= CROPBOTTOM:
            # Below our cropped region
            pass
        else:
            # In the cropped region, correct and add to our list
            croppedY = int(position - CROPTOP)
            scanLines.append(croppedY)
    # Show the no. of positions
    print(len(scanLines))
    # Find points of interest
    match = []
    unmatched = []
    for y in scanLines:
        # scan the line
        edge = SweepLine(lineMask, y)
        # match them
        FindMatches(y,edge,edge, match, unmatched)
        others = edge[:]
        for x in others:
            unmatched.append((x,y))
    print(ctr,'No of matches:', len(match), 'No of unmatched:', len(unmatched))
    ctr += 1
    #print('No of unmatched: ', len(unmatched))
    pointImage = cropped[:,:,:]
    for point in match:
        DrawCross(pointImage, point, 2, (255,255,0))
    for point in unmatched:
        DrawCross(pointImage, point, 6, (255,0,0))  
    targetY = (CROPBOTTOM - CROPTOP)*0.4
    offsetIndex = 0
    offsetErrorY = abs(targetY - unmatched[0][1])
    for i in range(len(unmatched)):
        errorY = abs(targetY - unmatched[i][1])
        if errorY < offsetErrorY:
            offsetIndex = i
            offsetErrorY = errorY
    offsetPoint = unmatched[offsetIndex]
    #print(offsetPoint[0]-250)
    #DrawCross(pointImage, (offsetPoint[0]-250,offsetPoint[1]), 6, (10,10,200)) 
    
    out.write(frame)
    
    cv2.imshow('frame', frame)
    cv2.imshow('mask', lineMask)
    #cv2.imshow('pointImage', pointImage)
    k = cv2.waitKey(50)
    if k%256 == 27:
        break
cap.release()
cv2.destroyAllWindows()
out.release()
    