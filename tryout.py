#!/usr/bin/env python
# coding: Latin-1


import tinyik
import numpy as np


# arm = tinyik.Actuator(['z', [0.00001, 0., 0.3], 'y', [1., 0., 0.], 'y', [0.5, 0., 0.], 'x', [0.4, 0., 0.]])
# arm.ee = [-1 , 0.5, 1.2]
# print(arm.angles)
# arm.angles=[np.pi/6, 0, np.pi/6, 0, 0]

arm = tinyik.Actuator(['z', [0.15, 0., 0.4], 'y', [0.421, 0, 1.124], 'y', [0.337, 0, 0.834], 'x', [0.105, 0, 0.2596]])
# arm = tinyik.Actuator(['z', [0.15, 0., 0.4], 'y', [0.421, 0, 1.124], 'y', [0.337, 0, 0.834], 'x', [0.105, 0, 0.2596], 'y', [0.405, 0, 1.012]])
# arm.angles = [[0, 0, 0]]

# steps_0 = int(6000 + arm.angles[0]/0.0005416538925509148)
# min_steps_0 = 3968
# max_steps_0 = 8000
# if steps_0 > max_steps_0:
#     steps_0 = max_steps_0
#     print("exceeded max steps_0")
# elif steps_0 < min_steps_0:
#     steps_0 = min_steps_0
#     print("exceeded min steps_0")
# print(steps_0)


# steps_1 = int(6000 + arm.angles[1]/0.0003926990816987241)
# min_steps_1 = 3000
# max_steps_1 = 9984
# if steps_1 > max_steps_1:
#     steps_1 = max_steps_1
#     print("exceeded max steps_1")
# elif steps_1 < min_steps_1:
#     steps_1 = min_steps_1
#     print("exceeded min steps_1")
# print(steps_1)


# 1 step is 0.0003926990816987241 rad


def angle_to_position(angle, min, max):
    steps = np.rad2deg(angle)*4000 + 6000
# print(arm.ee)
# arm.ee = [-1 , 0.5, 1.2]
# arm.angles = [0., np.pi/2 - np.arctan(40/15)]
print(arm.angles)

# print(120*np.cos(np.arctan(40/15)))
# print(120*np.sin(np.arctan(40/15)))

tinyik.visualize(arm)