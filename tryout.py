#!/usr/bin/env python
# coding: Latin-1


import tinyik
import numpy as np
import maestro


servo = maestro.Controller('COM8') # Setup connection with the correct USB port

# arm = tinyik.Actuator(['z', [0.00001, 0., 0.3], 'y', [1., 0., 0.], 'y', [0.5, 0., 0.], 'x', [0.4, 0., 0.]])
# arm.ee = [-1 , 0.5, 1.2]
# print(arm.angles)
# arm.angles=[np.pi/6, 0, np.pi/6, 0, 0]

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
# arm = tinyik.Actuator(['z', [0.15, 0., 0.4], 'y', [0.421, 0, 1.124], 'y', [0.337, 0, 0.834], 'x', [0.105, 0, 0.2596], 'y', [0.405, 0, 1.012]])
# arm.angles = [[0, 0, 0]]
# destination_coordinates = [ 0 + 1.81472887, 0, 0 + 0.52638276]
# arm.ee = destination_coordinates

# servo.setSpeed(2, 30)
# servo.setTarget(2, 8000)

# print()
# print(120*np.sin(np.arctan(theta)))
# print(np.rad2deg(np.arctan(36/7)))
tinyik.visualize(arm)