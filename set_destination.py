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
    middle = 6492‬ steps
    end = 9984 steps

servo elbow servo
    1 step is 0.0025 deg = 0.0003926990816987241 rad
    z axis =  steps
    90 deg = 4300 steps

    beginning = 2000 steps
    middle = 5250 steps
    end = 8500 steps

servo wrist
    1 step is 0.03215 deg = 0.00056099868 rad
    90 deg = 2800 steps

    beginning = 2000 steps
    middle = 5250 steps
    end = 8500 steps

'''

global rad_per_step_list
global min_max_servo_steps_list
rad_per_step_list = [0.00054165, 0.00039269, 0.00039269, 0.00056099868]
min_max_servo_steps_list = [[3968, 8000], [3000, 9984], [2100, 8600], [2100, 8600]]


def set_speed_acceleration(agent, motor_number, speed=25, accel=5):
    agent.setAccel(motor_number, accel)
    agent.setSpeed(motor_number, speed)


def set_position(agent, servo_number):
    rad_per_step = rad_per_step_list[servo_number]
    if servo_number==3:
        steps = int(6500 + agent.angles[servo_number]/rad_per_step)
    else:
        steps = int(6000 + agent.angles[servo_number]/rad_per_step)
    # print(steps)

    if steps > min_max_servo_steps_list[servo_number][1]:
        print("exceeded max steps in servo 0\ngoal was %i steps"%steps)
        steps = min_max_servo_steps_list[servo_number][1]
        
    elif steps < min_max_servo_steps_list[servo_number][0]:
        print("exceeded min steps in servo 0\ngoal was %i steps"%steps)
        steps = min_max_servo_steps_list[servo_number][0]

    print("Servo %i location in steps: %i" %(servo_number, steps))
    return steps


def set_destination(coordinates):
    destination = [[coordinates[0][0], coordinates[0][1], coordinates[0][2]]]
    # destination = [[-coordinates[0][0] + 0.15 + 0.421 + 0.337 + 0.105, -coordinates[0][1], -coordinates[0][2] + 0.4 + 1.124 + 0.834 + 0.2596]]
    print("function:", destination)
    return destination


servo = maestro.Controller('COM8') # Setup connection with the correct USB port
arm = tinyik.Actuator(['z', [0.15, 0., 0.4], 'y', [0.421, 0, 1.124], 'y', [0.337, 0, 0.834], 'x', [0.105, 0, 0.2596]])
# arm = tinyik.Actuator(['z', [0.15, 0., 0.4], 'y', [0.421, 0., 1.124]]) # Create the initial full model of the arm

# Set speed and acceleration of the servos
set_speed_acceleration(servo, 0, speed=15)
set_speed_acceleration(servo, 1, speed=15)
set_speed_acceleration(servo, 2, speed=15)
set_speed_acceleration(servo, 3, speed=15)



try:

    destination_coordinates = [[0,1,1]]
    arm.ee = set_destination(destination_coordinates)


    servo.setTarget(0, set_position(arm, 0)) # Base
    servo.setTarget(1, set_position(arm, 1)) # Base Arm
    servo.setTarget(2, set_position(arm, 2)) # Elbow Arm
    servo.setTarget(3, set_position(arm, 3)) # Wrist
    
    servo.close()
except:
    pass









# import maestro
# servo = maestro.Controller('COM8')
# servo.setAccel(1,4)      #set servo 0 acceleration to 4
# servo.setSpeed(1,25)
# y = int(input())
# print(type(y))
# servo.setTarget(1,y)  #set servo to move to center position
# x = servo.getPosition(1) #get the current position of servo 1
# print(x)
# servo.close()