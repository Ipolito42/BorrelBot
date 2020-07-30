#!/usr/bin/env python
# coding: Latin-1


import tinyik
import numpy as np
import maestro


theta = np.arccos(9.2/12)

x_0 = 1.4
z_0 = 3.6

x_1 = 12*np.cos(theta)
z_1 = 12*np.sin(theta)

x_2 = 9*np.sin(theta)
z_2 = -9*np.cos(theta)

x_3 = 2.8*np.sin(theta)
z_3 = -2.8*np.cos(theta)

x_4 = 8
z_4 = 0



arm = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1], 'y', [x_2, 0, z_2], 'x', [x_3 , 0, z_3], 'y', [x_4, 0, z_4]])

# Trying to find link and joint locations
link = arm.components[3].coord
joint = arm.components[4]._x_rot(arm.angles[4])
print(link)


# # Destination Coordinates
# destination_coordinates = [15, 0, 0]  
# arm.ee = destination_coordinates


tinyik.visualize(arm)

# Trying to find link and joint locations
link = arm.components[3].coord
joint = arm.components[4]._x_rot(arm.angles[4])
print(link)

# Trying to find link and joint locations
link = arm.components[3].coord
# print(joint.geo())




# Take the motors to default position

# servo = maestro.Controller('COM8') # Setup connection with the correct USB port
# for i in range(6):
#     servo.setSpeed(i, 20)
#     servo.setTarget(i, 6000)