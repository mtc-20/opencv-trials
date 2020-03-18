#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:44:28 2020

@author: mtc-20
"""

import cv2
import dwa
import time
import numpy as np

# Initialization
cap=cv2.VideoCapture('J_shape_wideangle.avi')
#cap.set(3, 640)
#cap.set(4, 480)


#while(cap.isOpened()):
#    ret, frame=cap.read()
#    if ret == True:
#        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#        h,w,d = frame.shape
#        top = int(h*0.6)
#        gray[0:top, 0:w] = 0 
#        ret, thresh = cv2.threshold(gray, 127, 255, 0)
#        edges = cv2.Canny(thresh, 10, 150, apertureSize=3)
#        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        cv2.polylines(frame, contours, False, (255, 0, 0), 2)
#
##        cv2.imshow('canny', edges)
##        cv2.imshow('thresh', thresh)
#        cv2.imshow('frame',frame)
#        k = cv2.waitKey(1)
#        if k%256 == 27:
#            print("[INFO] ESC hit, closing...")
#            break
#    else:
#        print("[INFO] File not found or corrupted; closing...")
#        break
#    
## Close everything here
#cv2.destroyAllWindows()
#cap.release()
class Demo_image(object):
    def __init__(self):
        cv2.namedWindow('demo')
        cv2.setMouseCallback('demo', self.callback)
        self.point_cloud = []
        self.draw_points = []

        # Planner Settings
        self.vel = (0.0, 0.0)
        self.pose = (30.0, 60.0, 0)
        self.goal = None
        self.base = [-3.0, -2.5, +3.0, +2.5]
        self.config = dwa.Config(
                max_speed = 3.0,
                min_speed = -1.0,
                max_yawrate = np.radians(40.0),
                max_accel = 15.0,
                max_dyawrate = np.radians(110.0),
                velocity_resolution = 0.1,
                yawrate_resolution = np.radians(1.0),
                dt = 0.1,
                predict_time = 3.0,
                heading = 0.15,
                clearance = 1.0,
                velocity = 1.0,
                base = self.base)
        
        
        
    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.goal = (x/10, y/10)
            
    def main(self):
        image = cv2.imread('sample_0.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h,w,d = image.shape
        top = int(h*0.6)
        gray[0:top, 0:w] = 0
#        roi = gray[top:h, 0:w]
        ret, thresh = cv2.threshold(gray, 127, 255, 0)
        edges = cv2.Canny(thresh, 10, 150, apertureSize=3)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        lines = cv2.polylines(image, contours, False, (255, 0, 0), 1)
        
        print("contours len: ", len(contours), contours)
        for contour in contours:
            for c in contour:
                for pt in c:
                    #print("point: ", contour[0][0])
                    self.draw_points.append(pt)
                    self.point_cloud.append(pt)
                    #cv2.circle(image, tuple(contour[0][0]), 5, (255, 255, 255), -1)
            
        #print("drawpoints: ", self.draw_points)
        print("point cloud len:", len(self.point_cloud))
        self.pose = (w/20, 70.0, 0)
        while True:
            prev_time = time.time()
            self.map = np.zeros((720, 1280, 3), dtype=np.uint8)
            for point in self.draw_points:
                cv2.circle(self.map, tuple(point), 5, (255, 255, 255), -1)
                
            if self.goal is not None:
                cv2.circle(self.map, (int(self.goal[0]*10), int(self.goal[1]*10)),
                        4, (0, 255, 0), -1)
                if len(self.point_cloud):
                    # Planning
                    self.vel = dwa.planning(self.pose, self.vel, self.goal,
                            np.array(self.point_cloud, np.float32), self.config)
                    # Simulate motion
                    self.pose = dwa.motion(self.pose, self.vel, self.config.dt)
            
            pose = np.ndarray((3,))
            pose[0:2] = np.array(self.pose[0:2]) * 10
            pose[2] = self.pose[2]
    
            base = np.array(self.base) * 10
            base[0:2] += pose[0:2]
            base[2:4] += pose[0:2]
            
            # Not the correct rectangle but good enough for the demo
            width = base[2] - base[0]
            height = base[3] - base[1]
            rect = ((pose[0], pose[1]), (width, height), np.degrees(pose[2]))
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.map,[box],0,(0,0,255),-1)
            
            fps = int(1.0 / (time.time() - prev_time))
            cv2.putText(self.map, f'FPS: {fps}', (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(self.map, f'Point Cloud Size: {len(self.point_cloud)}',
                        (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
            cv2.imshow('frame', image)
            cv2.imshow('demo', self.map)
            k = cv2.waitKey(1)
            if k%256 == 27:
                break
        cv2.destroyAllWindows
        
        
class Demo(object):
    def __init__(self):
        cv2.namedWindow('frame')
#        cv2.resizeWindow("demo", 1280, 720)  
        cv2.setMouseCallback('frame', self.callback)
        self.drawing = False
        self.ctr = 0

        self.point_cloud = []
        self.draw_points = []

        # Planner Settings
        self.vel = (0.0, 0.0)
        self.pose = (60.0, 60.0, 0)
        self.goal = None
        self.base = [-3.0, -2.5, +3.0, +2.5]
        self.config = dwa.Config(
                max_speed = 3.0,
                min_speed = -1.0,
                max_yawrate = np.radians(40.0),
                max_accel = 15.0,
                max_dyawrate = np.radians(110.0),
                velocity_resolution = 0.1,
                yawrate_resolution = np.radians(1.0),
                dt = 0.1,
                predict_time = 3.0,
                heading = 0.15,
                clearance = 1.0,
                velocity = 1.0,
                base = self.base)
        
        
        
    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.goal = (x/10, y/10)
            
    def main(self):
        cap=cv2.VideoCapture('J_shape_wideangle.avi')
        while(cap.isOpened()):
            self.point_cloud = []
            self.draw_points = []
            prev_time = time.time()
            ret, frame=cap.read()
#            if ret != True:
#                break
            self.ctr += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h,w,d = frame.shape
            top = int(h*0.6)
            gray[0:top, 0:w] = 0 
            ret, thresh = cv2.threshold(gray, 127, 255, 0)
            edges = cv2.Canny(thresh, 10, 150, apertureSize=3)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.polylines(frame, contours, False, (255, 0, 0), 2)
            if self.ctr%10 == 0: 
                for contour in contours:
                    for c in contour:
                        for pt in c:
                    #print("point: ", contour[0][0])
                            self.draw_points.append(pt)
                            self.point_cloud.append(pt)
                #print("drawpoints: ", self.draw_points)
                    
            self.map = np.zeros((720, 1280, 3), dtype=np.uint8)
            for point in self.draw_points:
                cv2.circle(frame, tuple(point), 5, (255, 255, 255), -1)
                
            if self.goal is not None:
                cv2.circle(frame, (int(self.goal[0]*10), int(self.goal[1]*10)),
                        4, (0, 255, 0), -1)
                if len(self.point_cloud):
                    # Planning
                    self.vel = dwa.planning(self.pose, self.vel, self.goal,
                            np.array(self.point_cloud, np.float32), self.config)
                    print(self.vel)
                    # Simulate motion
                    self.pose = dwa.motion(self.pose, self.vel, self.config.dt)
                    
            pose = np.ndarray((3,))
            pose[0:2] = np.array(self.pose[0:2]) * 10
            pose[2] = self.pose[2]

            base = np.array(self.base) * 10
            base[0:2] += pose[0:2]
            base[2:4] += pose[0:2]
            
            # Not the correct rectangle but good enough for the demo
            width = base[2] - base[0]
            height = base[3] - base[1]
            rect = ((pose[0], pose[1]), (width, height), np.degrees(pose[2]))
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame,[box],0,(0,0,255),-1)
            
            fps = int(1.0 / (time.time() - prev_time))
            cv2.putText(frame, f'FPS: {fps}', (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.putText(frame, f'Point Cloud Size: {len(self.point_cloud)}',
                    (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
#            cv2.imshow('demo', self.map)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                print("[INFO] ESC hit, closing...")
                break
            
            elif k == ord('r'):
                self.point_cloud = []
                self.draw_points = []
                
if __name__ == '__main__':
    Demo().main()
    cv2.destroyAllWindows()
    cap.release()
                
