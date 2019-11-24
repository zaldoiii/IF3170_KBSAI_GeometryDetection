import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import numpy as np
import cv2
import random
import math
import sys
#import shape_detection
#import

gui = tk.Tk()

def euclidian_dist(x1,y1,x2,y2):
	return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

def makeAngle(a,b,c):
	return np.arccos((a**2+b**2-c**2)/(2*a*b))*(180/np.pi)

def detectShape():
	global angles
	global nodes
	global sides
	
	img = cv2.imread(namaFile, 1)
	white = cv2.imread("images/white.png", 1)

	# Displaying to see how it looks
	# cv2.imshow("Original",img)

	# Converting the image to Gray Scale
	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

	# Removing Gaussian Noise
	blur = cv2.GaussianBlur(gray, (3,3),0)

	# Applying inverse binary due to white background and adapting thresholding for better results
	thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)

	# Checking to see how it looks
	# cv2.imshow("Binary",blur)

	# Finding contours with simple retrieval (no hierarchy) and simple/compressed end points
	contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# Checking to see how many contours were found
	# An empty list to store filtered contours
	# Looping over all found contours
	for i,c in enumerate(contours):
		# If it has significant area, add to list
		epsilon = 0.01 * cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, epsilon, closed=True)
		print(approx)
	cv2.drawContours(white, [approx], -1, (0, 255, 255), 1)

	# Check line that has been recognize
	# print(approx)

	# Length of array side
	side = len(approx)

	# Initiate container to store node ang angles information
	nodes = []
	angles = []
	sides = []

	# Create angle
	for i in range(side):
		nodes.append([approx[i][0][0],approx[i][0][1]])
		a = euclidian_dist(approx[i%side][0][0],approx[i%side][0][1],approx[(i+1)%side][0][0],approx[(i+1)%side][0][1])
		b = euclidian_dist(approx[(i+2)%side][0][0],approx[(i+2)%side][0][1],approx[(i+1)%side][0][0],approx[(i+1)%side][0][1])
		c = euclidian_dist(approx[(i+2)%side][0][0],approx[(i+2)%side][0][1],approx[(i)%side][0][0],approx[(i)%side][0][1])
		angles.append(makeAngle(a,b,c))
		sides.append(a)
	
	detectionList.insert("end", angles)
	detectionList.insert("end", nodes)
	detectionList.insert("end", sides)

def bukaFoto():
	global namaFile
	global photo
	namaFile = filedialog.askopenfilename(title="Open File")
	photo = tk.PhotoImage(file=namaFile)
	sourceImage.configure(image=photo)
	

# --- TAMPILAN DASAR --- #
gui.geometry("1000x750+0+0")
gui.minsize(1000, 750)
gui.maxsize(1000, 750)
gui.resizable(0, 0)
gui.title("Draft GUI Tubes 2")
gui.configure(background="#d9d9d9")
gui.configure(highlightbackground="#d9d9d9")
gui.configure(highlightcolor="black")

# --- TOMBOL 1 --- #
buttonImage = tk.Button(master=gui)
buttonImage.place(relx=0.81, rely=0.027, height=20, width=150)
buttonImage.configure(activebackground="#ececec")
buttonImage.configure(activeforeground="#000000")
buttonImage.configure(background="#d9d9d9")
buttonImage.configure(disabledforeground="#a3a3a3")
buttonImage.configure(foreground="#000000")
buttonImage.configure(highlightbackground="#d9d9d9")
buttonImage.configure(highlightcolor="black")
buttonImage.configure(pady="0")
buttonImage.configure(text='''Open Image''')
buttonImage.configure(command=bukaFoto)

# --- TOMBOL 2 --- #
buttonEditor = tk.Button(master=gui)
buttonEditor.place(relx=0.81, rely=0.067, height=20, width=150)
buttonEditor.configure(activebackground="#ececec")
buttonEditor.configure(activeforeground="#000000")
buttonEditor.configure(background="#d9d9d9")
buttonEditor.configure(disabledforeground="#a3a3a3")
buttonEditor.configure(foreground="#000000")
buttonEditor.configure(highlightbackground="#d9d9d9")
buttonEditor.configure(highlightcolor="black")
buttonEditor.configure(pady="0")
buttonEditor.configure(text='''Open Rule Editor''')

