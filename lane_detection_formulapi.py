#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:20:14 2020

Taken from FormulaPi blog

@author: mtc-20
"""

import cv2
import numpy as np
import math

# Initialization
image = cv2.imread("frame_1.png")

# ROI
height, width, channel = image.shape
cropTop = int(height*0.6)
cropBottom = int(height*1.0)
cropped = image[cropTop:cropBottom, :]

# Remove non-track area
wallR = 60
wallG = 60
wallB = 60
walls = cv2.inRange(cropped, np.array((0, 0, 0)), np.array((wallB, wallG, wallR)))
erodeSize = 5
erodeKernel = np.ones((erodeSize, erodeSize), np.uint8)
walls = cv2.erode(walls, erodeKernel)
#cv2.imshow('walls.jpg', walls)

# Split colour channels
blue, green, red = cv2.split(cropped)
maxImage = np.maximum(np.maximum(red, blue), green)
# Apply gains and corrections
red = red*1.0
green = green*1.0
blue = blue*1.15
red = np.clip(red, 0, 255)
green = np.clip(green, 0, 255)
blue = np.clip(blue, 0, 255)
red = np.array(red, dtype= np.uint8)
green = np.array(green, dtype= np.uint8)
blue = np.array(blue, dtype= np.uint8)
maxImage = np.maximum(np.maximum(red, blue), green)

# Remove dark portions
red[red<maxImage] = 0
green[green<maxImage] = 0
blue[blue<maxImage] = 0
merged = cv2.merge([blue, green, red])
# Apply gains and corrections
highLevel = merged*10
highLevel = np.clip(highLevel, 0, 255)
highLevel = np.array(highLevel, np.uint8)

exclude = walls > 0
red[exclude] = 0
green[exclude] = 0
blue[exclude] = 0
red   = cv2.erode(red,   erodeKernel)
green = cv2.erode(green, erodeKernel)
blue  = cv2.erode(blue,  erodeKernel)
merged = cv2.merge([blue, green, red])

whiteWalls = cv2.merge([walls, walls, walls])
mergedWalls = cv2.addWeighted(merged, 1.0, whiteWalls, 1.0, 0)

# mask for scan 
red   = red   > 0
green = green > 0
blue  = blue  > 0
walls = walls > 0

grid = 100
scanLines = []
for i in range(grid):
    position = (i/float(grid))*height
    position = int(position)
    if position<cropTop:
        pass
    elif position>cropBottom:
        pass
    else:
        croppedY = int(position - cropTop)
        scanLines.append(croppedY)
print(scanLines)

scanLineImage = np.zeros_like(cropped)
colourWhite = (255,255,255)
for y in scanLines:
    cv2.line(scanLineImage, (0,y), (width-1,y), colourWhite, 1)
cv2.imshow('scanImage', scanLineImage)
        
def SweepLine(mask, y):
    found = []
    line = mask[y,:]
    changed = np.where(line[:-1] != line[1:])[0]
    for i in changed:
        if i<2 or i>(width-3):
            pass
        else:
            found.append(i)
    return found

# The values of try1, try2, try3 are used to attempt a match with target
# Any matches are added to existing lists matched1, matched2, matched3
# Any values which cannot be matched are added to the existing list unmatched
def FindMatches(y, target, try1, try2, try3, matched1, matched2, matched3, unmatched):
    maxSeparation = int(width*0.05)
    while len(target)>0:
        xt = target.pop()
        matched = False
        if try1:
            for x1 in try1:
                if abs(x1-xt)<maxSeparation:
                    matched = True
                    try1.remove(x1)
                    x = (xt+x1)/2
                    matched1.append((x,y))
                    break
                if matched:
                    continue
        if try2:
            for x2 in try2:
                if abs(x2-xt)<maxSeparation:
                    matched = True
                    try2.remove(x2)
                    x = (xt+x2)/2
                    matched1.append((x,y))
                    break
                if matched:
                    continue
        if try3:
            for x3 in try3:
                if abs(x3-xt)<maxSeparation:
                    matched = True
                    try3.remove(x3)
                    x = (xt+x3)/2
                    matched1.append((x,y))
                    break
                if matched:
                    continue
        unmatched.append((xt, y))
        
# Make matched lists
matchRG = []
matchRB = []
matchRW = []
matchGB = []
matchGW = []
unmatched = []
# Loop over each line
for y in scanLines:
    edgeR = SweepLine(red, y)
    edgeG = SweepLine(green, y)
    edgeB = SweepLine(blue, y)
    edgeW = SweepLine(walls, y)
    FindMatches(y,edgeR, edgeG, edgeB, edgeW, matchRG, matchRB, matchRW, unmatched)
    FindMatches(y, edgeG, edgeB, edgeW, None, matchGB, matchGW, None, unmatched)
    # Add leftover points to unmatched
    others = edgeB[:]
    others.extend(edgeW)
    for x in others:
        unmatched.append((x,y))
        
def DrawCross(image, XY,RGB):
    x, y = XY[0], XY[1]
    crossSize = 5
    width = image.shape[0]
    height = image.shape[1]
    points = []
    for i in range(-crossSize, crossSize+1):
        points.append((x+i,y))
        points.append((x,y+i))
    for point in points:
        x = point[0]
        y = point[1]
        if (x>=0) and (y>=0) and (x<width) and (y<height):
            image.itemset((int(y),int(x),0), RGB[2])
            image.itemset((int(y),int(x),1), RGB[1])
            image.itemset((int(y),int(x),2), RGB[0])
            
            
pointImage = cropped[:,:,:]
for point in matchRG:
    DrawCross(pointImage, point, (255,255,0))
for point in matchRB:
    DrawCross(pointImage, point, (255, 0, 255))
for point in matchRW:
    DrawCross(pointImage, point, (255, 0, 0))
for point in matchGB:
    DrawCross(pointImage, point, (0, 255, 255))
for point in matchGW:
    DrawCross(pointImage, point, (0, 255, 0))
for point in unmatched:
    DrawCross(pointImage, point, (127, 127, 127))    
cv2.imshow('points', pointImage)
    
lines = [matchRW, matchRB, matchRB, matchGB, matchGW]
count = 0
index = 0
for i in range(len(lines)):
    if len(lines[i])>count:
        index = i
        count = len(lines[i])

lineIndexToOffset = {0:3.0, 1:1.0, 2:0.0, 3:-1.0, 4:-3}
lineOffset = lineIndexToOffset[index]
bestLine = lines[index]

# Distance
targetY = (cropBottom - cropTop)*0.33
offsetIndex = 0
offsetErrorY = abs(targetY - bestLine[0][1])
for i in range(len(bestLine)):
    errorY = abs(targetY - bestLine[i][1])
    if errorY < offsetErrorY:
        offsetIndex = i
        offsetErrorY = errorY
offsetPoint = bestLine[offsetIndex]

targetX = width/2
lanewidth = 1250 # measure manually at targetY value and resolution
offsetX = offsetPoint[0] -targetX
offsetX = offsetX/lanewidth
print (offsetX)
# Compute
trackOffset = lineOffset + offsetX
print (trackOffset)

# delta
dXdY = []
for i in range(1, len(bestLine)):
    dX = float(bestLine[i-1][0] - bestLine[i][0])
    dY = float(bestLine[i][1] - bestLine[i-1][1])
    dXdY.append((dX, dY))

# Track angle ( between lane and bot)
gradient = 0
for changes in dXdY:
    gradient += changes[0]/changes[1]
gradient /= len(dXdY)

# Perspective correction
correctionFactor = 2.6/0.25 # perspective error, gradient/offset_of_lane
correction = correctionFactor*offsetX
gradient -= correction
angle = math.atan(gradient) * 180 / math.pi

# gradient of curvature
gradient2 = 0.0
lastG = dXdY[0][0]/dXdY[0][1]
for i in range(1, len(dXdY)):
    nextG = dXdY[i][0]/dXdY[i][1]
    changeG = lastG - nextG
    gradient2 += changeG / dXdY[i][1]
    lastG = nextG
gradient2 /= len(dXdY)

    

    



cv2.imshow('max2', maxImage)
cv2.imshow('merged', merged)
cv2.imshow('mergedMax', highLevel)
# Display 
cv2.imshow('green', green)
cv2.imshow('blue', blue)
cv2.imshow('red', red)
cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()