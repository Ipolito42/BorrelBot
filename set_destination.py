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

class set_destination():
	def __init__(self, 
				model, 
				agent=None, speed=15, acceleration=5):
		global rad_per_step_list
		global min_max_servo_steps_list

		rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561]
		min_max_servo_steps_list = [[3968, 8000], [3000, 9984], [4000, 8000], [2000, 8500]]

		
		self.model = model
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


	def get_steps_from_position(self, servo_number, 
									servo_0_middle=5100,
									servo_1_middle=6000,
									servo_2_middle=6000,
									servo_3_middle=6000):
		'''
			Args:
				servo_number: Servo number on the board
			Returns the steps required for the servos to rotate to the appropriate angle calculated from the IK model
		'''
		rad_per_step = rad_per_step_list[servo_number]
		if servo_number==0:
			steps = int(servo_0_middle + self.model.angles[servo_number]/rad_per_step)
		if servo_number==1:
			steps = int(servo_1_middle + self.model.angles[servo_number]/rad_per_step)
		if servo_number==2:
			steps = int(servo_2_middle + (self.model.angles[servo_number])/rad_per_step)
		if servo_number==3:
			steps = int(servo_3_middle + self.model.angles[servo_number]/rad_per_step)

		if steps > min_max_servo_steps_list[servo_number][1]:
			print("exceeded max steps in servo 0\ngoal was %i steps"%steps)
			steps = min_max_servo_steps_list[servo_number][1]
			
		elif steps < min_max_servo_steps_list[servo_number][0]:
			print("exceeded min steps in servo 0\ngoal was %i steps"%steps)
			steps = min_max_servo_steps_list[servo_number][0]

		print("Servo %i location in steps: %i" %(servo_number, steps))
		return steps


	def set_destination_coordinates(self,):
		'''
			Args: None
			Sets the corrected destination coordinates
		'''
		self.destination = [[self.destination_coordinates[0][0] + 1.66371003, self.destination_coordinates[0][1], self.destination_coordinates[0][2] + 2.18830734]]
		self.destination_model = [[self.destination_coordinates[0][0] + 1.81472887, self.destination_coordinates[0][1], self.destination_coordinates[0][2] + 0.52638276]]
		# print("Destination coordinates:", self.destination)

	


	def set_to_parked_position(self,):
		'''
			Returns all the servos to the parked position before switching off
		'''
		self.agent.setTarget(0, min_max_servo_steps_list[0][1])
		self.agent.setTarget(1, min_max_servo_steps_list[1][1])
		self.agent.setTarget(2, min_max_servo_steps_list[2][1])
		self.agent.setTarget(3, min_max_servo_steps_list[3][1])




	def main(self, destination_coordinates, vizualization=True):
		'''
			Args:
				destination_coordinates: a list [x,y,z] of the destination coordinates
			Kwargs:
				vizualization: pops a 3d vizualization window with a rotatable model of the arm
			Moves the motors to the destination coordinates and if requested pops a vizualization window of the model
		'''
		self.destination_coordinates = [destination_coordinates]
		self.set_destination_coordinates()
		self.model.ee = self.destination_model
		if vizualization:
			tinyik.visualize(self.model)

			
		if self.agent!=None:
			# Set speed and acceleration of the servos
			# self.set_speed_acceleration(self.agent, 0)
			# self.set_speed_acceleration(self.agent, 1)
			# self.set_speed_acceleration(self.agent, 2)
			# self.set_speed_acceleration(self.agent, 3)

			# self.agent.setTarget(0, self.get_steps_from_position(arm, 0)) # Base
			# self.agent.setTarget(1, self.get_steps_from_position(arm, 1)) # Base Arm
			# self.agent.setTarget(2, self.get_steps_from_position(arm, 2)) # Elbow Arm
			# self.agent.setTarget(3, self.get_steps_from_position(arm, 3)) # Wrist

			for i in range(4):
				self.set_speed_acceleration(i)
				self.agent.setTarget(i, self.get_steps_from_position(i))