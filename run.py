#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np

from set_destination import set_destination
from camera_code import camera_code
from inverse_kinematics import inverse_kinematics



# If servo controller is connected to port COM8 it will run the motors
try: 
	servo_agent = maestro.Controller('COM8') # Check to which port the driver is connected
except: servo_agent = None

try:
	# Initialize the classes
	camera = camera_code()
	motors = set_destination(servo_agent)
	ik = inverse_kinematics()
	# Set the robot the its parking position
	motors.set_to_parked_position()

	# Wait a sec to properly initialize everything
	time.sleep(1)

	while True:
		# Calculate the cap cartesian coordinates from a frame in the camera's frame of reference if a cap is identified
		destination_coordinates = camera.main(show_camera=True)
		
		if destination_coordinates != None:
			# Check if the identified cap is close enough for the robot to reach
			# Once a cap is identified, turn off camera
			if np.abs(destination_coordinates[0]) < 15 and np.abs(destination_coordinates[1]) < 15 and np.abs(destination_coordinates[2]) < 15:
				print("\nTARGET LOCKED")
			
				# Calculate and simulate the required motors' position angles to reach the cap
				pos_angles = ik.get_motor_position_angles(np.array(destination_coordinates)/10)
				# Move motors such that the endpoint reaches the cap
				motors.main(pos_angles)
				# Give some time to the motors to reach the destination
				time.sleep(2)

				print("\nTARGET REACHED")
				print("\nGRABBING BOTTLE")

				# Grab the bottle
				motors.grab()
				break

		# While the camera is running, it's possible to press "q" to break the loop and stop the camera
		# Once "q" is pressed, break the loop and kill all windows
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	cv2.destroyAllWindows() 
	cv2.VideoCapture(0).release()

# Press Ctrl-c if required to stop the whole process 
except KeyboardInterrupt:
	print("User Shutdown")

# Keep the robot in the destination position for 5 sec then return to the parked position for the motor safety
time.sleep(5)
motors.set_to_parked_position()