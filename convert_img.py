#!/usr/bin/python

import sys
import cv2

scale = 16

def red(gray):
  if gray < 128:
    out = gray * scale
  else:
    out = 0

  if out > 255:
    out = 255

  return out

def blue(gray):
  inv = 255-gray
 
  if inv < 128:
    out = inv * scale
  else:
    out = 0

  if out > 255:
    out = 255

  return out

filename = sys.argv[1] 
img = cv2.imread(filename)

cmap = [[red(i), 0, blue(i)] for i in range(256)]

s = img.shape
for r in range(s[0]):
  for c in range(s[1]):
    gray = img[r,c,0]
    img[r,c,:] = cmap[gray]

l = filename.split('.')
outname = l[0] + '_conv.png'
print outname
cv2.imwrite(outname, img)
