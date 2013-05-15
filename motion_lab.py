import Image
import cv2.cv as cv
import numpy
from scipy import ndimage
import sys

c = cv.CreateCameraCapture(0)
cv.SetCaptureProperty( c, cv.CV_CAP_PROP_FRAME_WIDTH, 220 )
cv.SetCaptureProperty( c, cv.CV_CAP_PROP_FRAME_HEIGHT, 140 )
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

def pil_to_cv(pi, type):
  cv_im = cv.CreateImageHeader(pi.size, type, 1)
  cv.SetData(cv_im, pi.tostring())
  return cv_im

def cv_to_pil(cv_im, type):
  return Image.fromstring(type, cv.GetSize(cv_im), cv_im.tostring())

def to_binary(image, umb):
  w, h = image.size
  pix = image.load() 
  output = Image.new("L", (w, h))
  out_pix = output.load()
  for i in xrange(w):
    for j in xrange(h):
      if image.mode == "L":
        if pix[i, j] >= umb: out_pix[i, j] = 255
        else: out_pix[i, j] = 0
  output.save('output.png', 'PNG')
  return output

def to_grayscale(image):
  w, h = image.size
  pix = image.load()
  output = Image.new("L", (w, h))
  out_pix = output.load()
  for i in range(w):
    for j in range(h):
      R, G, B = pix[i, j]
      out_pix[i, j] = (R + G + B)/3
  output.save('output_grayscale.png', 'PNG')
  return output

def difference(im1, im2):
  w, h = im1.size
  output = Image.new('L', (w, h))
  pix_out = numpy.asarray(output)
  pix1 = numpy.asarray(im1)
  pix2 = numpy.asarray(im2)
  pix_out = pix2 - pix1
  return Image.fromarray(pix_out)

def smooth(im):
  im = numpy.array(im.getdata(),
                    numpy.uint8).reshape(im.size[1], im.size[0], 3)
  im_out = ndimage.gaussian_filter(im, sigma=1)
  return  Image.fromarray(im_out)  

while True:
  camera_image = cv.QueryFrame( c )
  frame1 = cv.CloneImage( camera_image )
  pil1 = cv_to_pil(frame1, "RGB")
  #pil1 = smooth(pil1)

  camera_image = cv.QueryFrame( c )
  frame2 = cv.CloneImage( camera_image )
  pil2 = cv_to_pil(frame2, "RGB")
  #pil2 = smooth(pil2)

  pil = difference(pil1, pil2)
  #pil = to_grayscale(pil)
  #pil = to_binary(pil, 20)
  
  display_image = pil_to_cv(pil, cv.IPL_DEPTH_8U)
  cv.ShowImage('e2', display_image)

  if cv.WaitKey(5) == 27:
    break
