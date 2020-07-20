#!/usr/bin/env python
# coding: Latin-1

# import numpy as np
import maestro
import cv2
import time
import numpy as np
import tinyik

'''
servo base servo
1 step is 0.031034482 deg = 0.0005416538925509148 rad
	beginning = 3968 steps
	middle = 5984 steps
	end = 8000 steps

servo base arm servo
	1 step is 0.0025 deg = 0.0003926990816987241 rad
	z axis = 8300 steps
	90 deg = 4300 steps

	beginning = 3000 steps
	middle = 6492 steps
	end = 9984 steps

servo elbow servo
	1 step is 0.0025 deg = 0.00039269908169872416 rad
	z axis =  steps
	90 deg = 4000 steps

	beginning = 4000 steps
	middle = 6000 steps
	end = 8000 steps

servo wrist
	1 step is 0.03215 deg = 0.00056099868 rad
	90 deg = 2800 steps

	beginning = 2000 steps
	middle = 5250 steps
	end = 8500 steps

'''
global rad_per_step_list
global min_max_servo_steps_list
rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561]
min_max_servo_steps_list = [[3968, 8000], [3000, 9984], [4000, 8000], [2000, 8500]]


def set_speed_acceleration(agent, motor_number, speed=15, accel=5):
	agent.setAccel(motor_number, accel)
	agent.setSpeed(motor_number, speed)


def get_steps_from_position(agent, servo_number):
	rad_per_step = rad_per_step_list[servo_number]
	if servo_number==0:
		steps = int(5984 + agent.angles[servo_number]/rad_per_step)
	if servo_number==1:
		steps = int(6492 + agent.angles[servo_number]/rad_per_step)
	if servo_number==2:
		steps = int(6000 + (agent.angles[servo_number])/rad_per_step)
	if servo_number==3:
		steps = int(5250 + agent.angles[servo_number]/rad_per_step)

	if steps > min_max_servo_steps_list[servo_number][1]:
		print("exceeded max steps in servo 0\ngoal was %i steps"%steps)
		steps = min_max_servo_steps_list[servo_number][1]
		
	elif steps < min_max_servo_steps_list[servo_number][0]:
		print("exceeded min steps in servo 0\ngoal was %i steps"%steps)
		steps = min_max_servo_steps_list[servo_number][0]

	print("Servo %i location in steps: %i" %(servo_number, steps))
	return steps


def set_destination(coordinates):
	destination = [[-coordinates[0][0] + 1.66371003, -coordinates[0][1], -coordinates[0][2] + 2.18830734]]
	print("Destination coordinates:", destination)
	return destination


def parked_position(agent):
	agent.setTarget(0, min_max_servo_steps_list[0][1])
	agent.setTarget(1, min_max_servo_steps_list[1][1])
	agent.setTarget(2, min_max_servo_steps_list[2][1])
	agent.setTarget(3, min_max_servo_steps_list[3][1])



# Calculate analytic model parameters

theta = np.arctan(36/14)
x_0 = 120*np.cos(np.arctan(theta))
z_0 = 120*np.sin(np.arctan(theta))

x_1 = 90*np.cos(np.arctan(theta))
z_1 = 90*np.sin(np.arctan(theta))

x_2 = 28*np.cos(np.arctan(theta))
z_2 = 28*np.sin(np.arctan(theta))



servo = maestro.Controller('COM8') # Setup connection with the correct USB port

arm = tinyik.Actuator(['z', [0.14, 0., 0.36], 'y', [x_0/100, 0, z_0/100], 'y', [x_1/100, 0, z_1/100], 'x', [x_2/100, 0, z_2/100]]) # Create the initial full model of the arm

# Set speed and acceleration of the servos


def main(agent, model, destination_coordinates, speed=15):
	try:
		model.ee = set_destination(destination_coordinates)

		set_speed_acceleration(agent, 0, speed)
		set_speed_acceleration(agent, 1, speed)
		set_speed_acceleration(agent, 2, speed)
		set_speed_acceleration(agent, 3, speed)

		agent.setTarget(0, get_steps_from_position(arm, 0)) # Base
		agent.setTarget(1, get_steps_from_position(arm, 1)) # Base Arm
		agent.setTarget(2, get_steps_from_position(arm, 2)) # Elbow Arm
		agent.setTarget(3, get_steps_from_position(arm, 3)) # Wrist

	except: pass

destination_coordinates = [[0, 0, 0]]
main(servo, arm, destination_coordinates)

# parked_position(servo)