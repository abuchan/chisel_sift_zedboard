#!/usr/bin/python

import sys
import cv2

def red(gray, scale=16):
  if gray < 128:
    out = gray * scale
  else:
    out = 0

  if out > 255:
    out = 255

  return out

def blue(gray, scale=16):
  inv = 255-gray
 
  if inv < 128:
    out = inv * scale
  else:
    out = 0

  if out > 255:
    out = 255

  return out

def colormap(scale=16):
  return [[red(i,scale), 0, blue(i,scale)] for i in range(256)]

if __name__ == '__main__':
  filename = sys.argv[1] 
  img = cv2.imread(filename)

  cmap = colormap()

  s = img.shape
  for r in range(s[0]):
    for c in range(s[1]):
      gray = img[r,c,0]
      img[r,c,:] = cmap[gray]

  l = filename.split('.')
  outname = l[0] + '_conv.png'
  print outname
  cv2.imwrite(outname, img)
