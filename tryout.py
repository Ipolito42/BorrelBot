#!/usr/bin/env python
# coding: Latin-1


import tinyik
import numpy as np
import maestro
import csv

import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------URDF CALCULATIONS--------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------
# ---------------------joint origins-------------------------
# -----------------------------------------------------------
theta = np.arccos(9.2/12)
print(theta)

'''
x = (0, 0.014, 0.106, 0.684, 0.702, 0.782)
z = (0.056, 0.092, 0.17, 0.100, 0.079, 0.079)
'''

x_0_0 = 0.
z_0_0 = 0.056

x_0 = 0.014 + x_0_0
z_0 = 0.036 + z_0_0

x_1 = 0.12*np.cos(theta) + x_0
z_1 = 0.12*np.sin(theta) + z_0

x_2 = 0.09*np.sin(theta) + x_1
z_2 = -0.09*np.cos(theta) + z_1

x_3 = 0.028*np.sin(theta) + x_2
z_3 = -0.028*np.cos(theta) + z_2

x_4 = 0.08 + x_3
z_4 = 0 + z_3

x = ["%.4f" % item for item in [x_0_0, x_0, x_1, x_2, x_3, x_4]]
y = ["%.4f" % item for item in np.zeros(len(x))]
z = ["%.4f" % item for item in [z_0_0, z_0, z_1, z_2, z_3, z_4]]
# -----------------------------------------------------------
# ---------------------link origins-------------------------
# -----------------------------------------------------------

'''
x = (0, 0.007, 0.06, 0.693, 0.742)
z = (0.028, 0.074, 0.131, 0.0893, 0.0786)
'''


x_origin_0_0 = (x_0_0) / 2
z_origin_0_0 = (z_0_0) / 2

x_origin_0 = (x_0_0 + x_0)/2
z_origin_0 = (z_0_0 + z_0)/2

x_origin_1 = (x_1 + x_0) / 2
z_origin_1 = (z_1 + z_0) / 2

x_origin_2 = (x_2 + x_1) / 2
z_origin_2 = (z_2 + z_1) / 2

x_origin_3 = (x_3 + x_2) / 2
z_origin_3 = (z_3 + z_2) / 2

x_origin_4 = (x_4 + x_3) / 2
z_origin_4 = (z_4 + z_3) / 2

x_origin = ["%.4f" % item for item in [x_origin_0_0, x_origin_0, x_origin_1, x_origin_2, x_origin_3, x_origin_4]]
y_origin = ["%.4f" % item for item in np.zeros(len(x_origin))]
z_origin = ["%.4f" % item for item in [z_origin_0_0, z_origin_0, z_origin_1, z_origin_2, z_origin_3, z_origin_4]]

joint_coordinates = []
for i in range(len(x)):
    joint_coordinates.append([x[i], y[i], z[i]])

link_coordinates = []
for i in range(len(x)):
    link_coordinates.append([x_origin[i], y_origin[i], z_origin[i]])

data = [["x joint", "y joint", "z joint"]] + joint_coordinates + [["x link", "y link", "z link"]] + link_coordinates

# rows = np.array(['row1', 'row2', 'row3'], dtype='|S20')[:, np.newaxis]
# with open('test.csv', 'w') as f:
#     np.savetxt(f, np.hstack((rows, data)), delimiter=', ', fmt='%s')


np.savetxt("joint_and_link_coordinates.txt", data, delimiter=" ", fmt="%s")


# ----------------------------------ORIGIN----------------------------------
# ---------------------------------------------------------------------------

plt.plot([0, x_origin_0_0, x_origin_0, x_origin_1, x_origin_2, x_origin_3, x_origin_4], [0, z_origin_0_0, z_origin_0, z_origin_1, z_origin_2, z_origin_3, z_origin_4], "r.")
plt.plot([0, x_0_0, x_0, x_1, x_2, x_3, x_4], [0, z_0_0, z_0, z_1, z_2, z_3, z_4], "b-o")
plt.show()

# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------

















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

# arm = tinyik.Actuator(['z', [x_0, 0., z_0], 'y', [x_1, 0, z_1], 'y', [x_2, 0, z_2], 'x', [x_3 , 0, z_3], 'y', [x_4, 0, z_4]])

# # Trying to find link and joint locations
# link = arm.components[3].coord
# joint = arm.components[4]._x_rot(arm.angles[4])
# print(link)


# # Destination Coordinates
# destination_coordinates = [15, 0, 0]  
# arm.ee = destination_coordinates


# tinyik.visualize(arm)

# Trying to find link and joint locations
# link = arm.components[3].coord
# joint = arm.components[4]._x_rot(arm.angles[4])
# print(link)

# # Trying to find link and joint locations
# link = arm.components[3].coord
# print(joint.geo())




# Take the motors to default position

# servo = maestro.Controller('COM8') # Setup connection with the correct USB port
# for i in range(6):
#     servo.setSpeed(i, 20)
#     servo.setTarget(i, 6000)