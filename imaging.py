import Image, ImageTk
import Tkinter
from sys import argv
import numpy

OUTPUT_FILE = "output.png"

#Convertir a grayscale
def to_grayscale(image, filt, t):
  if image.mode == "RGB":
    w, h = image.size
    pix = image.load()
    output = Image.new("L", (w, h))
    out_pix = output.load()

    for k in range(t):
      for i in range(w):
        for j in range(h):
          curr = pix[i, j]
          out_pix[i, j] = max(curr)
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
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

def callback_grayscale():
  global WORKING_IMAGE
  WORKING_IMAGE = to_grayscale(WORKING_IMAGE, 1, 1)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

def callback_binary():
  global WORKING_IMAGE
  WORKING_IMAGE = to_binary( WORKING_IMAGE, 127)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

def callback_reset(image):
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = image
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = argv[1])
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

if __name__ == "__main__":
  tk = Tkinter.Tk()
  image = Image.open(argv[1])
  global WORKING_IMAGE 
  WORKING_IMAGE = image
  photo = ImageTk.PhotoImage(file = argv[1])
  w, h = image.size
  canvas = Tkinter.Canvas(tk, width = w, height = h)
  button = Tkinter.Button(canvas, text = 'Grayscale', command = lambda:callback_grayscale())
  button_window = canvas.create_window(10, 10, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'Binary', command = lambda:callback_binary())
  button_window = canvas.create_window(10, 40, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'MedianBlur', command = lambda:callback_blur())
  button_window = canvas.create_window(10, 70, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'Reset', command = lambda:callback_reset(image))
  button_window = canvas.create_window(10, 100, anchor='nw', window=button)


  canvas.create_image(0, 0, anchor = "nw", image= photo, tags = "bg")
  canvas.pack()
  tk.mainloop()
