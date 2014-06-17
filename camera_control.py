#!/usr/bin/python

import sys
from i2c_stream import *

class CameraControl:
  def __init__(self, useBP = False):
    if(useBP):
      self.i2c = BP_I2C()
    else:
      self.i2c = XB_I2C()

  def turn_on(self):
    self.i2c.start()
    self.i2c.write([0x78, 0x03, 0x02])
    self.i2c.stop()
    print 'Camera on'

  def turn_off(self):
    self.i2c.start()
    self.i2c.write([0x78, 0x03, 0x40])
    self.i2c.stop()
    print 'Camera off'

  def do_command(self, cmd):
    if cmd == 'n':
      self.turn_on()
    elif cmd == 'f':
      self.turn_off()
  
  def close(self):
    self.i2c.close()

if __name__ == '__main__':
  cc = CameraControl()

  if len(sys.argv) > 1:
    cc.do_command(sys.argv[1])
  else:
    cmd = raw_input('Command: ')
    while cmd != 'q':
      cc.do_command(cmd)
      cmd = raw_input('Command: ')

  cc.close()
