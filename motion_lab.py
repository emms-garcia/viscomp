import Image
import cv2.cv as cv
import numpy
import sys

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
  print "No se especifico video de entrada, usando camara web."
  print "Usa %s -h   o %s --help para conocer los parametros."%(sys.argv[0], sys.argv[0])
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

#def threshold(image, umb):
#  umb = numpy.empty(image.shape, dtype = image.dtype).fill(umb)
#  WHITE = numpy.array(255)
#  BLACK = numpy.array(0)
#  out = image.copy()
#  w, h = image.shape
#  for i in range(w):
#    for j in range(h):
#      if image[i, j] >= umb:
#        out[i, j] = WHITE
#      else:
#        out[i, j] = BLACK
#  return out

def total_occupied_pixels(image, pt1, pt2):
  x1, y1 = pt1
  x2, y2 = pt2
  WHITE = numpy.array([255, 255, 255], dtype = image.dtype)
  RED = numpy.array([255, 0, 0], dtype = image.dtype)
  count = 0
  tmp = image[y1: y2, x1: x2, :]
  count = numpy.where(tmp != WHITE)
  count = len(count[0])/10
    #print pt1, pt2, count
  return count

def grid(image, size = 10):
  divx = WIDTH / size
  divy = HEIGHT / size
  AREA = size*size
  pixels = cv2array(image).copy()
  for i in range(divx):
    for j in range(divy):
      pt1 = i*size, j*size
      pt2 = (i + 1)*size, (j + 1)*size
      n = total_occupied_pixels(pixels, pt1, pt2)
      #print n
      if n > AREA*0.07:
        cv.Rectangle(image, pt1, pt2, cv.CV_RGB(0, 255, 0), 2)
      else: 
        cv.Rectangle(image, pt1, pt2, cv.CV_RGB(128, 128, 128), 1)
  return


def grayscale(image):
  w, h, _ = image.shape
  gray = numpy.sum(image.astype(numpy.int), axis=2) / 3
  gray = numpy.array(gray, dtype = image.dtype)
  return gray

def difference(im1, im2):
  a = im1.astype(numpy.int)
  b = im2.astype(numpy.int)
  diff = abs(a-b)
  diff = diff.astype(numpy.uint8)
  return diff

#def search_color(image, color):
#  return numpy.where(image == numpy.array(color))[0]

current_frame = 0
while True:
  if VIDEOFILE: cv.SetCaptureProperty(c, cv.CV_CAP_PROP_POS_FRAMES, current_frame )
  camera_image = cv.QueryFrame( c )
  frame1 = cv.CloneImage( camera_image )
#  cv.ConvertImage(frame1, frame1, cv.CV_CVTIMG_FLIP)
  array1 = cv2array(frame1)
  #pil1 = smooth(pil1)

  camera_image = cv.QueryFrame( c )
  frame2 = cv.CloneImage( camera_image )
#  cv.ConvertImage(frame2, frame2, cv.CV_CVTIMG_FLIP)
  array2 = cv2array(frame2)
#  #pil2 = smooth(pil2)

#  out = difference(array1, array2)
#  out = grayscale(out)
#  out = threshold(out, 2)
#  print search_color(out, (0, 0, 0))
  
#  display_image = array2cv(out)
  display_image = frame2
  grid(display_image)
  cv.ShowImage('e2', display_image)
  
  current_frame += 1

  if current_frame == NFRAMES - 1:
    break

  if cv.WaitKey(5) == 27:
    break
