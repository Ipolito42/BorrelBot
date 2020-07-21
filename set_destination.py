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
	def __init__(self, model, destination_coordinates, agent=None):

		rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561]
		min_max_servo_steps_list = [[3968, 8000], [3000, 9984], [4000, 8000], [2000, 8500]]

		self.destination_coordinates = [destination_coordinates]
		self.model = model
		self.agent = agent
		

		

		



	def set_speed_acceleration(self, servo_number, speed=15, accel=5):
		self.agent.setAccel(servo_number, accel)
		self.agent.setSpeed(servo_number, speed)


	def get_steps_from_position(self, servo_number):
		rad_per_step = rad_per_step_list[servo_number]
		if servo_number==0:
			steps = int(5100 + self.model.angles[servo_number]/rad_per_step)
		if servo_number==1:
			steps = int(6000 + self.model.angles[servo_number]/rad_per_step)
		if servo_number==2:
			steps = int(6000 + (self.model.angles[servo_number])/rad_per_step)
		if servo_number==3:
			steps = int(6000 + self.model.angles[servo_number]/rad_per_step)

		if steps > min_max_servo_steps_list[servo_number][1]:
			print("exceeded max steps in servo 0\ngoal was %i steps"%steps)
			steps = min_max_servo_steps_list[servo_number][1]
			
		elif steps < min_max_servo_steps_list[servo_number][0]:
			print("exceeded min steps in servo 0\ngoal was %i steps"%steps)
			steps = min_max_servo_steps_list[servo_number][0]

		print("Servo %i location in steps: %i" %(servo_number, steps))
		return steps


	def set_destination_coordinates(self,):
		self.destination = [[self.destination_coordinates[0][0] + 1.66371003, self.destination_coordinates[0][1], self.destination_coordinates[0][2] + 2.18830734]]
		self.destination_model = [[self.destination_coordinates[0][0] + 1.81472887, self.destination_coordinates[0][1], self.destination_coordinates[0][2] + 0.52638276]]
		# 0 + 1.81472887, 0, 0 + 0.52638276
		print("Destination coordinates:", self.destination)

	


	def set_to_parked_position(self,):
		self.agent.setTarget(0, min_max_servo_steps_list[0][1])
		self.agent.setTarget(1, min_max_servo_steps_list[1][1])
		self.agent.setTarget(2, min_max_servo_steps_list[2][1])
		self.agent.setTarget(3, min_max_servo_steps_list[3][1])




	def main(self, speed=15):
		self.set_destination_coordinates()
		print(self.destination)
		self.model.ee = self.destination_model
		tinyik.visualize(self.model)

			
		if self.agent!=None:
			# Set speed and acceleration of the servos
			self.set_speed_acceleration(self.agent, 0, speed)
			self.set_speed_acceleration(self.agent, 1, speed)
			self.set_speed_acceleration(self.agent, 2, speed)
			self.set_speed_acceleration(self.agent, 3, speed)

			self.agent.setTarget(0, self.get_steps_from_position(arm, 0)) # Base
			self.agent.setTarget(1, self.get_steps_from_position(arm, 1)) # Base Arm
			self.agent.setTarget(2, self.get_steps_from_position(arm, 2)) # Elbow Arm
			self.agent.setTarget(3, self.get_steps_from_position(arm, 3)) # Wrist

		
	







# Calculate analytic model parameters
theta = np.arctan(36/14)
x_0 = 120*np.cos(np.arctan(theta))
z_0 = 120*np.sin(np.arctan(theta))

x_1 = 90*np.cos(np.arctan(theta))
z_1 = 90*np.sin(np.arctan(theta))

x_2 = 28*np.cos(np.arctan(theta))
z_2 = 28*np.sin(np.arctan(theta))


try: 
	servo_agent = maestro.Controller('COM8') # Setup connection with the correct USB port
except: servo_agent=None

arm_model = tinyik.Actuator(['z', [0.14, 0., 0.36], 'y', [x_0/100, 0, z_0/100], 'y', [x_1/100, 0, z_1/100], 'x', [x_2/100, 0, z_2/100]]) # Create the initial full model of the arm_model

destination_coordinates = [float((input("Give x: "))),float((input("Give y: "))),float((input("Give z: ")))]


if __name__ == "__main__":
	set_destination(arm_model, destination_coordinates, servo_agent).main()