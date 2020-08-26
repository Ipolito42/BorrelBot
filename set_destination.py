#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np

# servo base servo
# 1 step is 0.031034482 deg = 0.0005416538925509148 rad
# 	beginning = 3968 steps
# 	middle = 6000 steps
# 	end = 8000 steps

# servo base arm servo
# 	1 step is 0.0025 deg = 0.0003926990816987241 rad
# 	z axis = 8300 steps
# 	90 deg = 4300 steps

# 	beginning = 3000 steps
# 	middle = 6492 steps
# 	end = 9984 steps

# servo elbow servo
# 	1 step is 0.0025 deg = 0.00039269908169872416 rad
# 	z axis =  steps
# 	90 deg = 4000 steps

# 	beginning = 4000 steps
# 	middle = 6000 steps
# 	end = 8000 steps

# servo wrist x-axis
# 	1 step is 0.03215 deg = 0.00056099868 rad
# 	90 deg = 2800 steps

# 	beginning = 2000 steps
# 	middle = 5250 steps
# 	end = 8500 steps

# servo wrist y-axis
# 	beginning = 4000 steps
# 	end = 7700 steps


# 	servo grappler
# 	open = 5500
# 	middle 4750
# 	closed = 4000


global rad_per_step_list
global servo_steps_list

class set_destination():
	def __init__(self,
				agent=None, speed=15, acceleration=5):
		global rad_per_step_list
		global servo_steps_list

		rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561, 0.000561]
		servo_steps_list = [[4000, 6000, 8000], [3000, 6000, 9900], [4000, 6000, 8000], [2000, 6000, 8500], [4000, 6000, 7700]] # [min, middle, max]

		self.agent = agent
		self.speed = speed
		self.acceleration = acceleration


	def set_speed_acceleration(self, servo_number):
		'''
			Args:
				servo_number: Servo number on the board
			Sets the speed and acceleration of the servos
		'''

		self.agent.setAccel(servo_number, self.acceleration)
		self.agent.setSpeed(servo_number, self.speed)


	def get_steps_from_position(self, servo_number):
		'''
			Args:
				servo_number: Servo number on the board
			Returns the steps required for the servos to rotate to the appropriate angle calculated from the IK model
		'''
		servo_steps = servo_steps_list[servo_number]
		steps = int(servo_steps[1] + (self.pos_angles[servo_number])/rad_per_step_list[servo_number])


		if steps > servo_steps_list[servo_number][2]:
			print("exceeded max steps in servo 0\ngoal was %i steps"%steps)
			steps = servo_steps_list[servo_number][2]

		elif steps < servo_steps_list[servo_number][0]:
			print("exceeded min steps in servo 0\ngoal was %i steps"%steps)
			steps = servo_steps_list[servo_number][0]

		print("Servo %i location in steps: %i" %(servo_number, steps))
		return steps



	def set_to_parked_position(self,):
		'''
			Returns all the servos to the parked position before switching off
		'''
		self.agent.setTarget(0, servo_steps_list[0][2])
		self.agent.setTarget(1, servo_steps_list[1][2])
		self.agent.setTarget(2, servo_steps_list[2][2])
		self.agent.setTarget(3, servo_steps_list[3][2])
		self.agent.setTarget(3, servo_steps_list[4][2])
	

	def grab(self,):
		self.agent.setTarget(5, 4000)





	def main(self, pos_angles):
		steps = []
		self.pos_angles = pos_angles
		# for i in range(5):
		# 	steps.append(self.get_steps_from_position(i))
		# 	print(steps, i)

		if self.agent!=None:

			for i in range(5):
				self.set_speed_acceleration(i)
				self.agent.setTarget(i, self.get_steps_from_position(i))



