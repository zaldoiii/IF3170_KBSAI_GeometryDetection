import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import numpy as np
import cv2
import random
import math
import sys
import clips
#import shape_detection
#import

gui = tk.Tk()

def euclidian_dist(x1,y1,x2,y2):
	return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

def makeAngle(a,b,c):
	return np.arccos((a**2+b**2-c**2)/(2*a*b))*(180/np.pi)

def detect_shape(angles, nodes, sides):
    env = clips.Environment()

    #define facts
    fact_sisi_string = """
    (deftemplate sisi
        (slot jumlah (type INTEGER)))
    """
    env.build(fact_sisi_string)
    new_fact = env.find_template('sisi').new_fact()
    new_fact['jumlah'] = len(angles)
    new_fact.assertit()


    fact_polygon_name = """
    (deftemplate polygon
        (slot nama (type SYMBOL))
        (slot tx1 (type INTEGER))
        (slot tx2 (type INTEGER))
        (slot tx3 (type INTEGER))
        (slot tx4 (type INTEGER))
        (slot sisi1 (type FLOAT))
        (slot sisi2 (type FLOAT))
        (slot sisi3 (type FLOAT))
        (slot sisi4 (type FLOAT))
        (slot sisi5 (type FLOAT))
        (slot sisi6 (type FLOAT))
        (slot sudut1 (type FLOAT))
        (slot sudut2 (type FLOAT))
        (slot sudut3 (type FLOAT))
        (slot sudut4 (type FLOAT))
        (slot sudut5 (type FLOAT))
        (slot sudut6 (type FLOAT)))
    """
    env.build(fact_polygon_name)

    #define helping functions
    calculate_error_function = """
    (deffunction acceptable-error
        (?real ?desired ?error)
        (<= (abs (- ?real ?desired)) ?error))
    """
    env.build(calculate_error_function)
    calculate_error_function = """
    (deffunction inequal
        (?arg1 ?arg2 ?error)
        (>= (abs (- ?arg1 ?arg2)) ?error))
    """
    env.build(calculate_error_function)

    #define rules
    #SEGITIGA
    if(len(angles) == 3):
        rule_sisi_string = """
        (defrule define-polygon-segitiga
            (sisi (jumlah 3))
            =>
            (assert (polygon (nama segitiga)
            			(sudut1 """+str(angles[0])+""")
            			(sudut2 """+str(angles[1])+""")
            			(sudut3 """+str(angles[2])+""")
					)
			)
		)
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-sikusiku
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (acceptable-error ?s1 90.0 1) (acceptable-error ?s2 90.0 1) (acceptable-error ?s3 90.0 1)))
            =>
            (printout t "Polygon: Segitiga Siku-Siku" crlf)
            (assert (polygon (nama segitigasiku-siku))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (acceptable-error ?s1 60.0 1.0) )
            (test (acceptable-error ?s2 60.0 1.0) )
            (test (acceptable-error ?s3 60.0 1.0) )
            =>
            (printout t "Polygon: Segitiga Sama Sisi" crlf)
            (assert (polygon (nama segitigasamasisi))))
        """
        env.build(rule_panjang_sisi_string)
        

        rule_panjang_sisi_string = """
        (defrule define-segitiga-samakaki
            (not (polygon (nama segitigasamasisi)))
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (acceptable-error ?s1 ?s2 1.0) (acceptable-error ?s1 ?s3 1.0) (acceptable-error ?s3 ?s2 1.0)))
            =>
            (printout t "Polygon: Segitiga Sama Kaki" crlf)
            (assert (polygon (nama segitigasamakaki))))
        """
        env.build(rule_panjang_sisi_string)

        rule_panjang_sisi_string = """
        (defrule define-segitiga-tumpul
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (> ?s1 92.0) (> ?s2 92.0) (> ?s3 92.0)))
            =>
            (printout t "Polygon: Segitiga Tumpul" crlf)
            (assert (polygon (nama segitigatumpul))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-lancip
            (not (polygon (nama segitigasamasisi)))
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (and (< ?s1 90.0) (< ?s2 90.0) (< ?s3 90.0)))
            =>
            (printout t "Polygon: Segitiga Lancip" crlf)
            (assert (polygon (nama segitigalancip))))
        """
        env.build(rule_panjang_sisi_string)
    


    #SEGIEMPAT
    if(len(angles) == 4):
        rule_sisi_string = """
        (defrule define-polygon-segiempat
            (sisi (jumlah 4))
            =>
            (printout t "Polygon: Segi Empat" crlf)
            (assert (polygon (nama segiempat)
						(sudut1 """+str(angles[0])+""")    
						(sudut2 """+str(angles[1])+""")
						(sudut3 """+str(angles[2])+""")
						(sudut4 """+str(angles[3])+""")
						(sisi1 """+str(sides[0])+""")
						(sisi2 """+str(sides[1])+""")
						(sisi3 """+str(sides[2])+""")
						(sisi4 """+str(sides[3])+""")
						(tx1 """+str(nodes[0][0])+""")
						(tx2 """+str(nodes[1][0])+""")
						(tx3 """+str(nodes[2][0])+""")
						(tx4 """+str(nodes[3][0])+""")
					)
            )
		)
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segiempat-beraturan
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (polygon (sisi1 ?t1))
            (polygon (sisi2 ?t2))
            (polygon (sisi3 ?t3))
            (polygon (sisi4 ?t4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 3))
            (test (acceptable-error ?t1 ?t2 3))
            (test (acceptable-error ?t2 ?t3 3))
            (test (acceptable-error ?t3 ?t4 3))
            (test (acceptable-error ?t1 ?t4 3)) 
            =>
            (printout t "Polygon: Segi Empat Beraturan" crlf)
            (assert (polygon (nama segiempatberaturan))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segiempat-layang-layang
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (or
                (test(and (acceptable-error ?s1 ?s3 3) (inequal ?s2 ?s4 3)))
                (test(and (acceptable-error ?s2 ?s4 3) (inequal ?s1 ?s3 3)))
            )
            =>
            (printout t "Polygon: Segi Empat Layang-Layang" crlf)
            (assert (polygon (nama segiempatlayanglayang))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-samakaki
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (or
                (test(and (acceptable-error ?s2 ?s3 2) (inequal ?s1 ?s2 1)))
                (test(and (acceptable-error ?s2 ?s1 2) (inequal ?s2 ?s3 1)))
            )
            =>
            (printout t "Polygon: Trapesium Sama Kaki" crlf)
            (assert (polygon (nama trapesiumsamakaki))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (and
                (test(or (acceptable-error ?s1 90.0 3) (acceptable-error ?s3 90.0 3)))
                (test(or (acceptable-error ?s2 90.0 3) (acceptable-error ?s4 90.0 3)))
            )
            =>
            (printout t "Polygon: Trapesium Rata" crlf)
            (assert (polygon (nama trapesiumrata))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata-kiri
            (polygon (tx1 ?s1))
            (polygon (tx2 ?s2))
            (polygon (tx3 ?s3))
            (polygon (tx4 ?s4))
            (polygon (nama trapesiumrata))
            (or
                (test(and (acceptable-error ?s1 ?s2 4) (< ?s2 ?s3)))
                (test(and (acceptable-error ?s2 ?s3 4) (< ?s3 ?s4)))
                (test(and (acceptable-error ?s3 ?s4 4) (< ?s4 ?s1)))
                (test(and (acceptable-error ?s4 ?s1 4) (< ?s1 ?s2)))
            )
            
            =>
            (printout t "Polygon: Trapesium Rata Kiri" crlf)
            (assert (polygon (nama trapesiumratakiri))))
        """
        env.build(rule_panjang_sisi_string)

        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata-kanan
            (polygon (tx1 ?s1))
            (polygon (tx2 ?s2))
            (polygon (tx3 ?s3))
            (polygon (tx4 ?s4))
            (polygon (nama trapesiumrata))
            (not (polygon (nama trapesiumratakiri)))
            (or
                (test(and (acceptable-error ?s1 ?s2 5) (> ?s2 ?s3)))
                (test(and (acceptable-error ?s2 ?s3 5) (> ?s3 ?s4)))
                (test(and (acceptable-error ?s3 ?s4 5) (> ?s4 ?s1)))
                (test(and (acceptable-error ?s4 ?s1 5) (> ?s1 ?s2)))
            )
            =>
            (assert (polygon (nama trapesiumratakanan))))
            (printout t "Polygon: Trapesium Rata Kanan" crlf)
        """
        env.build(rule_panjang_sisi_string)
    if(len(angles) == 5):
        #SEGILIMA
        rule_sisi_string = """
        (defrule define-polygon-segilima
            (sisi (jumlah 5))
            =>
            (printout t "Polygon: Segi Lima" crlf)
            (assert (polygon (nama segilima)
                            (sudut1 """+str(angles[0])+""")
                            (sudut2 """+str(angles[1])+""")
                            (sudut3 """+str(angles[2])+""")
                            (sudut4 """+str(angles[3])+""")
                            (sudut5 """+str(angles[4])+""")
                    )
            )
        )
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segienam-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (polygon (sudut5 ?s5))
            (test (acceptable-error ?s1 108 2.5) )
            (test (acceptable-error ?s2 108 2.5) )
            (test (acceptable-error ?s3 108 2.5) )
            (test (acceptable-error ?s4 108 2.5) )
            (test (acceptable-error ?s5 108 2.5) )
            =>
            (printout t "Polygon: Segi Lima Sama Sisi" crlf)
            (assert (polygon (nama segilimasamasisi))))
        """
        env.build(rule_panjang_sisi_string)
    

    if(len(angles) == 6):
        #SEGIENAM
        rule_sisi_string = """
        (defrule define-polygon-segienam
            (sisi (jumlah 6))
            =>
            (printout t "Polygon: Segi Enam" crlf)
            (assert (polygon (nama segienam)
                            (sudut1 """+str(angles[0])+""")
                            (sudut2 """+str(angles[1])+""")
                            (sudut3 """+str(angles[2])+""")
                            (sudut4 """+str(angles[3])+""")
                            (sudut5 """+str(angles[4])+""")
                            (sudut6 """+str(angles[5])+""")
                    )
            )
        )
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segienam-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (polygon (sudut5 ?s5))
            (polygon (sudut6 ?s6))
            (test (acceptable-error ?s1 120.0 2.5) )
            (test (acceptable-error ?s2 120.0 2.5) )
            (test (acceptable-error ?s3 120.0 2.5) )
            (test (acceptable-error ?s4 120.0 2.5) )
            (test (acceptable-error ?s5 120.0 2.5) )
            (test (acceptable-error ?s6 120.0 2.5) )
            =>
            (printout t "Polygon: Segi Enam Sama Sisi" crlf)
            (assert (polygon (nama segienamsamasisi))))
        """
        env.build(rule_panjang_sisi_string)
    

    #activate rules
	# check existing rules 
    for activation in env.activations():
        print(activation)
        rulesList.insert("end", str(activation))

    #get result
    env.run()
    for fact in  env.facts():
	    factList.delete("0", "end")
	    factList.insert("end", str(fact))
	    myshape = str(fact)
	    if "nama" in myshape: 
		    print(myshape)
		    print(myshape.split("(polygon (nama ")[1].split(")")[0])
		    detectionList.delete("0", "end")
		    detectionList.insert("end", myshape.split("(polygon (nama ")[1].split(")")[0])
    
    for activation in env.activations():
        print(activation)
        rulesList.delete("0", "end")
        rulesList.insert("end", str(activation))

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
buttonEditor.configure(text='''Show Results''')

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
buttonRule.configure(command= lambda: detect_shape(angles, nodes, sides))

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
