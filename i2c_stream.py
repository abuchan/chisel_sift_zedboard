#!/usr/bin/python

import sys

class BP_I2C:
  def __init__(self):
    from pyBusPirate.BinaryMode.I2C import *
    
    self.i2c = I2C('/dev/ttyUSB0', 115200)
    if not self.i2c.BBmode():
      print 'Failed to enter BitBang mode'
      sys.exit()

    if not self.i2c.enter_I2C():
      print 'Failed to enter I2C mode'
      sys.exit()

    if not self.i2c.set_speed(I2CSpeed._400KHZ):
      print 'Failed to set I2C speed'
      sys.exit()

    self.i2c.timeout(0.2)

  def close(self):
    if not self.i2c.resetBP():
      print 'Failed to reset BP to user terminal'

  def start(self):
    self.i2c.send_start_bit()

  def stop(self):
    self.i2c.send_stop_bit()

  def write(self, data):
    self.i2c.bulk_trans(len(data), data)

class XB_I2C:
  def __init__(self):
    self.w = open('/dev/xillybus_write_8','w')

  def close(self):
    self.w.close()

  def start(self):
    self.w.write('\xff\x02\x01')
    self.w.flush()

  def stop(self):
    self.w.write('\xff\x02\x02')
    self.w.flush()

  def write(self, data):
    self.w.write(''.join(map(chr,data)))
    self.w.flush()

