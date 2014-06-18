#!/usr/bin/python

from xillybus_accel import *
import threading
import cv2
import time
import numpy

SYNC_TOKEN =  '\x00\x00\x00\xFF'

def raw_to_np(data):
  np_arr = numpy.ndarray((480,640,4), numpy.uint8, data)
  return np_arr[:,:,0:3]

class FrameBuffer(threading.Thread):
  def __init__(self, syncing = False):
    super(FrameBuffer, self).__init__()
    self.daemon = True
    self.pipe = XillybusPipe(32)
    self.is_open = True
    self.lock = threading.Condition()
    #self.frame = None
    self.frame = (640*480*8)*'\x00'
    self.n_frames = 0
    self.syncing = syncing
    self.sync = ''

  def run(self):
    while(True):
      quitting = False
      self.lock.acquire()
      if (self.is_open):
        self.grab_frame()
        self.n_frames = self.n_frames + 1
      else:
        quitting = True
        self.pipe.close()
      self.lock.release()
      
      if (quitting):
        break
  
  def grab_frame(self):
    if (self.syncing):
      data = self.pipe.read((640*480+1)*4)
      self.frame = data[4:]
      self.sync = data[0:4]
    else:
      self.frame = self.pipe.read(640*480*4)
      #self.pipe.close()
      #self.pipe.open()

  def sync_frame(self):
    if not self.syncing or self.frame == None:
      return False
    else:
      if self.sync != SYNC_TOKEN:
        sync_idx = self.frame.index(SYNC_TOKEN)
        self.lock.acquire()
        self.pipe.read(sync_idx+4)
        self.grab_frame()
        self.lock.release()

    return self.sync == SYNC_TOKEN

  def get_frame(self):
    return self.frame

  def close(self):
    self.lock.acquire()
    self.is_open = False
    self.lock.release()

  def show_frame(self):
    cv2.namedWindow('test')
    cv2.imshow('test',raw_to_np(self.frame))
    
if __name__ == '__main__':
  fb = FrameBuffer()
  fb.start()
  
  while fb.frame == None:
    time.sleep(10)
  
  fb.sync_frame()

  key = cv2.waitKey(10)
  
  while key != 27:
    fb.show_frame()
    key = cv2.waitKey(1)

  fb.close()
