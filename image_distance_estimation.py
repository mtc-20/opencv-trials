#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:46:26 2020

@author: mtc-20
"""


"""
Load reference image and find pixel coordinates of points of interest

left clicking on the image will draw a circle at that point, print the coordinate
 and append to a list
"""
import cv2
refpt = []
def callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        refpt.append((x,y))
        print(refpt)
        cv2.circle(image, (x,y), 1, (255,255,0),1)

# Initialization        
image = cv2.imread('captured.jpg')
cv2.namedWindow("image")
cv2.setMouseCallback("image", callback)   

height, width, channel = image.shape     
while True:
    cv2.imshow('image', image)
    k = cv2.waitKey(1)
    if k%256==27:
        break
    
cv2.destroyAllWindows()


"""
Generate data points from obtained coordinates into x (image) and 
y (actual distance) values

The x values are extracted from the ref_pt list, however it doesn't check if 
the coordinate points in the list are along the same x coordinate  
The y values need to be done manually
"""
import numpy as np
x_values = []
for x,y in refpt:
    x_values.append(height - y)
#    print(x,y)
print(x_values)
x_data = np.array(x_values)
print(x_data, type(x_data))    
#x_data = np.array([60,84,98,103]) 
y_data = np.array([25, 50, 100, 150])

# Plot the data points
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
plt.scatter(x_data, y_data)

## Try to best fit curve with known functions
#from scipy import optimize
#
##def test_func(x,a,b):
##    return a*np.exp(b*x)
#
#def test_func(x,a,b,c):
#    return a*(x**2) + (b*x) + c
#
## Save the function parameters
#params, params_covariance = optimize.curve_fit(test_func, x_data, y_data, )
#print(params)
#
## Plot the results
#plt.figure(figsize=(6, 4))
#plt.scatter(x_data, y_data, label='Data')
#plt.plot(x_data, test_func(x_data, params[0], params[1], params[2]),
#         label='Fitted function')
#plt.legend(loc='best')
#plt.show()



# Alternatively use this for interpolation
from scipy.interpolate import interp1d
xnew = np.linspace(x_data.min(), x_data.max(), 30) 
f = interp1d(x_data, y_data) # linear fit
#f = interp1d(x_data, test_func(x_data, params[0], params[1], params[2]), kind='quadratic')
f2 = interp1d(x_data, y_data, kind='quadratic') # quadratic fit
plt.plot(x_data, y_data, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
#plt.plot(x_data, test_func(x_data, params[0], params[1], params[2]))
plt.legend(['data', 'linear', 'quadratic'], loc='best')

# test the interpolation function
print(f2(103))
print(f2(50))
