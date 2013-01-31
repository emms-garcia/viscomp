import Image, ImageTk
import Tkinter
from sys import argv

OUTPUT_FILE = "output.png"
WORKING_IMAGE = None


def to_grayscale(image, filt, t):
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


def callback_grayscale(img):
  print "grayscale"
  WORKING_IMAGE = to_grayscale(img, 1, 1)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

def callback_binary(img):
  WORKING_IMAGE = to_binary(img, 127)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  canvas.itemconfig("bg", image = photo)
  tk.nothing()

if __name__ == "__main__":
  tk = Tkinter.Tk()


  image = Image.open(argv[1]).convert("RGB")
  WORKING_IMAGE = image
  photo = ImageTk.PhotoImage(file = argv[1])
  w, h = image.size
  canvas = Tkinter.Canvas(tk, width = w, height = h)
  button = Tkinter.Button(canvas, text = 'Grayscale', command = lambda:callback_grayscale(WORKING_IMAGE))
  button_window = canvas.create_window(10, 10, anchor='nw', window=button)
  button = Tkinter.Button(canvas, text = 'Binary', command = lambda:callback_binary(WORKING_IMAGE))
  button_window = canvas.create_window(10, 40, anchor='nw', window=button)

  canvas.create_image(0, 0, anchor = "nw", image= photo, tags = "bg")
  canvas.pack()
  tk.mainloop()
