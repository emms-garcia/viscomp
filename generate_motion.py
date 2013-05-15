import Image
import random
import numpy
import sys
import os

WIDTH, HEIGHT = 280, 160
bg = numpy.empty((HEIGHT, WIDTH))
bg.fill(255)
bg = Image.fromarray(bg).convert('RGB')

def draw_square(image, (x, y), size, color, n):
  w, h = image.size
  pix = image.load()
  size = [k for k in range(-size/2 + 1, size/2 + 1)]
  for i in size:
    for j in size:
      dx, dy = x + i, y + j
      pix[dx, dy] = color
  image.save('jpgs/output_frame_%s.png'%n, 'PNG')
  return image

points = []
size = 21
color = (255, 0, 0)
num = 0
x1, y1 = random.randint(0+size, WIDTH-size), random.randint(0+size, HEIGHT-size)
for i in range(int(sys.argv[1])):
  x2, y2 = random.randint(0+size, WIDTH-size), random.randint(0+size, HEIGHT-size)
  if x1 > x2:
    while x1 is not x2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      x1 -= 1 
      if x1 == x2:
        break
      
  elif x1 < x2:
    while x1 is not x2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      x1 += 1
      if x1 == x2:
        break
  if y1 > y2:
    while y1 is not y2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      y1 -= 1
      if y1 == y2:
        break
  elif y1 < y2:
    while y1 is not y2:
      frame = bg.copy()
      frame = draw_square(frame, (x1, y1), size, color, num)
      num += 1
      y1 += 1
      if y1 == y2:
        break
  x1, y1 = x2, y2

os.system("avconv -f image2 -i jpgs/output_frame_%d.png videos/tmp.avi")
os.system("mencoder videos/out.avi -ovc raw -vf format=i420 -nosound -o videos/out.avi")
os.system("rm videos/tmp.avi")
