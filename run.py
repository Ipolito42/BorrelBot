#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np
import tinyik

from set_destination import set_destination
from camera_code import camera_code



# Calculate analytic model parameters
theta = np.arctan(36/14)

x_0 = 0.14
z_0 = 0.36

x_1 = (120*np.cos(np.arctan(theta)) + 0.14)/100
z_1 = (120*np.sin(np.arctan(theta)) + 0.36)/100

x_2 = (90*np.sin(np.arctan(theta)) + x_1)/100
z_2 = (z_1 - 90*np.cos(np.arctan(theta)))/100

x_3 = (28*np.sin(np.arctan(theta)) + x_2)/100
z_3 = (z_2 - 28*np.cos(np.arctan(theta)))/100



arm = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1], 'y', [x_2, 0, z_2], 'x', [x_3 , 0, z_3]])



# If servo controller is connected to port COM8 it will run the motors
# Otherwise it just runs the model and skips the motor code
try: 
	servo_agent = maestro.Controller('COM8') # Setup connection with the correct USB port
except: servo_agent=None


# Make tinyik model with our servos coordinates and directions

arm = tinyik.Actuator(['z', [0.14, 0., 0.36], # Base
				  	'y', [x_0, 0, z_0], # Base arm
					'y', [x_1, 0, z_1], # Elbow
					'x', [x_2 , 0, z_2]]) # Wrist


# arm_model = tinyik.Actuator(['z', [0.14, 0., 0.36], # Base
# 							'y', [x_0/100, 0, z_0/100], # Base arm
# 							'y', [x_1/100, 0, z_1/100], # Elbow
# 							'x', [x_2/100, 0, z_2/100]]) # Wrist



# Destination coordinates will be given by the camera
# destination_coordinates = [float((input("Give x: "))),float((input("Give y: "))),float((input("Give z: ")))]



try:
	# Initialize the classes
	camera = camera_code()
	motors = set_destination(arm_model, servo_agent)

	# Wait a sec to properly initialize everything
	time.sleep(1)

	# 
	destination_coordinates_previous = [0,0,0]


	while True:
		# Calculate the destination coordinates from an image
		destination_coordinates = camera.main(show_camera=False)

		if destination_coordinates != None:
			destination_coordinates_previous = destination_coordinates
		elif destination_coordinates == None:
			destination_coordinates = destination_coordinates_previous

		# Move motors such that the endpoint reaches to the destination coordinates
		motors.main(destination_coordinates, vizualization=False)

		# Give some time to the motors to reach the destination
		time.sleep(1)

		# Print the destination coordinates
		if destination_coordinates != None:
			print("x={:.1f}, y={:.1f} z={:.1f}".format(destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]))

		

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	# Kill all windows when "q" is pressed
	cv2.destroyAllWindows() 
	cv2.VideoCapture(0).release()

except KeyboardInterrupt:
	print("Shutdown")









# Will loop over main with coordinates given by the camera in the loop
# need to turn the vizualization parameter to false to run in the loop


# motors.set_to_parked_position()