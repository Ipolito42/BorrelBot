#!/usr/bin/env python
# coding: Latin-1

import maestro
import cv2
import time
import numpy as np

# ================================================================================================================================
# |=============================== This class translates position angle to number of steps =======================================|
# |========================================== for each servo of the BorrelBot ====================================================|
# ================================================================================================================================


global rad_per_step_list
global servo_steps_list

class set_destination():
	def __init__(self,
				agent=None, speed=15, acceleration=5):
		global rad_per_step_list
		global servo_steps_list

		rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561, 0.000561] # rad per step 
		servo_steps_list = [[4000, 6000, 8000], [3000, 6000, 9900], [4000, 6000, 8000], [2000, 6000, 8500], [4000, 5000, 7700]] # [min, middle, max]
		
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
			Returns the steps required for the servos to rotate to some position angle
		'''
		servo_steps = servo_steps_list[servo_number]
		if servo_number==4:
			steps = int(servo_steps[1] + (self.pos_angles[servo_number])/rad_per_step_list[servo_number])
		else:
			steps = int(servo_steps[1] - (self.pos_angles[servo_number])/rad_per_step_list[servo_number])
		

		# To now allow the servos to exceed their minimum and maximum steps
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
		self.agent.setTarget(0, servo_steps_list[0][1])
		self.agent.setTarget(1, servo_steps_list[1][1])
		self.agent.setTarget(2, servo_steps_list[2][1])
		self.agent.setTarget(3, servo_steps_list[3][1])
		self.agent.setTarget(4, servo_steps_list[4][1])
		self.agent.setTarget(5, 5500)

	

	def grab(self,):
		'''
			Rotates the gripper servo to grab the target
		'''
		self.agent.setTarget(5, 4000)





	def main(self, pos_angles):
		'''
			Args:
				pos_angles: list of position angles for each servo
			Rotates the servos to the desired angle
		'''
		steps = []
		self.pos_angles = pos_angles
		if self.agent!=None:

			for i in range(5):
				self.set_speed_acceleration(i)
				self.agent.setTarget(i, self.get_steps_from_position(i))

# ================================================================================================================================
# ================================================================================================================================


# 	grappler servo
# 	open at 5500 steps
# 	middle at 4750 steps
# 	closed at 4000 steps

