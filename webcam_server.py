#/usr/bin/python

import cv2
import socket
import threading
import numpy
import time
import subprocess

host = 'localhost'
port = 50007

img_w = 640
img_h = 480
img_b = 3
img_size = img_w * img_h * img_b

class CamReader(threading.Thread):
  def __init__(self, sock = None):
    super(CamReader, self).__init__()
    self.cam = cv2.VideoCapture(-1)
    self.daemon = True

    if (sock == None):
      self.sock = None
      print 'Opening server'
      self.pipe = subprocess.Popen(['nc','-l',str(port)],
        stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind((host,port))
      self.sock.listen(1)
      self.conn, self.addr = self.sock.accept()
      print 'Accepted connection'
      self.conn.setblocking(0)

  def read_frame(self):
    print 'grabbing frame'
    self.rval, self.frame = self.cam.read()

  def is_request(self):
    data = ''
    
    if (self.sock == None):
      data = self.pipe.stdout.read(1)
    else:
      try:
        data = self.conn.recv(1)
      except IOError:
        pass
     
    return data == 'a'

  def send_frame(self):
    if (self.sock == None):
      self.pipe.stdin.write(self.frame.data)
      self.pipe.stdin.flush()
    else:
      n_sent = 0
      while n_sent < img_size:
        sent = self.conn.send(self.frame.data[n_sent:])
        print 'sending frame, %d' % sent
        n_sent = n_sent + sent

  def close_connections(self):
    if (self.sock != None):
      print 'Closing connections'
      self.conn.close()
      self.sock.close()
    
  def run(self):
    self.read_frame()

    while(self.rval):
      try:
        req = self.is_request()
        while (not req):
          time.sleep(0.1)
          req = self.is_request()
        self.read_frame()
        self.send_frame()
      except KeyboardInterrupt:
        self.close_connections()
        break

class NetworkReader(threading.Thread):
  def __init__(self, sock=None):
    super(NetworkReader, self).__init__()
    if (sock == None):
      self.sock = None
      print 'Opening client'
      self.pipe = subprocess.Popen(['nc',host,str(port)],
        stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((host,port))
    
    self.win = cv2.namedWindow('test')
    self.daemon = True

  def ask(self):
    print 'Sending a'
    if (self.sock == None):
      self.pipe.stdin.write('a')
      self.pipe.stdin.flush()
    else:
      self.sock.send('a')
    
  def get_img(self):
    if (self.sock == None):
      data = self.pipe.stdout.read(img_size)
    else:
      n_read = 0
      data = ''
      while n_read < img_size:
        new_data = self.sock.recv(img_size)
        print 'Received data, %d long' % len(new_data)
        data = data + new_data
        n_read = n_read + len(new_data)
    
    print 'Got full image'
    self.img = numpy.ndarray((img_h,img_w,img_b), numpy.uint8, data)
  
  def close_connections(self):
    print 'Closing connections'
    self.sock.close()
  
  def run(self):
    while(True):
      try:
        self.ask()
        self.get_img()

        cv2.imshow('test',self.img)
        cv2.waitKey(10)
      except KeyboardInterrupt:
        self.close_connections()
        break

