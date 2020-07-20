#!/usr/bin/env python
# coding: Latin-1
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt


global cap_width, camera_focal_length
cap_width = 3 # cm
camera_focal_length = 900 # pixels 1430 for the camera we have        1050 is for my laptop

def mask_color(frame):
	img_conv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	# HLS
	# white = [[50, 50, 180], [170, 180, 255]]
	# HSV
	white = [[10, 120, 210], [50, 255, 255]]

	lower = np.array(white[0])
	upper = np.array(white[1])
		
	mask = cv2.inRange(img_conv, lower, upper)
	output = cv2.bitwise_and(img_conv, img_conv, mask = mask)
	output = cv2.GaussianBlur(output, (5,5),0)

	return output, mask, img_conv



def detect_contour(image, frame):
	#--- First obtain the threshold using the greyscale image ---

	


	output = frame.copy()
	gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5),0)
	ret,th = cv2.threshold(gray,127,255, 0)

	#--- Find all the contours in the binary image ---
	contours,hierarchy = cv2.findContours(th,2,1)
	cnt = contours
	big_contour = []
	max_area = 0
	for i in cnt:
		area = cv2.contourArea(i) #--- find the contour having biggest area ---
		if(area > max_area):
			max_area = area
			big_contour = i
			try:
				ellipse = cv2.fitEllipse(i) # (xcenter,ycenter), (MA,ma), angle
				axes = ellipse[1]
				minor, major = axes
				text_dist = int(np.sqrt(minor**2 + major**2))
				x = int(ellipse[0][0])
				y = int(ellipse[0][1])
				# print(x)
				# print(axes)
			except: pass
	try:
		cap_distance = camera_focal_length*cap_width/major
		cv2.putText(image, "{:.1f}".format(cap_distance) , (x+text_dist/3,y+text_dist/3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
		output = cv2.ellipse(image,ellipse,(0,255,0),2)
		
	except:
		output = image

	# output = cv2.drawContours(image, big_contour, -1, (255,0,0), 3)
	return output

	

counter = 0
number_to_avg = 50
radius_list = np.zeros(number_to_avg)
#capture from camera at location 0
cap = cv2.VideoCapture(0)
#set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(3,1280) # Width
cap.set(4,1024) # Height
# cap.set(5, 25) # Frame rate
cap.set(15, -5) # Exposure time 2^(-5)



while True:
	ret, img = cap.read()
	# img = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
	# img_conv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	# cv2.circle(img_conv, (640, 360), 10, (0, 255, 0), 4)
	# # print(np.shape(img_conv))
	# print(img_conv[640, 360,:])
	output, mask, img_conv = mask_color(img)
	print(img_conv[240,360,:])
	cv2.circle(img_conv, (360, 240), 10, (0, 255, 0), 4)

	output_circle = detect_contour(img, output)
	

	
	
	# counter += 1
	

	# if counter >= number_to_avg:
	# 	print(np.median(radius_list))
	# 	counter = 0
	cv2.imshow("input", output_circle)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()










# def detect_circles(frame):
# 	output = frame.copy()
# 	gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
# 	gray = cv2.GaussianBlur(gray, (5,5),0)
# 	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=2.2, minDist=120)
# 	radius = 0
# 	# ensure at least some circles were found
# 	if circles is not None:
# 		# convert the (x, y) coordinates and radius of the circles to integers
# 		circles = np.round(circles[0, :]).astype("int")
# 		# loop over the (x, y) coordinates and radius of the circles
# 		for (x, y, r) in circles:
# 			# draw the circle in the output image, then draw a rectangle
# 			# corresponding to the center of the circle
# 			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
# 			# cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)
# 			radius = r
# 	return output, radius