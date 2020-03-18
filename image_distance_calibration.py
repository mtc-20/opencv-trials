#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:30:03 2020

@author: mtc-20
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pickle

# Function Definitions
def save_callback(event, x, y, flags, param):
    global refpt
    if event == cv2.EVENT_LBUTTONDOWN:
        refpt.append((x,y))
        print(refpt)
        cv2.circle(image, (x,y), 1, (255,255,0),1)



#Generate data points from obtained coordinates into x (image) and 
#y (actual distance) values
#The x values are extracted from the ref_pt list, however it doesn't check if 
#the coordinate points in the list are along the same x coordinate  
#The y values need to be done manually, for now they're set to 4 distances: 25,
#50, 100, 150 cm      
def fit_points(refpt, y_data):
    x_values =[]
    height = image.shape[0]
    for x,y in refpt:
        x_values.append(height - y)
    
    x_data = np.array(x_values)
    print(x_data)
#    y_data = np.array([25, 50, 100, 150])
#    plt.figure(figsize=(6, 4))
#    plt.scatter(x_data, y_data)
    quad_curve = interp1d(x_data, y_data, kind='quadratic')
    
    xnew = np.linspace(x_data.min(), x_data.max(), 30) 
    plt.plot(x_data, y_data, 'o', xnew, quad_curve(xnew), '-')
    plt.legend(['data', 'quadratic'], loc='best')
    with open('interpolation.txt', 'wb') as fp:
        pickle.dump(quad_curve,fp)
    return quad_curve

#Simple tool to save the coordinates of points of interest from calibration 
#image
def find_coord(image):
    global refpt
    refpt = []
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", save_callback)  
    #height, width, channel = image.shape
    while True:
        cv2.imshow('image', image)
        k = cv2.waitKey(1)
        if k%256==27:
            break    
    cv2.destroyAllWindows()
    return fit_points(refpt, np.array([25, 50, 100, 150]))



if __name__ == '__main__':
    image = cv2.imread('captured.jpg')
    f = find_coord(image)
    fit_points(refpt, np.array([25, 50, 100, 150]))

    with open('interpolation.txt', 'rb') as fp:
        loaded_func = pickle.load(fp)
    print(f(103))
    print(loaded_func(100))