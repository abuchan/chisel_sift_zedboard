#!/usr/bin/python

import cv2

from xillybus_accel import *
from convert_img import *

import numpy

def webcam_init():
  cv2.namedWindow('Input')
  cv2.namedWindow('Output')

  webcam = cv2.VideoCapture(-1)
  #webcam = cv2.VideoCapture('/home/zeddev/Videos/snake.mp4')

  sse = XillybusPipe(32)

  buf_in = numpy.empty((480,640,4), numpy.uint8)
  
  if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
  else:
    rval = False
    frame = None
  
  return (webcam, sse, frame, rval, buf_in)

def process_rgb(frame, buf_in = None):
  if buf_in is None:
    buf_in = numpy.empty((480,640,4), numpy.uint8)

  dim = frame.shape
  buf_in[0:dim[0],0:dim[1],0:dim[2]] = frame
  
  result = sse.process(buf_in)
  np_arr = numpy.ndarray((480,640,4), numpy.uint8, result)
  return np_arr[:,:,0:3]

  #cmap = numpy.ndarray((256,3),numpy.uint8,colormap())
  #cmap = colormap()
  #conv = [cmap[p&0xFF] for p in result]
  #np_arr = numpy.ndarray((480,640,3), numpy.uint8, conv)
  #return np_arr

def change_stream(stream, reset=False):
  mem = open('/dev/xillybus_mem_8','w')
  if reset:
    mem.write('\xFF')
  else:
    mem.write('\x00' + chr(stream))
  mem.close()

if __name__ == '__main__':
  (webcam, sse, frame, rval, buf_in) = webcam_init()

  while rval:
    try:
      cv2.imshow('Input', frame)
      buf_out = process_rgb(frame)
      cv2.imshow('Output', buf_out)
 
      rval, frame = webcam.read()
      key = cv2.waitKey(10)
      if key == 27: # exit on ESC
        break
      elif key == ord('`'):
        print 'Selecting stream 0'
	change_stream(0,True)
	process_rgb(frame)
        change_stream(0)
      elif key in range(ord('1'),ord('9')+1):
        print 'Selecting stream %d' % (key-0x30)
	change_stream(0,True)
	process_rgb(frame)
        change_stream(key-0x30)
      elif key == ord('0'):
        print 'Selecting stream 10'
	change_stream(0,True)
	process_rgb(frame)
        change_stream(10)

    except KeyboardInterrupt:
      break
