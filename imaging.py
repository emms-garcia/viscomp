#!/usr/bin/python
import Image
import ImageTk
import Tkinter
from sys import argv
#import numpy
import random
import math
import random
import time
from os import path
import sys

OUTPUT_FILE = "output.png"
INICIO = 0
FIN = 0
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)
#Ruido sal y pimienta, aplicando pixeles negros y blancos al azar
#Parametro
#-im Objeto de la clase PIL con la pix a aplicar el ruido
#-intensidad Porcentaje de pixeles sobre el total que seran sal y pimienta.
#-pol Rango de polarizacion que determina que tan blancos o que tan negros
#     son los puntos.
def sal_y_pimienta(im, intensidad, pol):
  w, h = im.size
  pix = im.load()
  n = w*h
  n = int(intensidad*(n/100))
  i = 0
  if im.mode == "RGB":
    while i != n:
      x, y = random.randint(0, w - 1), random.randint(0, h - 1)
      det = random.randint(0, 1)
      if det == 1:
        sal = random.randint(255-pol, 255)
        pix[x, y] = (sal, sal, sal)
      else:
        pim = random.randint(0, pol)
        pix[x, y] = (pim, pim, pim)
      i += 1

  if im.mode == "L":
    while i != n:
      x, y = random.randint(0, w - 1), random.randint(0, h - 1)
      det = random.randint(0, 1)
      if det == 1:
        sal = random.randint(255-pol, 255)
        pix[x, y] = sal
      else:
        pim = random.randint(0, pol)
        pix[x, y] = pim
      i += 1

  im.save("output.png", "png")
  return im

#Eliminacion del ruido sal y pimienta, usando una combinacion entre promedio y umbrales
#Parametros
#-im Objeto de la libreria PIL con la pix a la cual se eliminara el ruido.
#-umb Umbral que determinara en que rangos de pixeles se aplicara la eliminacion de ruido.
def des_sal_y_pimienta(im, umb):
  w, h = im.size
  pix = im.load()
  salypimienta = []
  for i in range(umb):
    salypimienta.append((i, i, i))
    salypimienta.append((i))
  for i in range(255-umb, 255):
    salypimienta.append((i, i, i))
    salypimienta.append((i))
  if im.mode == "RGB":
    for i in range(w):
      for j in range(h):
        prom = []
        if pix[i, j] in salypimienta:
          if i > 0: prom.append(list(pix[i-1, j]))
          if i < w-1: prom.append(list(pix[i+1, j]))
          if j < h-1: prom.append(list(pix[i, j+1]))
          if j > 0: prom.append(list(pix[i, j-1]))
          col_totals = [ sum(x) for x in zip(*prom) ]
          pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
    im.save(OUTPUT_FILE, "png")
  elif im.mode == "L":
    output = Image.new("L", (w, h))
    out_pix = output.load()
    for i in range(w):
      for j in range(h):
        prom = []
        if pix[i, j] in salypimienta:
          if i > 0: prom.append(pix[i-1, j])
          if i < w-1: prom.append(pix[i+1, j])
          if j < h-1: prom.append(pix[i, j+1])
          if j > 0: prom.append(pix[i, j-1])
          pix[i, j] = sum(prom)/len(prom)
    im.save(OUTPUT_FILE, "png")
  return im

#Convertir a grayscale
#Parametros
#image Objeto de la libreria PIL con la pix a convertir.
#filt Filtro a usar("prom" para promedio, "max" para mayor", "min" para menor)
def to_grayscale(image, filt):
  w, h = image.size
  pix = image.load()
  output = Image.new("RGB", (w, h))
  out_pix = output.load()
  for i in range(w):
    for j in range(h):
      curr = pix[i, j]
      if filt == "prom":
        prom = (curr[0] + curr[1] + curr[2]) / 3
        out_pix[i, j] = prom, prom, prom
      if filt == "max":
        max_ = max(curr)
        out_pix[i, j] = max_, max_, max_
      if filt == "min":
        min_ = min(curr)
        out_pix[i, j] = min_, min_, min_
  output.save(OUTPUT_FILE, 'PNG')
  return output

#Conversion a pix binarizada
#Parametros
#image Objeto de la libreria PIL con la pix a convertir
#umb Umbral de decision para convertir a 0 o 255
def to_binary(image, umb):
  w, h = image.size
  pix = image.load() 
  output = Image.new("RGB", (w, h))
  out_pix = output.load()
  for i in range(w):
    for j in range(h):
      if image.mode == "RGB":
        if max(pix[i, j]) >= umb: out_pix[i, j] = (255, 255, 255)
        else: out_pix[i, j] = (0, 0, 0)
      elif image.mode == "L":
        if pix[i, j] >= umb: out_pix[i, j] = 255
        else: out_pix[i, j] = 0
  output.save(OUTPUT_FILE, 'PNG')
  return output