# --- TOMBOL 3 --- #
buttonFacts = tk.Button(master=gui)
buttonFacts.place(relx=0.81, rely=0.107, height=20, width=150)
buttonFacts.configure(activebackground="#ececec")
buttonFacts.configure(activeforeground="#000000")
buttonFacts.configure(background="#d9d9d9")
buttonFacts.configure(disabledforeground="#a3a3a3")
buttonFacts.configure(foreground="#000000")
buttonFacts.configure(highlightbackground="#d9d9d9")
buttonFacts.configure(highlightcolor="black")
buttonFacts.configure(pady="0")
buttonFacts.configure(text='''Show Facts''')
buttonFacts.configure(command=detectShape)

# --- TOMBOL 4 --- #
buttonRule = tk.Button(master=gui)
buttonRule.place(relx=0.81, rely=0.147, height=20, width=150)
buttonRule.configure(activebackground="#ececec")
buttonRule.configure(activeforeground="#000000")
buttonRule.configure(background="#d9d9d9")
buttonRule.configure(disabledforeground="#a3a3a3")
buttonRule.configure(foreground="#000000")
buttonRule.configure(highlightbackground="#d9d9d9")
buttonRule.configure(highlightcolor="black")
buttonRule.configure(pady="0")
buttonRule.configure(text='''Show Rule''')

labelQuestion = tk.Label(master=gui)
labelQuestion.place(relx=0.81, rely=0.207, height=40, width=150)
labelQuestion.configure(activebackground="#f9f9f9")
labelQuestion.configure(activeforeground="black")
labelQuestion.configure(background="#d9d9d9")
labelQuestion.configure(disabledforeground="#a3a3a3")
labelQuestion.configure(foreground="#000000")
labelQuestion.configure(highlightbackground="#d9d9d9")
labelQuestion.configure(highlightcolor="black")
labelQuestion.configure(text='''What shape do you want?''')

shapeList = ttk.Treeview(master=gui)
shapeList.place(relx=0.81, rely=0.247, relheight=0.28, width=150)
shapeList.insert('', '0', 'A', text = 'Segitiga')
shapeList.insert('A', '0', 'A1', text = 'Segitiga lancip')
shapeList.insert('A', '1', 'A2', text = 'Segitiga tumpul')
shapeList.insert('A', '2', 'A3', text = 'Segitiga siku-siku')
shapeList.insert('A', '3', 'A4', text = 'Segitiga sama kaki')
shapeList.insert('A4', '0', 'A41', text = 'Segitiga sama kaki siku-siku')
shapeList.insert('A4', '1', 'A42', text = 'Segitiga sama kaki tumpul')
shapeList.insert('A4', '2', 'A43', text = 'Segitiga sama kaki lancip')
shapeList.insert('A', '4', 'A5', text = 'Segitiga sama sisi')
shapeList.insert('', '1', 'B', text = 'Segiempat')
shapeList.insert('B', '0', 'B1', text = 'Jajaran genjang')
shapeList.insert('B1', '0', 'B11', text = 'Segiempat beraturan')
shapeList.insert('B1', '1', 'B12', text = 'Layang-layang')
shapeList.insert('B', '1', 'B2', text = 'Trapesium')
shapeList.insert('B2', '0', 'B21', text = 'Trapesium sama kaki')
shapeList.insert('B2', '1', 'B22', text = 'Trapesium rata kanan')
shapeList.insert('B2', '2', 'B23', text = 'Trapesium rata kiri')
shapeList.insert('', '2', 'C', text = 'Segi lima')
shapeList.insert('C', '0', 'C1', text = 'Segi lima sama sisi')
shapeList.insert('', '3', 'D', text = 'Segi enam')
shapeList.insert('D', '0', 'D1', text = 'Segi lima sama sisi')

