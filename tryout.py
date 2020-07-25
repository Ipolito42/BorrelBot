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

theta = np.arctan(9.2/1.4)

x_0 = 1.4
z_0 = 9.2


x_1 = (12*np.cos(theta))
z_1 = (12*np.sin(theta))

x_2 = (9*np.sin(theta))
z_2 = (-9*np.cos(theta))

x_3 = (2.8*np.sin(theta))
z_3 = (-2.8*np.cos(theta))

x_4 = (8*np.sin(theta))/10
z_4 = (8*np.cos(theta))/10



arm = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1], 'y', [x_2, 0, z_2], 'x', [x_3 , 0, z_3], 'y', [x_4, 0, z_4]])
# kwstas = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1]])
arm = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1], 'y', [x_2, 0, z_2], 'x', [x_3 , 0, z_3], 'y', [x_4, 0, z_4]])
# del(kwstas)
# arm.angles = [0,np.pi/2]
destination_coordinates = [10, 0, 5]
arm.ee = destination_coordinates
print("asdasd", 12*np.sin(theta + arm.angles[1]))
tinyik.visualize(arm)


kwstas = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1]])
kwstas.angles = [arm.angles[0], arm.angles[1]]
print(kwstas.ee)
# joint = tinyik.visualizer.Joint(arm.components[4])
# geo = joint.geo()
# print(joint.geo())

# print(arm.components[3].coord)
# print(arm.components[4].coord)



# tinyik.visualize(kwstas)
# servo.setSpeed(2, 30)
# servo.setTarget(2, 8000)