#Aplicacion de blur ("borrosidad") a una pix
#Parametro
#image Objeto de la libreria PIL con la pix a la que se aplicara blur
#n Numero de veces que se le aplicara el efecto
def blur(image, n):
  w, h = image.size
  pix = image.load() 
  output = Image.new("RGB", (w, h))
  out_pix = output.load()
  for k in range(n):
    for i in range(w):
      for j in range(h):
        prom = []
        prom.append(list(pix[i, j]))
        if i > 0: prom.append(list(pix[i-1, j]))
        if i < w-1: prom.append(list(pix[i+1, j]))
        if j < h-1: prom.append(list(pix[i, j+1]))
        if j > 0: prom.append(list(pix[i, j-1]))
        col_totals = [ sum(x) for x in zip(*prom) ]
        out_pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
  output.save(OUTPUT_FILE, "png")
  return output

#Normalizacion de la pix para fijar los pixeles dentro de un rango
#entre el pixel mayor y menor.
#Parametros
#-im Objeto de la libreria PIL con la pix a normalizar
def normalize(im):
  w, h = im.size
  pix1 = im.load()
  im2 = Image.new("RGB", (w, h))
  pix2 = im2.load()
  max_ = 0
  min_ = 256
  for i in range(w):
    for j in range(h):
      if pix1[i, j][0] > max_:
        max_ = pix1[i, j][0]
      if pix1[i, j][0] < min_:
        min_ = pix1[i, j][0]
  #print max_, min_
  prop = 256.0/(max_ - min_);
  for i in range(w):
    for j in range(h):
      curr = int(math.floor((pix1[i, j][0] - min_)*prop))
      pix2[i, j] = curr, curr, curr
  im2.save(OUTPUT_FILE, "png") 
  return im2 

#Diferencia entre dos pixes, restando los pixeles de una a otra.
#Parametros
#-im1 pix original a la cual se restaran pixeles.
#-im2 pix que se restara a la original.
def contornos(im1, im2):
  pix1 = im1.load()
  pix2 = im2.load()
  w, h = im1.size
  im3 = Image.new('RGB', im1.size)
  pix3 = im3.load()
  for i in range(w):
    for j in range(h):
      pix3[i, j] = (pix1[i, j][0] - pix2[i, j][0], \
                    pix1[i, j][1] - pix2[i, j][1], \
                    pix1[i, j][2] - pix2[i, j][2])
  im3.save(OUTPUT_FILE, 'png')
  return im3

def zeros(n, m):
  matrix = []
  for i in range(n):
    curr = []
    for j in range(m):
      curr.append(0)
    matrix.append(curr)
  return matrix

def convolucion(im, g):
  w, h = im.size
  pix = im.load()
  out_im = Image.new("RGB", (w, h))
  out = out_im.load()
  for i in xrange(w):
    for j in xrange(h):
      suma = 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
      out[i, j] = suma, suma, suma
  out_im.save("output.png", "png")
  return out_im


def bfs(im, origen, color):
  pix = im.load()
  w, h = im.size
  q = []
  coords = []
  q.append(origen)
  original = pix[origen]
  n = 0
  while len(q) > 0:
    (x, y) = q.pop(0)
    actual = pix[x, y]
    if actual == original or actual == color:
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          i, j = (x + dx, y + dy)
          if i >= 0 and i < w and j >= 0 and j < h:
            contenido = pix[i, j]
            if contenido == original:
              pix[i, j] = color
              coords.append((i, j))
              n += 1
              q.append((i, j))
  im.save(OUTPUT_FILE, 'png')
  return n, coords

def check_erosion(pix, i, j):
  for n in range(i-1, i+2):
    for m in range(j-1, j+2):
      if pix[n, m] == (BACKGROUND):
        return True
  return False

def dilation(im):
  w, h = im.size
  pix = im.load()
  struct = [ [1, 1, 1],
             [1, 1, 1],
             [1, 1, 1] ]
  im2 = Image.new('RGB', (w, h))
  pix2 = im2.load()
  for i in range(w):
    for j in range(h):
      t = False
      if pix[i, j] == FOREGROUND:
        for n in range(i-1, i+2):
          for m in range(j-1, j+2):
            try:
              if pix[n, m] == (BACKGROUND):
                t = True
            except:
              pass
      if t:
        pix2[i, j] = FOREGROUND
      else:
        pix2[i, j] = pix[i, j]
        
  im2.save(OUTPUT_FILE, 'png')
  return im2


