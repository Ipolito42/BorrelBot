#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np
import tinyik

from set_destination import set_destination



# Calculate analytic model parameters
theta = np.arctan(36/14)
x_0 = 120*np.cos(np.arctan(theta))
z_0 = 120*np.sin(np.arctan(theta))

x_1 = 90*np.cos(np.arctan(theta))
z_1 = 90*np.sin(np.arctan(theta))

x_2 = 28*np.cos(np.arctan(theta))
z_2 = 28*np.sin(np.arctan(theta))



# If servo controller is connected to port COM8 it will run the motors
# Otherwise it just runs the model and skips the motor code
try: 
	servo_agent = maestro.Controller('COM8') # Setup connection with the correct USB port
except: servo_agent=None


# Make tinyik model with our servos coordinates and directions
arm_model = tinyik.Actuator(['z', [0.14, 0., 0.36], # Base
							'y', [x_0/100, 0, z_0/100], # Base arm
							'y', [x_1/100, 0, z_1/100], # Elbow
							'x', [x_2/100, 0, z_2/100]]) # Wrist



# Destination coordinates will be given by the camera
destination_coordinates = [float((input("Give x: "))),float((input("Give y: "))),float((input("Give z: ")))]



# Make an initialization of the set_destination
motors = set_destination(arm_model, servo_agent)


# Will loop over main with coordinates given by the camera in the loop
# need to turn the vizualization parameter to false to run in the loop
# motors.main(destination_coordinates, vizualization=True)

motors.set_to_parked_position()