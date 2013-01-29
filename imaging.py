import Image
import Tkinter
from sys import argv

def to_grayscale(image, filt, t):
  w, h = image.size
  pix = image.load()

  output = Image.new("RGB", (w, h))
  out_pix = output.load()

  for k in range(t):
    for i in range(w):
      for j in range(h):
        curr = pix[i, j]
        out_pix[i, j] = (max(curr), max(curr), max(curr))
	
    
  output.save('output.png', 'png')

  return output

def callback():
  print "bitch please"
  to_grayscale(image, 1, 1)
  photo = Tkinter.PhotoImage(file = "output.png").convert('rgb')
  canvas.create_image(0, 0,anchor = "nw", image= photo)
  canvas.pack()
  

if __name__ == "__main__":
  tk = Tkinter.Tk()

  photo = Tkinter.PhotoImage(file = argv[1].replace("png", "gif"))
  image = Image.open(argv[1])
  w, h = image.size
  canvas = Tkinter.Canvas(tk, width = w, height = h)
  button = Tkinter.Button(canvas, text = 'Bitch please', command = callback)
  button_window = canvas.create_window(10, 10, anchor='nw', window=button)
  canvas.create_image(0, 0,anchor = "nw", image= photo)
  canvas.pack()


tk.mainloop()
