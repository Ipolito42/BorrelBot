#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np
# import tinyik

from set_destination import set_destination
from camera_code import camera_code
from inverse_kinematics import inverse_kinematics



# If servo controller is connected to port COM8 it will run the motors
try: 
	servo_agent = maestro.Controller('COM8') # Setup connection with the correct USB port
except: servo_agent = None

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------Destination coordinates will be given by the camera---------------------------------
# --------------------------------------------This is for testing only-------------------------------------------------

# destination_coordinates = [float((input("Give x: "))),float((input("Give y: "))),float((input("Give z: ")))]

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


try:
	# Initialize the classes
	camera = camera_code()
	motors = set_destination(servo_agent)
	ik = inverse_kinematics()

	# Wait a sec to properly initialize everything
	time.sleep(1)

	# Default value otherwise it's None type
	destination_coordinates_previous = [0,0,0]


	while True:
		# Calculate the destination coordinates from an image
		destination_coordinates = camera.main(show_camera=True)

		if destination_coordinates != None:
			if destination_coordinates[0] < 15 and destination_coordinates[1] < 15 and destination_coordinates[2] < 15:
				print("TARGET LOCKED")
			
				# inverse_kinematics is the pybullet class which calculates the position angle for each motor given the destination coordinates
				pos_angles = ik.get_motor_position_angles(destination_coordinates)
				# Move motors such that the endpoint reaches to the destination coordinates
				motors.main(pos_angles)

				# Give some time to the motors to reach the destination
				time.sleep(2)

				# Print the destination coordinates
				print("x={:.1f}, y={:.1f} z={:.1f}".format(destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]))

				break
				print("TARGET REACHED")


		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	# Kill all windows when "q" is pressed
	cv2.destroyAllWindows() 
	cv2.VideoCapture(0).release()

except KeyboardInterrupt:
	print("User Shutdown")



# motors.set_to_parked_position()