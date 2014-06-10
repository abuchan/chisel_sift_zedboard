#!/usr/bin/python

import sys
from pyBusPirate.BinaryMode.I2C import *

def camera_on(bp_i2c):
  bp_i2c.send_start_bit()
  bp_i2c.bulk_trans(3, [0x78, 0x03, 0x02])
  bp_i2c.send_stop_bit()
  print 'Camera on'

def camera_off(bp_i2c):
  bp_i2c.send_start_bit()
  bp_i2c.bulk_trans(3, [0x78, 0x03, 0x40])
  bp_i2c.send_stop_bit()
  print 'Camera off'

def do_command(bp_i2c, cmd):
  if cmd == 'n':
    camera_on(bp_i2c)
  elif cmd == 'f':
    camera_off(bp_i2c)

def i2c_setup():
  i2c = I2C('/dev/ttyUSB0', 115200)
  if not i2c.BBmode():
    print 'Failed to enter BitBang mode'
    sys.exit()

  if not i2c.enter_I2C():
    print 'Failed to enter I2C mode'
    sys.exit()

  if not i2c.set_speed(I2CSpeed._400KHZ):
    print 'Failed to set I2C speed'
    sys.exit()

  i2c.timeout(0.2)
  return i2c

def i2c_close(bp_i2c):
  if not bp_i2c.resetBP():
    print 'Failed to reset BP to user terminal'
  
if __name__ == '__main__':
  bp_i2c = i2c_setup()

  if len(sys.argv) > 1:
    do_command(bp_i2c, sys.argv[1])
  else:
    cmd = raw_input('Command: ')
    while cmd != 'q':
      do_command(bp_i2c, cmd)
      cmd = raw_input('Command: ')

  i2c_close(bp_i2c)