def classify_forms(im):
  w, h = im.size
  total = w * h
  porcentajes = []
  centroids = []
  cont = 0
  pix = im.load()
  basura = []
  for i in range(w):
    for j in range(h):
      if pix[i, j] == (0, 0, 0):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        n, coords = bfs(im, (i, j), (r, g, b))
        sys.exit()
        p = float(n)/float(total) * 100.0
        print "Pintando figura %s"%cont
        sums = [sum(x) for x in zip(*coords)]
        centroids.append((sums[0] / len(coords), sums[1] / len(coords)))
        porcentajes.append([p, (r, g, b)])
        cont += 1
  fondo_id = porcentajes.index(max(porcentajes))
  max_color = porcentajes[fondo_id][1]
  print "Pintando fondo"
  for i in range(w):
    for j in range(h):
      if pix[i, j] == max_color:
        pix[i, j] = (150, 150, 150)
  print "Pintando centros de masa"
  for i in range(len(centroids)):
    print centroids[i]
    if i == fondo_id:
      pix[centroids[i]] = (255, 0, 0)
    else:
      pix[centroids[i]] = (0, 0, 0)
  im.save(OUTPUT_FILE, 'png')
  cont = 0
  for p in porcentajes:
    print "Porcentaje de la figura ID %s: %.2f"%(cont, p[0])
    cont += 1
  return im, centroids

def is_left(p1, p2, p3):
 return ((p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0])) > 0 

def jarvis(S):
  hull = [min(S)]
  i = 0
  while True:
    end = S[0]
    for j in range(len(S) - 1):
      if end == hull[i] or is_left(end, hull[i], S[j]):
        end = S[j]
    i += 1
    hull.append(end)
    if end == hull[0]:
      break
  return hull
        
def convex_hull(im):
  w, h = im.size
  pix = im.load()
  hulls = []
  for i in range(w):
    for j in range(h):
      if pix[i, j] == (255, 255, 255):
        n, coords = bfs(im, (i, j), (255, 0, 0))
        hulls.append(jarvis(coords))
  for hull in hulls:
    for points in hull:
      pix[points] = (0, 255, 0)
  im.save(OUTPUT_FILE, 'png')
  return im, hulls

def negativo(im):
  w, h = im.size
  pix = im.load()
  for i in range(w):
    for j in range(h):
      act = pix[i, j]
      if act == (255, 255, 255):
        pix[i, j] = 0, 0, 0
      else:
        pix[i, j] = 255, 255, 255
  im.save(OUTPUT_FILE, 'png')
  return im

def sort_dictionary(d):
  return sorted(d.items(), key=lambda x: x[1], reverse = True)

def random_color():
  r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
  return (r, g, b)

def hough_transform(im, umb):
  maskx = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
  masky = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
  #maskx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
  #masky = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
  gradx = convolucion(im, maskx)
  grady = convolucion(im, masky)
  gx = gradx.load()
  gy = grady.load()
  matrix = []
  combination = {}
  angles = []
  w, h = im.size
  for i in range(w):
    tmp = list()
    for j in range(h):
      r, g, b = gx[i, j]
      x = float((r + g + b) / 3)
      r, g, b = gy[i, j]
      y = float((r + g + b) / 3)
      if x > 0:
        theta = math.atan(y/x)
      else:
        theta = None
      if theta is not None:
        theta = int(math.degrees(theta)/10)*10
        rho = int((i) * math.cos(theta) + (j) * math.sin(theta)/10)*10
        if not theta in angles:  angles.append(theta)
        if i > 0 and i < w-1 and j > 0 and j < h - 1:
          if (rho, theta) in combination:
            combination[(rho, theta)] += 1
          else:
            combination[(rho, theta)] = 1
        tmp.append((rho, theta))
      else:
        tmp.append((None, None))
    matrix.append(tmp)
  print angles
  pix = im.load()
  colors = {}
  lines = {}
  line_image = Image.new('RGB', (w, h))
  pix_line = line_image.load()
  for i in range(w):
    for j in range(h):
      if i > 0 and j > 0 and i < w and j < h:
        rho, theta = matrix[i][j]
        if (rho, theta) in combination:
          if (theta) not in colors: colors[(theta)] = random_color()
          if theta not in lines: lines[theta] = 1
          else: lines[theta] += 1
          pix[i, j] = colors[(theta)]
          pix_line[i, j] = (255, 255, 255)
  print len(colors), len(angles)
  for line in lines:
    print "Cantidad de pixeles con angulo %s: %s, Color: %s"%(line, lines[line], colors[line])
  colors = []
  for i in range(w):
    for j in range(h):
      if pix_line[i, j] == (255, 255, 255):
        color = random_color()
        while color in colors:
          color = random_color()
        n, coords = bfs(line_image, (i, j), color)
        colors.append(color)
  for i in range(len(colors)):
    print "Color de la linea %s: %s"%(i+1, colors[i])
  im.save('output.png', 'png')
  line_image.save('output_lines.png')
  return im

