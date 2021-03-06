#!/usr/bin/env python
# coding: Latin-1
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

# ================================================================================================================================
# |============================== This class utilizes opencv to identify a blue bottle cap =======================================|
# |================================ and calculates its position in cartesian corrdinates =========================================|
# ================================================================================================================================


global cap_width, camera_focal_length
cap_width = 3 # cm
camera_focal_length = 1430 # pixels 1430 for the camera we have        900 for the laptop integrated camera

class camera_code():
	def __init__(self, 
				):

		global cap_width, camera_focal_length

		self.cam = cv2.VideoCapture(0)
		self.cam.set(3,1280) # Width
		self.cam.set(4,1024) # Height
		# self.cam.set(5, 25) # Frame rate
		# self.cam.set(15, -3) # Exposure time 2^(-3)

		

	def mask_color(self,):
		'''
			Args:
			Detects and makes a mask of anything "sky" blue
		'''
		# converting HSV color coding system
		self.img_HSV = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
		color = [[10, 120, 210], [50, 255, 255]]

		lower_mask_boundary = np.array(color[0])
		upper_mask_boundary = np.array(color[1])
			
		self.mask = cv2.inRange(self.img_HSV, lower_mask_boundary, upper_mask_boundary)
		self.img_masked = cv2.bitwise_and(self.img_HSV, self.img_HSV, mask = self.mask)
		# Blur the image to easier make contours later on
		self.img_masked = cv2.GaussianBlur(self.img_masked, (5,5),0)



	def detect_ellipse(self,):
		# This function is poorly written but it works :)
		'''
			Args:
			Tries to make contours. Keeps the biggest and fits an ellipe. 
			From this ellipse knowing the bottle cap size, it calculates 
			the cartesian 3D coordinates of the botte cap in the camera's 
			coordinate system.
		'''
		# Blur the grayscale image to easier make contours
		self.img_fit_ellipse = self.img_masked.copy()
		gray = cv2.cvtColor(self.img_fit_ellipse, cv2.COLOR_RGB2GRAY)
		gray = cv2.GaussianBlur(gray, (5,5),0)
		ret,th = cv2.threshold(gray ,127,255, 0)

		# Find all the contours in the binary frame 
		contours,hierarchy = cv2.findContours(th,2,1)
		cnt = contours
		big_contour = []
		max_area = 0
		self.ellipse = None
		for i in cnt:
			# Find the contour having biggest area 
			area = cv2.contourArea(i) 
			if(area > max_area):
				max_area = area
				big_contour = i
				try:
					# Fit an ellipse
					self.ellipse = cv2.fitEllipse(i) # (xcenter,ycenter), (MA,ma), angle
					# Extract the fitted ellipse information
					axes = self.ellipse[1]
					self.minor, self.major = axes
					text_dist = int(np.sqrt(self.minor**2 + self.major**2))
					# Calculate the center of the ellipse
					self.xcenter = int(self.ellipse[0][0] - self.width/2)
					self.ycenter = int(self.ellipse[0][1] - self.height/2)
				except: pass

		if self.ellipse != None:
			# Get the cartesian coordinates of the center of the cap
			self.get_coordinates()

			# Draw the fitted ellipse
			self.img_fit_ellipse = cv2.ellipse(self.frame,self.ellipse,(0,255,0),2)

			# Draw the x,y,z coordinates around the ellipse as text
			cv2.putText(self.img_fit_ellipse, "x={:.1f}".format(self.x_coordinate) ,
						(int(self.xcenter + self.width/2 -text_dist/3),int(self.ycenter + self.height/2+text_dist/3)),
						 cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

			cv2.putText(self.img_fit_ellipse, "y={:.1f}".format(self.y_coordinate) ,
						(int(self.xcenter + self.width/2+text_dist/3),int(self.ycenter + self.height/2-text_dist/3)),
						 cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

			cv2.putText(self.img_fit_ellipse, "z={:.1f}".format(self.z_coordinate) ,
						(int(self.xcenter + self.width/2+text_dist/3),int(self.ycenter + self.height/2+text_dist/3)),
						 cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

			
			
		else:
			self.img_fit_ellipse = self.frame

		# Alternatively, draw the biggest contour if an ellipse is not successfully fitted
			# self.img_fit_ellipse = cv2.drawContours(self.img_fit_ellipse, big_contour, -1, (255,0,0), 3)

	

	def get_coordinates(self,):
		'''
			Args:
			Calculates the cartesian coordinates of the center of the fitted ellipse
		'''
		self.x_coordinate = camera_focal_length*cap_width / self.major
		self.y_coordinate = self.xcenter * cap_width / self.major
		self.z_coordinate = -self.ycenter * cap_width / self.major


	def main(self,show_camera=True):
		'''
			Args:
			Reads a frame and returns the cap cartesian coordinates in the camera frame of reference if a cap is identified
		'''
		ret, self.frame = self.cam.read()
		self.height, self.width, _ = self.frame.shape
		

		self.mask_color()
		self.detect_ellipse()

		# For Testing
		# print(img[240,360,:])
		# cv2.circle(self.img_fit_ellipse, (360, 240), 10, (218, 177, 44), 4)
		# 218, 177, 44

		# img_HSV
		# img_masked
		# img_fit_ellipse

		# To show the camera feed with the ellipse and the calculated coordinates
		if show_camera:
			cv2.imshow("input", self.img_fit_ellipse)

		if self.ellipse != None:
			# The return list is scrambled because of the pybullet's frame of reference being different
			return [self.z_coordinate, self.x_coordinate, -self.y_coordinate]

# ================================================================================================================================
# ================================================================================================================================