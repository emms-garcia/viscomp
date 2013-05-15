import Image
import cv2.cv as cv
import numpy
import sys
import math
import time

c = cv.CreateCameraCapture(0)
cv.SetCaptureProperty( c, cv.CV_CAP_PROP_FRAME_WIDTH, 280 )
cv.SetCaptureProperty( c, cv.CV_CAP_PROP_FRAME_HEIGHT, 160 )
VIDEOFILE = False

try:
  if ".avi" in sys.argv[1]:
    VIDEOFILE = True
    c = cv.CaptureFromFile( sys.argv[1] ) 
    NFRAMES = cv.GetCaptureProperty( c, cv.CV_CAP_PROP_FRAME_COUNT  )
    WIDTH = int(cv.GetCaptureProperty(c, cv.CV_CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cv.GetCaptureProperty(c, cv.CV_CAP_PROP_FRAME_HEIGHT))
except:
  print "Error, no se especifico un video de entrada."
  sys.exit()

def cv2array(im):
  depth2dtype = {
        cv.IPL_DEPTH_8U: 'uint8',
        cv.IPL_DEPTH_8S: 'int8',
        cv.IPL_DEPTH_16U: 'uint16',
        cv.IPL_DEPTH_16S: 'int16',
        cv.IPL_DEPTH_32S: 'int32',
        cv.IPL_DEPTH_32F: 'float32',
        cv.IPL_DEPTH_64F: 'float64',
    }

  arrdtype=im.depth
  a = numpy.fromstring(
         im.tostring(),
         dtype=depth2dtype[im.depth],
         count=im.width*im.height*im.nChannels)
  a.shape = (im.height,im.width,im.nChannels)
  return a

def array2cv(a):
  dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
  try:
    nChannels = a.shape[2]
  except:
    nChannels = 1
  cv_im = cv.CreateImageHeader((a.shape[1],a.shape[0]),
          dtype2depth[str(a.dtype)],
          nChannels)
  cv.SetData(cv_im, a.tostring(),
             a.dtype.itemsize*nChannels*a.shape[1])
  return cv_im


def total_occupied_pixels(image, pt1, pt2):
  x1, y1 = pt1
  x2, y2 = pt2
  WHITE = numpy.array([255, 255, 255], dtype = image.dtype)
  RED = numpy.array([255, 0, 0], dtype = image.dtype)
  count = 0
  tmp = image[y1: y2, x1: x2, :]
  count = numpy.where(tmp == WHITE)
  count = len(count[0])/10
    #print pt1, pt2, count
  return count

def center(image, color):
  color = numpy.array(color)
  x, y, _ = numpy.where(image == color)
  n = len(x)
  return int(y.mean()), int(x.mean())

def grid(image, motion, size = 15):
  divx = WIDTH / size
  divy = HEIGHT / size
  AREA = size*size
  pixels = cv2array(motion).copy()
  #centers = []
  for i in range(divx):
    for j in range(divy):
      pt1 = i*size, j*size
      pt2 = (i + 1)*size, (j + 1)*size
      n = total_occupied_pixels(pixels, pt1, pt2)
      #print n
      if n > AREA*0.00001:
        cv.Rectangle(image, pt1, pt2, cv.CV_RGB(0, 255, 0), 2)
        #centers.append((pt1[0] + size/2, pt1[1] + size/2))
      else: 
        cv.Rectangle(image, pt1, pt2, cv.CV_RGB(128, 128, 128), 1)
  #n = len(centers)
  #centers = [sum(i) for i in zip(*centers)] 
  #return centers[0]/n, centers[1]/n
  return center(pixels, (255, 255, 255))

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
  elif int(math.degrees(angle)) in range(-45, 46):
    print "Izquierda, ", math.degrees(angle)
  elif int(math.degrees(angle)) in range(45, 136):
    print "Arriba, ", math.degrees(angle)
  else:
    print 'Abajo', math.degrees(angle)
  return

current_frame = 0
movement = "Nothing"
frames = []
while True:
  if VIDEOFILE: cv.SetCaptureProperty(c, cv.CV_CAP_PROP_POS_FRAMES, current_frame )
  camera_image = cv.QueryFrame( c )
  frame1 = cv.CloneImage( camera_image )
  array1 = cv2array(frame1)

  camera_image = cv.QueryFrame( c )
  frame2 = cv.CloneImage( camera_image )
  array2 = cv2array(frame2)

  out = difference(array1, array2)
  out = grayscale(out)
  motion = threshold(out, 15)

  motion = array2cv(out)
  cent = grid(frame1, motion)
  frames.append(cent)

  if len(frames) == 2:
    direction(frames[0], frames[1], movement)
    frames.pop(0)

  cv.ShowImage('e2', frame1)
  current_frame += 1
  if current_frame >= NFRAMES - 1: 
    break

  if cv.WaitKey(5) == 27:
    break
