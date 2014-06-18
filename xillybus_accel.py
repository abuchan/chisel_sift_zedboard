import numpy
import threading
import time

class WriteThread(threading.Thread):
  def __init__(self, data, device):
    threading.Thread.__init__(self)
    self.data = data
    self.device = device

  def run(self):
    w = open(self.device,'w')
    w.write(self.data)
    w.close()

class XillybusPipe():
  def __init__(self, nbits):
    self.nbits = nbits
    self.open()

  def open(self):
    self.r = open('/dev/xillybus_read_%d' % self.nbits,'r')
    self.w = open('/dev/xillybus_write_%d' % self.nbits, 'w')
    
  def process(self, data_in):
    total_size = data_in.size * data_in.dtype.itemsize

    start_time = time.time()
    self.w.write(data_in)
    result = self.r.read(total_size)
    stop_time = time.time()
    
    self.last_time = stop_time-start_time
    return result

  def read(self, n_bytes=None):
    start_time = time.time()
    
    if (n_bytes is None):
      result = self.r.read()
    else:
      result = self.r.read(n_bytes)

    stop_time = time.time()
    self.last_time = stop_time-start_time
    return result

  def close(self):
    self.r.close()
    self.w.close()

def xb_accel(data_array, nbits):
  
  r = open('/dev/xillybus_read_%d' % nbits,'r')
  w = WriteThread(data_array, '/dev/xillybus_write_%d' % nbits)
  w.start()

  return r.read(data_array.size * data_array.dtype.itemsize)

