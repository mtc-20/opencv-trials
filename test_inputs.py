#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:42:09 2020

@author: mtc-20
"""
import time
import threading
from inputs import get_gamepad

#while 1:
#    events = get_gamepad()
#    for event in events:
#        print(event.ev_type, event.code, event.state)
        
        
class Gamepad():
    def __init__(self):
        self.running = True
        self.start_status = False
        self.threading_status = True
        self.key_map = {'AN_UD':'ABS_Y',
                        'AN_LR':'ABS_X',
                        'DPAD_UD': 'ABS_HAT0Y',
                        'DPAD_LR': 'ABS_HAT0X',
                        'START':'BTN_START'}
    def get_event(self):
        name = threading.currentThread().getName()
        print("Thread ", name, " start...")
        while self.threading_status:
            events = get_gamepad()
            for event in events:
                if event.code == self.key_map['DPAD_UD']:
                    if event.state == -1:
                        print('forward')
                    elif event.state == 1:
                        print('reverse')
                    elif event.state == 0:
                        print('stop')
                if event.code == self.key_map['DPAD_LR']:
                    if event.state == -1:
                        print('left')
                    elif event.state == 1:
                        print('right')
                    elif event.state == 0:
                        print('stop')
                        
                        
if __name__ == '__main__':
    try:
        gamepad = Gamepad()
        x = threading.Thread(name='Gamepad',target=gamepad.get_event)
        x.start()
        print('Starting main loop')
        while True: 
            pass
    except Exception:
        print(Exception)
        