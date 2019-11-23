# Tugas Besar Intelligensia Buatan 2
# Shape Detection

# Ardystrio Fakhri Haroen / 13517062 
# Marsa Thoriq Ahmada / 13517071
# Anzaldi Soelaiman Oemar / 13517098 
# Fajar Muslim / 13517149


# Import the Libraries
import numpy as np
import cv2
import random
import math
import sys
import rules

# Calculate euclidian distance
# Input : point1 (x1, y1), point2 (x2,y2)
# Output : euclidian distance
def euclidian_dist(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

# Calculate angle using cos rule
# Input : a, b, c (real)
# Output : angle
def makeAngle(a,b,c):
    return np.arccos((a**2+b**2-c**2)/(2*a*b))*(180/np.pi)

try:
    filename = sys.argv[1]
except:
    filename = 'segitigaSembarang.png'

# Reading  image
img = cv2.imread('images/'+filename,1)
white = cv2.imread("white.png",1)

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

cv2.drawContours(white, [approx], -1, (0, 255, 255), 1)

# Check line that has been recognize
# print(approx)

# Length of array side
side = len(approx)

# Initiate container to store node ang angles information
nodes = []
angles = []

# Create angle
for i in range(side):
    nodes.append([approx[i][0][0],approx[i][0][1]])
    a = euclidian_dist(approx[i%side][0][0],approx[i%side][0][1],approx[(i+1)%side][0][0],approx[(i+1)%side][0][1])
    b = euclidian_dist(approx[(i+2)%side][0][0],approx[(i+2)%side][0][1],approx[(i+1)%side][0][0],approx[(i+1)%side][0][1])
    c = euclidian_dist(approx[(i+2)%side][0][0],approx[(i+2)%side][0][1],approx[(i)%side][0][0],approx[(i)%side][0][1])
    angles.append(makeAngle(a,b,c))

# Test angles and node has been built before
print("angles\n",angles)
print("nodes\n",nodes)

#Checking the number of filtered contours
# cv2.imshow("Binary",white)

# Using to close currently opened windows 
# cv2.waitKey(0)
# cv2.destroyAllWindows()


####SHAPE DETECTION USING KNOWLEDGE BASED RULES####
# Using Clipspy, A python interface for CLIPS

rules.detect_shape(angles, nodes)