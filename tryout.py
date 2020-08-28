#!/usr/bin/env python
# coding: Latin-1


import tinyik
import numpy as np
import maestro
import csv

import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------  URDF CALCULATIONS  ------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------
# ---------------------joint origins-------------------------
# -----------------------------------------------------------
theta = np.arccos(9.2/12)
# print(np.arccos(9.5/12))
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

x = ["%.4f" % item for item in [x_0_0*10, x_0*10, x_1*10, x_2*10, x_3*10, x_4*10]]
y = ["%.4f" % item for item in np.zeros(len(x))]
z = ["%.4f" % item for item in [z_0_0*10, z_0*10, z_1*10, z_2*10, z_3*10, z_4*10]]

# # -----------------------------------------------------------
# # ---------------------link origins-------------------------
# # -----------------------------------------------------------

# '''
# x = (0, 0.007, 0.06, 0.693, 0.742)
# z = (0.028, 0.074, 0.131, 0.0893, 0.0786)
# '''


# x_origin_0_0 = (x_0_0) / 2
# z_origin_0_0 = (z_0_0) / 2

# x_origin_0 = (x_0_0 + x_0)/2
# z_origin_0 = (z_0_0 + z_0)/2

# x_origin_1 = (x_1 + x_0) / 2
# z_origin_1 = (z_1 + z_0) / 2

# x_origin_2 = (x_2 + x_1) / 2
# z_origin_2 = (z_2 + z_1) / 2

# x_origin_3 = (x_3 + x_2) / 2
# z_origin_3 = (z_3 + z_2) / 2

# x_origin_4 = (x_4 + x_3) / 2
# z_origin_4 = (z_4 + z_3) / 2

# x_origin = ["%.4f" % item for item in [x_origin_0_0, x_origin_0, x_origin_1, x_origin_2, x_origin_3, x_origin_4]]
# y_origin = ["%.4f" % item for item in np.zeros(len(x_origin))]
# z_origin = ["%.4f" % item for item in [z_origin_0_0, z_origin_0, z_origin_1, z_origin_2, z_origin_3, z_origin_4]]

# joint_coordinates = []
# for i in range(len(x)):
#     joint_coordinates.append([x[i], y[i], z[i]])

# link_coordinates = []
# for i in range(len(x)):
#     link_coordinates.append([x_origin[i], y_origin[i], z_origin[i]])

# data = [["x joint", "y joint", "z joint"]] + joint_coordinates + [["x link", "y link", "z link"]] + link_coordinates

# # np.savetxt("joint_and_link_coordinates.txt", data, delimiter=" ", fmt="%s")


# # ----------------------------------ORIGIN----------------------------------
# # ---------------------------------------------------------------------------

# # plt.plot([0, x_origin_0_0, x_origin_0, x_origin_1, x_origin_2, x_origin_3, x_origin_4], [0, z_origin_0_0, z_origin_0, z_origin_1, z_origin_2, z_origin_3, z_origin_4], "r.")
# # plt.plot([0, x_0_0, x_0, x_1, x_2, x_3, x_4], [0, z_0_0, z_0, z_1, z_2, z_3, z_4], "b-o")
# # plt.show()

# # -------------------------------------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------------------------------------





# lengths = np.array([56, 4, 36, 119, 90, 28, 80])/1000
# halves = lengths/2

# sums=0
# joint_positions = np.zeros(len(lengths))
# origins = np.zeros(len(lengths))
# for i in range(len(lengths)):
#     sums += lengths[i]
#     joint_positions[i] = sums
#     origins[i] = sums - halves[i]
    

# # print("link origins", origins)
# # print("lengths", lengths)
# # print("joint positions", joint_positions)







# Take the motors to default position

# servo = maestro.Controller('COM8') # Setup connection with the correct USB port
# servo.setTarget(4,7700)
# for i in range(6):
#     # servo.setSpeed(i, 20)
#     servo.setTarget(i, 6000)

# rad_per_step_list = [0.000541, 0.000393, 0.000393, 0.000561, 0.000561]

# servo_steps_list = [[4000, 6000, 8000], [3000, 6000, 9900], [4000, 6000, 8000], [2000, 6000, 8500], [4000, 6000, 7700]] # [min, middle, max]
# minimums = []
# maximums = []
# for i in range(len(rad_per_step_list)):
#     a = -(servo_steps_list[i][1] - servo_steps_list[i][0]) * rad_per_step_list[i]
#     b = (servo_steps_list[i][2] - servo_steps_list[i][1]) * rad_per_step_list[i]
    
#     minimums.append(a)
#     maximums.append(b)

#     print(a)



from set_destination import set_destination


servo_agent = maestro.Controller('COM8') # Setup connection with the correct USB port
motors = set_destination(servo_agent)
# motors.set_to_parked_position()
motors.grab()


# import cv2
# from camera_code import camera_code


# import cv2

# cap = cv2.VideoCapture(1)

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()