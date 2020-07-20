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
	img_converted = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	# HLS
	# white = [[50, 50, 180], [170, 180, 255]]
	# HSV
	white = [[10, 120, 210], [50, 255, 255]]

	lower = np.array(white[0])
	upper = np.array(white[1])
		
	mask = cv2.inRange(img_converted, lower, upper)
	img_masked = cv2.bitwise_and(img_converted, img_converted, mask = mask)
	img_masked = cv2.GaussianBlur(img_masked, (5,5),0)

	return img_masked, mask, img_converted



def detect_ellipse(image, frame):
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
			except: pass
	try:
		cap_distance = camera_focal_length*cap_width/major
		cv2.putText(image, "{:.1f}".format(cap_distance) , (x+text_dist/3,y+text_dist/3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
		# Draw the fitted ellipse
		output = cv2.ellipse(image,ellipse,(0,255,0),2)
		
	except:
		output = image

	# Draw the biggest contour if an ellipse is not successfully fitted
	# output = cv2.drawContours(image, big_contour, -1, (255,0,0), 3)
	return output

	

counter = 0
number_to_avg = 50
radius_list = np.zeros(number_to_avg)
cam = cv2.VideoCapture(0)
cam.set(3,1280) # Width
cam.set(4,1024) # Height
# cam.set(5, 25) # Frame rate
cam.set(15, -5) # Exposure time 2^(-5)



while True:
	ret, img = cam.read()
	img_masked, mask, img_converted = mask_color(img)
	img_fit_ellipse = detect_ellipse(img, img_masked)

	# For Testing

	# print(img_converted[240,360,:])
	# cv2.circle(img_converted, (360, 240), 10, (0, 255, 0), 4)

	
	cv2.imshow("input", img_fit_ellipse)

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