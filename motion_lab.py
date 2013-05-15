import Image
import ImageDraw
import numpy
import sys
import math
import pygame

pygame.init()

WIDTH, HEIGHT = 280, 160
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

def total_occupied_pixels(image, pt1, pt2):
  x1, y1 = pt1
  x2, y2 = pt2
  WHITE = numpy.array([255], dtype = image.dtype)
  RED = numpy.array([255, 0, 0], dtype = image.dtype)
  count = 0
  tmp = image[y1: y2, x1: x2]
  #print tmp
  count = numpy.where(tmp == WHITE)
  count = len(count[0])
  return count

def center(image, color):
  color = numpy.array(color)
  x, y = numpy.where(image == color)
  n = len(x)
  return int(y.mean()), int(x.mean())

def grid(motion, image, size = 15):
  image = Image.fromarray(image)
  draw = ImageDraw.Draw(image)
  divx = WIDTH / size
  divy = HEIGHT / size
  AREA = size*size
  pixels = motion.copy()
  color, w = None, 1
  for i in range(divx):
    for j in range(divy):
      pt1 = i*size, j*size
      pt2 = (i + 1)*size, (j + 1)*size
      n = total_occupied_pixels(pixels, pt1, pt2)
      Rect = (pt1[0], pt1[1], pt2[0], pt2[1])
      if n > 0:
        w = 2
        color = (0, 255, 0)
      else: 
        w = 1
        color = (128, 128, 128)
      #Draw rectangle no soporta cambio de ancho de linea
      draw.line((pt1, (pt2[0], pt1[1])), color, width = w)
      draw.line(((pt2[0], pt1[1]), pt2), color, width = w)
      draw.line((pt2, (pt1[0], pt2[1])), color, width = w)
      draw.line(((pt1[0], pt2[1]), pt1), color, width = w)
        #draw.rectangle(Rect, outline = (128, 128, 128))
  pygame.display.update()
  image.save('tmp.png', 'PNG')
  return center(pixels, (255))

def grayscale(image):
  w, h, _ = image.shape
  gray = numpy.sum(image.astype(numpy.int), axis=2) / 3
  gray = numpy.array(gray, dtype = image.dtype)
  return gray

def threshold(image, umb):
  umb = numpy.array([umb], dtype = image.dtype)
  WHITE = numpy.array([255], dtype = image.dtype)
  out[numpy.where(image > umb)] = WHITE
  return out

def difference(im1, im2):
  a = im1.astype(numpy.int)
  b = im2.astype(numpy.int)
  diff = abs(a-b)
  diff = diff.astype(numpy.uint8)
  return diff

def direction(p, q, last):
  x1, y1 = p
  x2, y2 = q
  angle = math.atan2(p[1] - q[1], p[0] - q[0])
  if int(math.degrees(angle)) in range(135, 225):
    print "Derecha, ",math.degrees(angle)
    return pygame.font.SysFont("monospace", 15).render("->", 1, (0,0,0))
  elif int(math.degrees(angle)) in range(-45, 46):
    print "Izquierda, ",math.degrees(angle)
    return pygame.font.SysFont("monospace", 15).render("<-", 1, (0,0,0))
  elif int(math.degrees(angle)) in range(45, 136):
    print "Arriba, ", math.degrees(angle)
    return pygame.font.SysFont("monospace", 15).render("^", 1, (0,0,0))
  else:
    print 'Abajo, ', math.degrees(angle)
    return pygame.font.SysFont("monospace", 15).render("v", 1, (0,0,0))

current_frame = 0
movement = "Nothing"
frames = []
label = pygame.font.SysFont("monospace", 15).render("", 5, (0,0,0))
clock = pygame.time.Clock()
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  
  frame1 = Image.open('frames/output_frame_%d.png'%current_frame)
  current_frame += 1
  array1 = numpy.array(frame1)

  frame2 = Image.open('frames/output_frame_%d.png'%current_frame)
  array2 = numpy.array(frame2)
  current_frame += 1

  out = difference(array1, array2)
  out = grayscale(out)
  motion = threshold(out, 15)
  cent = grid(motion, array2)
  frames.append(cent)
  if len(frames) == 2:
    label = direction(frames[0], frames[1], movement)
    frames.pop(0)

  background = pygame.image.load("tmp.png")
  backgroundRect = background.get_rect()
  screen.blit(background, backgroundRect)
  screen.blit(label, (cent[0] - 20, cent[1] - 20))
  pygame.display.update()

  if current_frame >= 200: 
    break