detectionList = tk.Listbox(master=gui)
detectionList.place(relx=0.02, rely=0.587, relheight=0.333, relwidth=0.25)
detectionList.configure(background="white")
detectionList.configure(disabledforeground="#a3a3a3")
detectionList.configure(font="TkFixedFont")
detectionList.configure(foreground="#000000")
detectionList.configure(highlightbackground="#d9d9d9")
detectionList.configure(highlightcolor="black")
detectionList.configure(selectbackground="#c4c4c4")
detectionList.configure(selectforeground="black")

detectionLabel = tk.Label(master=gui)
detectionLabel.place(relx=0.069, rely=0.561, height=20, width=150)
detectionLabel.configure(activebackground="#f9f9f9")
detectionLabel.configure(activeforeground="black")
detectionLabel.configure(background="#d9d9d9")
detectionLabel.configure(disabledforeground="#a3a3a3")
detectionLabel.configure(foreground="#000000")
detectionLabel.configure(highlightbackground="#d9d9d9")
detectionLabel.configure(highlightcolor="black")
detectionLabel.configure(text='''Detection Results''')

factList = tk.Listbox(master=gui)
factList.place(relx=0.365, rely=0.587, relheight=0.333, relwidth=0.25)
factList.configure(background="white")
factList.configure(disabledforeground="#a3a3a3")
factList.configure(font="TkFixedFont")
factList.configure(foreground="#000000")
factList.configure(highlightbackground="#d9d9d9")
factList.configure(highlightcolor="black")
factList.configure(selectbackground="#c4c4c4")
factList.configure(selectforeground="black")

factLabel = tk.Label(gui)
factLabel.place(relx=0.42, rely=0.56, height=20, width=150)
factLabel.configure(activebackground="#f9f9f9")
factLabel.configure(activeforeground="black")
factLabel.configure(background="#d9d9d9")
factLabel.configure(disabledforeground="#a3a3a3")
factLabel.configure(foreground="#000000")
factLabel.configure(highlightbackground="#d9d9d9")
factLabel.configure(highlightcolor="black")
factLabel.configure(text='''Matched Facts''')

rulesList = tk.Listbox(master=gui)
rulesList.place(relx=0.71, rely=0.587, relheight=0.333, relwidth=0.25)
rulesList.configure(background="white")
rulesList.configure(disabledforeground="#a3a3a3")
rulesList.configure(font="TkFixedFont")
rulesList.configure(foreground="#000000")
rulesList.configure(highlightbackground="#d9d9d9")
rulesList.configure(highlightcolor="black")
rulesList.configure(selectbackground="#c4c4c4")
rulesList.configure(selectforeground="black")

rulesLabel = tk.Label(master=gui)
rulesLabel.place(relx=0.76, rely=0.56, height=20, width=150)
rulesLabel.configure(activebackground="#f9f9f9")
rulesLabel.configure(activeforeground="black")
rulesLabel.configure(background="#d9d9d9")
rulesLabel.configure(disabledforeground="#a3a3a3")
rulesLabel.configure(foreground="#000000")
rulesLabel.configure(highlightbackground="#d9d9d9")
rulesLabel.configure(highlightcolor="black")
rulesLabel.configure(text='''Hit Rules''')

sourceImage = tk.Label(master=gui)
sourceImage.place(relx=0.02, rely=0.027, height=375, width=375)
sourceImage.configure(activebackground="#f9f9f9")
sourceImage.configure(activeforeground="black")
sourceImage.configure(background="#FFFFFF")
sourceImage.configure(disabledforeground="#a3a3a3")
sourceImage.configure(foreground="#000000")
sourceImage.configure(highlightbackground="#d9d9d9")
sourceImage.configure(highlightcolor="black")
sourceImage.configure(highlightthickness="1")
sourceImage.configure(relief="ridge")

detectionImage = tk.Label(master=gui)
detectionImage.place(relx=0.415, rely=0.027, height=375, width=375)
detectionImage.configure(activebackground="#f9f9f9")
detectionImage.configure(activeforeground="black")
detectionImage.configure(background="#FFFFFF")
detectionImage.configure(disabledforeground="#a3a3a3")
detectionImage.configure(foreground="#000000")
detectionImage.configure(highlightbackground="#d9d9d9")
detectionImage.configure(highlightcolor="black")
detectionImage.configure(highlightthickness="1")
detectionImage.configure(relief="ridge")

gui.mainloop()
