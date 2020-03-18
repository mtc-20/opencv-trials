#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:57:59 2020

  Taken from StackOverflow https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv-python
    Alternatively use > cap.set(cv2.CAP_PROP_BUFFERSIZE, 0) if OpenCV >= 3.4

@author: mtc-20
"""

import cv2, Queue, threading

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = Queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


if __name__ == '__main__':
    cap = VideoCapture(0)
    while cap.cap.isOpened():
        frame = cap.read()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.cap.release()