def callback_convex_hull():
  global WORKING_IMAGE
  INICIO = time.time()
  WORKING_IMAGE, hulls = convex_hull(WORKING_IMAGE)
  FIN = time.time() - INICIO
  print FIN
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  #canvas.itemconfig(background, image = photo)
  for i in range(len(hulls)):
    for j in range(len(hulls[i]) - 1):
      #print (hulls[i][j]), (hulls[i][j+1])
      canvas.create_line((hulls[i][j]), (hulls[i][j+1]), fill="blue", width = 3.0)

def callback_classify():
  global WORKING_IMAGE
  WORKING_IMAGE, centroids = classify_forms(WORKING_IMAGE)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
  canvas.itemconfig(background, image = photo)
  i = 0
  for center in centroids:
    dx, dy = center[0], center[1]
    Tkinter.Label(canvas, text = '%d'%i).place(x = dx, y = dy)
    i += 1

def callback_blur():
  print "flip"
  global WORKING_IMAGE
  WORKING_IMAGE = blur(WORKING_IMAGE, 10)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_grayscale():
  global WORKING_IMAGE
  WORKING_IMAGE = to_grayscale(WORKING_IMAGE, "prom")
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_binary():
  global WORKING_IMAGE
  WORKING_IMAGE = to_binary( WORKING_IMAGE, 127)
  w, h = WORKING_IMAGE.size
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_sal():
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = sal_y_pimienta(WORKING_IMAGE, 0.5, 30)
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_des_sal():
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = des_sal_y_pimienta(WORKING_IMAGE, 30)
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_negative():
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = negativo(WORKING_IMAGE)
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = OUTPUT_FILE)

def callback_reset():
  w, h = image.size
  global  WORKING_IMAGE
  WORKING_IMAGE = image
  canvas.config(width = w, height = h)
  photo = ImageTk.PhotoImage(file = argv[1])

def check(im):
  w, h = im.size
  pix = im.load()
  for i in range(w):
    for j in range(h):
      if pix[i, j] == (255, 255, 255) or pix[i, j] == (0, 0, 0):
        pass
      else:
        return False
  return True

if __name__ == "__main__":
  global WORKING_IMAGE 
  assert(path.isfile(argv[1]))
  image = Image.open(argv[1]).convert('RGB')
  WORKING_IMAGE = image
  image = to_grayscale(image, 'prom')
  to_binary(image, 70)
  #hough_transform(image, 1.0)
  """
  root = Tkinter.Tk()
  root.title("Vision Computacional")
  photo = ImageTk.PhotoImage(file = argv[1])
  w, h = image.size

  canvas = Tkinter.Canvas(root, width = w, height = h)
  background = canvas.create_image((w/2,h/2), image = photo)

  button_content = { 'Grayscale' : lambda:callback_grayscale, 'Binary' : lambda:callback_binary(),
                    'MedianBlur' : lambda:callback_blur(), 'SalyPimienta' : lambda:callback_sal(),
                    'DeshacerSyP': lambda:callback_des_sal(), 'Reset' : lambda:callback_reset(),
                    'Clasificar' : lambda:callback_classify(), 'ConvexHull' : lambda:callback_convex_hull(),
                    'Negativo' : lambda:callback_negative()
                    }
  second_canvas = Tkinter.Canvas(root, width = w, height = h+50)
  i = 1
  for item in button_content:
    button = Tkinter.Button(second_canvas, text = item, command = button_content[item], width = 30)
    button_window = second_canvas.create_window(10, 30*i, anchor='nw', window=button)
    i += 1

  canvas.pack(side = "left")
  second_canvas.pack(side = "right")
  root.mainloop()"""
