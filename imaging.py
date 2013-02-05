import Image, ImageTk
import Tkinter
from sys import argv
import numpy
import math

OUTPUT_FILE = "output.png"

#Convertir a grayscale
def to_grayscale(image):
  if image.mode == "RGB":
    w, h = image.size
    pix = image.load()
    output = Image.new("RGB", (w, h))
    out_pix = output.load()
    for i in range(w):
      for j in range(h):
        curr = pix[i, j]
        out_pix[i, j] = max(curr), max(curr), max(curr)
    output.save(OUTPUT_FILE, 'PNG')
    return output
  else:
    print "Imagen en blanco y negro"
    return image


def to_binary(image, umb):
   w, h = image.size
   pix = image.load() 
   output = Image.new("L", (w, h))
   out_pix = output.load()
   for i in range(w):
     for j in range(h):
        if image.mode == "RGB":
	  if max(pix[i, j]) >= umb: out_pix[i, j] = 255 
          else: out_pix[i, j] = 0
        elif image.mode == "L":
	  if pix[i, j] >= umb: out_pix[i, j] = 255
	  else: out_pix[i, j] = 0
   output.save(OUTPUT_FILE, 'PNG')
   return output

def blur(image):
  w, h = image.size
  pix = image.load() 

  if image.mode == "RGB":
    output = Image.new("RGB", (w, h))
    out_pix = output.load()
    for i in range(w):
      for j in range(h):
         prom = []
  	 prom.append(list(pix[i, j]))
	  #print i, j
         if i > 0:
	   prom.append(list(pix[i-1, j]))
         if i < w-1:
	   prom.append(list(pix[i+1, j]))
         if j < h-1:
	   prom.append(list(pix[i, j+1]))
	 if j > 0:
	   prom.append(list(pix[i, j-1]))
         col_totals = [ sum(x) for x in zip(*prom) ]
     	 out_pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
    output.save(OUTPUT_FILE, "png")
  elif image.mode == "L":
    output = Image.new("L", (w, h))
    out_pix = output.load()
    for i in range(w):
      for j in range(h):
         prom = []
  	 prom.append(pix[i, j])
	  #print i, j
         if i > 0:
	   prom.append(pix[i-1, j])
         if i < w-1:
	   prom.append(pix[i+1, j])
         if j < h-1:
	   prom.append(pix[i, j+1])
	 if j > 0:
	   prom.append(pix[i, j-1])
     	 out_pix[i, j] = sum(prom)/len(prom)
    output.save(OUTPUT_FILE, "png")
  return output

def flip_90(image):
   w, h = image.size
   pix = image.load()
   output = Image.new("RGB", (h, w))
   out_pix = output.load()
   for i in range(h):
     for j in range(w):
       out_pix[i, j] = pix[j, i]
   output.save(OUTPUT_FILE, 'PNG')
   return output

def callback_blur():
  print "flip"
  global WORKING_IMAGE
  WORKING_IMAGE = blur(WORKING_IMAGE)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  label.config(image = photo)
  label.image = photo

def callback_grayscale():
  global WORKING_IMAGE
  WORKING_IMAGE = to_grayscale(WORKING_IMAGE, 1, 1)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  label.config(image = photo)
  label.image = photo

def callback_binary():
  global WORKING_IMAGE
  WORKING_IMAGE = to_binary( WORKING_IMAGE, 127)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  label.config(image = photo)
  label.image = photo

def callback_reset(image):
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = image
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = argv[1])
  label.config(image = photo)
  label.image = photo

def normalize(im3):
  w, h = im3.size
  pix1 = im3.load()
  im2 = Image.new("L", (w, h))
  pix2 = im2.load()
  max_ = 0
  min_ = 256
  for i in range(w):
    for j in range(h):
      if pix1[i, j] > max_:
	max_ = pix1[i, j]
      if pix1[i, j] < min:
	min_ = pix1[i, j]

  prop = 256.0/(max_ - min_);
  for i in range(w):
    for j in range(h):
      pix2[i, j] = int(math.floor((pix1[i, j] - min_)*prop))
  im2.save("normal.png", "png")  

def contornos(im1, im2):
  pix1 = im1.load()
  pix2 = im2.load()
  w, h = im1.size
  im3 = Image.new('L', im1.size)
  pix3 = im3.load()
  for i in range(w):
    for j in range(h):
      for k in range(len(pix2[i, j])):
        pix3[i, j] = (pix1[i, j][k] - pix2[i, j][k])
  im3.save('output.png', 'png')
  return im3

def zeros(n, m):
  matrix = []
  for i in range(n):
    curr = []
    for j in range(m):
      curr.append(0)
    matrix.append(curr)
  return matrix

def convolucion(im, h):
  w, h = im.size
  pix = im.load()

  im2 = Image.new('RGB', (w, h))
  pix2 = im2.load()


if __name__ == "__main__":
  im_name = "../test.jpg"
  im1 = Image.open(im_name)
  im1 = to_grayscale(im1)
  im2 = blur(im1)
  im3 = contornos(im1, im2)
  normalize(im3)


"""
  root = Tkinter.Tk()
  image = Image.open(argv[1])
  global WORKING_IMAGE 
  WORKING_IMAGE = image
  photo = ImageTk.PhotoImage(file = argv[1])
  w, h = image.size

  canvas = Tkinter.Canvas(root, width = w, height = h)
  label = Tkinter.Label(canvas, image = photo)
  label.image = photo
  label.pack()

  button = Tkinter.Button(canvas, text = 'Grayscale', command = lambda:callback_grayscale())
  button_window = canvas.create_window(10, 10, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'Binary', command = lambda:callback_binary())
  button_window = canvas.create_window(10, 40, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'MedianBlur', command = lambda:callback_blur())
  button_window = canvas.create_window(10, 70, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'Reset', command = lambda:callback_reset(image))
  button_window = canvas.create_window(10, 100, anchor='nw', window=button)


  canvas.pack()
  root.mainloop()"""
