#!/usr/bin/python

from xillybus_accel import *
import threading
import cv2
import time
import numpy

def raw_to_np(data):
  np_arr = numpy.ndarray((480,640,4), numpy.uint8, data)
  return np_arr[:,:,0:3]

class FrameBuffer(threading.Thread):
  def __init__(self):
    super(FrameBuffer, self).__init__()
    self.daemon = True
    self.pipe = XillybusPipe(32)
    self.is_open = True
    self.lock = threading.Condition()
    self.write_data = None
    self.n_frames = 0

  def run(self):
    while(True):
      quitting = False
      self.lock.acquire()
      if (self.is_open):
        sync = self.pipe.read(4)
        while sync != '\x00\x00\x00\xFF':
          sync = self.pipe.read(4)
        
        self.write_data = self.pipe.read(640*480*4)
        self.n_frames = self.n_frames + 1
      else:
        quitting = True
      self.lock.release()
      
      if (quitting):
        break
  
  def get_frame(self):
    return self.write_data

  def close(self):
    self.lock.acquire()
    self.is_open = False
    self.lock.release()

if __name__ == '__main__':
  fb = FrameBuffer()
  fb.start()
  while fb.write_data == None:
    time.sleep(10)

  cv2.namedWindow('test')
  
  key = cv2.waitKey(10)
  while key != 27:
    cv2.imshow('test',raw_to_np(fb.write_data))
    key = cv2.waitKey(1)
  fb.close()
