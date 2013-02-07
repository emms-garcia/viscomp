#!/usr/bin/python
import Image, ImageTk
import Tkinter
from sys import argv
import numpy
import random
import math

OUTPUT_FILE = "output.png"

#Filtro sal y pimienta, aplicando pixeles negros y blancos al azar
#Parametro
#image Imagen a aplicar el filtro
def sal_y_pimienta(im, porcentaje):
	w, h = im.size
	pix = im.load()
	n = w*h
	n = int(porcentaje*(n/100))
	i = 0
	if im.mode == "RGB":
		while i != n:
			x, y = random.randint(0, w - 1), random.randint(0, h - 1)
			det = random.randint(0, 1)
			if det == 1:
				pix[x, y] = (255, 255, 255)
			else:
				pix[x, y] = (0, 0, 0)
			i += 1

	if im.mode == "L":
		while i != n:
			x, y = random.randint(0, w - 1), random.randint(0, h - 1)
			det = random.randint(0, 1)
			if det == 1:
				pix[x, y] = 255
			else:
				pix[x, y] = 0
			i += 1

	im.save("output.png", "png")
	return im

#Deshacer el
def des_sal_y_pimienta(im):
	w, h = im.size
	pix = im.load()
	salypimienta = [(255, 255, 255), 255, (0, 0, 0), 0]
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
#image Objeto de la libreria PIL con la imagen a convertir.
#filt Filtro a usar("prom" para promedio, "max" para mayor", "min" para menor)
def to_grayscale(image, filt):
	if image.mode == "RGB":
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
					out_pix[i, j] = max(curr), max(curr), max(curr)
				if filt == "min":
					out_pix[i, j] = min(curr), min(curr), min(curr)
		output.save(OUTPUT_FILE, 'PNG')
		return output
	else:
		print "Imagen en blanco y negro"
		return image

#Conversion a imagen binarizada
#Parametros
#image Objeto de la libreria PIL con la imagen a convertir
#umb Umbral de decision para convertir a 0 o 255
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

#Aplicacion de blur ("borrosidad") a una imagen
#Parametro
#image Objeto de la libreria PIL con la imagen a la que se aplicara blur
#n Numero de veces que se le aplicara el efecto
def blur(image, n):
	w, h = image.size
	pix = image.load() 

	if image.mode == "RGB":
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
	elif image.mode == "L":
		output = Image.new("L", (w, h))
		out_pix = output.load()
		for k in range(n):
			for i in range(w):
				for j in range(h):
					 prom = []
			 		 prom.append(pix[i, j])
					 if i > 0: prom.append(pix[i-1, j])
					 if i < w-1: prom.append(pix[i+1, j])
					 if j < h-1: prom.append(pix[i, j+1])
		 			 if j > 0: prom.append(pix[i, j-1])
		 		 	 out_pix[i, j] = sum(prom)/len(prom)
		output.save(OUTPUT_FILE, "png")
	return output

#Normalizacion de la imagen.
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
	return im2 

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

def callback_blur():
	print "flip"
	global WORKING_IMAGE
	WORKING_IMAGE = blur(WORKING_IMAGE, 1)
	w, h = WORKING_IMAGE.size
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_grayscale():
	global WORKING_IMAGE
	WORKING_IMAGE = to_grayscale(WORKING_IMAGE, "prom")
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

def callback_sal(image):
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = sal_y_pimienta(WORKING_IMAGE, 0.5)
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_des_sal(image):
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = des_sal_y_pimienta(WORKING_IMAGE)
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_reset(image):
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = image
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = argv[1])
	label.config(image = photo)
	label.image = photo


if __name__ == "__main__":

	"""im_name = "../test.jpg"
	im1 = Image.open(im_name)
	im1 = to_grayscale(im1, "min")
	im2 = blur(im1, 1)
	im3 = contornos(im1, im2)
	normalize(im3)"""


	root = Tkinter.Tk()
	root.title("Vision Computacional")
	image = Image.open(argv[1])
	global WORKING_IMAGE 
	WORKING_IMAGE = image
	photo = ImageTk.PhotoImage(file = argv[1])
	w, h = image.size

	canvas = Tkinter.Canvas(root, width = w, height = h)
	label = Tkinter.Label(canvas, image = photo)
	label.image = photo
	label.pack()

	second_canvas = Tkinter.Canvas(root, width = w, height = h+50)
	button = Tkinter.Button(second_canvas, text = 'Grayscale', command = lambda:callback_grayscale(), width = 30)
	button_window = second_canvas.create_window(10, 10, anchor='nw', window=button)
	button = Tkinter.Button(second_canvas, text = 'Binary', command = lambda:callback_binary(), width = 30)
	button_window = second_canvas.create_window(10, 40, anchor='nw', window=button)
	button = Tkinter.Button(second_canvas, text = 'MedianBlur', command = lambda:callback_blur(), width = 30)
	button_window = second_canvas.create_window(10, 70, anchor='nw', window=button)
	button = Tkinter.Button(second_canvas, text = 'SalyPimienta', command = lambda:callback_sal(image), width = 30)
	button_window = second_canvas.create_window(10, 100, anchor='nw', window=button)
	button = Tkinter.Button(second_canvas, text = 'DeshacerSyP', command = lambda:callback_des_sal(image), width = 30)
	button_window = second_canvas.create_window(10, 130, anchor='nw', window=button)
	button = Tkinter.Button(second_canvas, text = 'Reset', command = lambda:callback_reset(image), width = 30)
	button_window = second_canvas.create_window(10, 160, anchor='nw', window=button)


	canvas.pack(side = "top")
	second_canvas.pack(side = "bottom")
	root.mainloop()
