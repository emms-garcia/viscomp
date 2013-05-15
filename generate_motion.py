import Image
import random
import numpy
import sys
import os
import time

WIDTH, HEIGHT = 280, 160
bg = numpy.empty((HEIGHT, WIDTH))
bg.fill(255)
bg = Image.fromarray(bg).convert('RGB')
os.system("rm jpgs/*")

def draw_square(image, (x, y), k, color, n):
  w, h = image.size
  pix = image.load()
  k = [k for k in range(-k/2 + 1, k/2 + 1)]
  for i in k:
    for j in k:
      dx, dy = x + i, y + j
      pix[dx, dy] = color
  image.save('jpgs/output_frame_%s.png'%n, 'PNG')
  return image

points = []
size = 20
speed = size/2
color = (255, 0, 0)
num = 0
x1, y1 = random.randrange(0+size, WIDTH-size, speed), random.randrange(0+size, HEIGHT-size, speed)
INICIO = time.time()
t = 0
while t < float(sys.argv[1])/4:
  x2, y2 = random.randrange(0+size, WIDTH-size, size), random.randrange(0+size, HEIGHT-size, size)
  if x1 > x2:
    while x1 is not x2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      x1 -= speed
      if x1 == x2:
        break
      
  elif x1 < x2:
    while x1 is not x2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      x1 += speed
      if x1 == x2:
        break
  if y1 > y2:
    while y1 is not y2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      y1 -= speed
      if y1 == y2:
        break
  elif y1 < y2:
    while y1 is not y2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      y1 += speed
      if y1 == y2:
        break
  x1, y1 = x2, y2
  ACTUAL = time.time()
  t = ACTUAL - INICIO

os.system("avconv -f image2 -i jpgs/output_frame_%d.png videos/tmp.avi")
os.system("mencoder videos/tmp.avi -ovc raw -vf format=i420 -nosound -o videos/out.avi")
os.system("rm videos/tmp.avi")
