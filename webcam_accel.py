#!/usr/bin/python

import cv2

from xillybus_accel import *
from convert_img import *
from webcam_server import *

import sys
import numpy

def webcam_init():
  cv2.namedWindow('Input')
  cv2.namedWindow('Output')

  usbcam = cv2.VideoCapture(-1)
  #usbcam = cv2.VideoCapture('/home/zeddev/Videos/snake.mp4')

  sse = XillybusPipe(32)

  buf_in = numpy.empty((480,640,4), numpy.uint8)
  
  if usbcam.isOpened(): # try to get the first frame
    rval, frame = usbcam.read()
  else:
    rval = False
    frame = None
  
  return (usbcam, sse, frame, rval, buf_in)

def process_rgb(frame, buf_in = None):
  if buf_in is None:
    buf_in = numpy.empty((480,640,4), numpy.uint8)

  dim = frame.shape
  buf_in[0:dim[0],0:dim[1],0:dim[2]] = frame
  
  result = sse.process(buf_in)
  np_arr = numpy.ndarray((480,640,4), numpy.uint8, result)
  return np_arr[:,:,0:3]

def change_stream(stream, reset=False):
  mem = open('/dev/xillybus_mem_8','w')
  if reset:
    mem.write('\xFF')
  else:
    mem.write('\x00' + chr(stream))
  mem.close()

if __name__ == '__main__':
  (usbcam, sse, frame, rval, buf_in) = webcam_init()
  
  #netcam = NetworkReader()
  netcam = None

  select = 0
  octave = 0
  change = True

  use_net = False

  sel_list = map(ord,['`','1','2','3','4','5','6','7','8','9','0'])
  oct_list = map(ord,['q','w','e','r'])

  while rval:
    try:
      buf_out = process_rgb(frame,buf_in) # Do we need buf_in?
      cv2.putText(frame, str(sse.last_time),
        (32,32), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255))
      cv2.imshow('Input', frame)

      cv2.imshow('Output', buf_out)
      key = cv2.waitKey(10)
      
      if netcam is not None and use_net:
        rval = True
        netcam.update()
        frame = netcam.img
      else:
        rval, frame = usbcam.read()
      
      if key == 27: # exit on ESC
        break
      elif netcam is not None and key == ord('c'):
        use_net = not use_net
        if use_net:
          c = 'network'
        else:
          c = 'USB'
        print 'Switching to %s camera' % c
      elif key in sel_list:
        select = sel_list.index(key)
        print 'Selecting stream %d' % select
        change = True
      elif key in oct_list:
        octave = oct_list.index(key)
        print 'Selecting octave %d' % octave
        change = True
      
      if change:
        change = False
        change_stream(0,True)
        process_rgb(frame,buf_in)
        change_stream(octave*16 + select)
      
    except KeyboardInterrupt:
      break
