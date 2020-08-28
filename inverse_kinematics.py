#!/usr/bin/env python
# coding: Latin-1

import pybullet as p
import time
import math
from datetime import datetime
import pybullet_data
import numpy as np

# ================================================================================================================================
# |================================ This class builds a pybullet simulation and performs ==========================================|
# |========================================== inverse kinematics for BorrelBot ====================================================|
# ================================================================================================================================


class inverse_kinematics():
  def __init__(self, 
				):
    pass

  
  def initialize_GUI(self,):
    '''
			Args:
			Ιnitializes the GUI and places the robot in place
		'''

    # Start the GUI
    clid = p.connect(p.GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    # Load the floor and the robot
    p.loadURDF("plane.urdf", [0, 0, 0])
    self.robot = p.loadURDF("bb_test.urdf", [0, 0, 0], useFixedBase=1)
    # Index of the endpoint for the invervse kinematics
    self.robotEndEffectorIndex = 5
    self.numJoints = p.getNumJoints(self.robot)
    p.setGravity(0, 0, -9.81)
    

    # Lower limits for null space
    self.ll = [-1.082, -1.179, -0.786, -2.244, -1.122, 0]
    # Upper limits for null space
    self.ul = [1.082, 1.5327, 0.786, 1.4025, 0.9537, 0]
    # Joint ranges for null space
    self.jr = [2*1.082, 1.5327+1.179, 2*0.786, 1.4025+2.244, 0.9537+1.122, 0]
    # Restposes for null space
    self.rp = [0, -0.657, 0.55*math.pi, 0, 0.3, 0]
    # Joint damping coefficents
    self.jd = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

  
    # Set the joints to the parked position of the robot (see set_destination script)
    for i in range(self.numJoints):
      p.resetJointState(self.robot, i, self.rp[i])
    time.sleep(3)

  def get_motor_position_angles(self, destination_coordinates):
    '''
			Args:
        destination_coordinates: target coordinates as seen by the camera
			This function takes the destination coordinates and returns the joint angles under the given constraints
		'''
    self.destination_coordinates = destination_coordinates
    self.initialize_GUI()
    
    # Change from camera's frame of reference to the robot's base frame of reference
    # Get the camera position
    camera_position = [0, 1.4, 1.5]
    # Correct for the camera location
    self.destination_coordinates += np.array(camera_position)
    # Correct to grab the bottle 3cm below the cap
    self.destination_coordinates += np.array([0, 0, -0.3])
    
    # Run the inverse kinematics with the proper constraints
    self.joint_pos_angle = p.calculateInverseKinematics(self.robot,
                                              self.robotEndEffectorIndex, 
                                              self.destination_coordinates,
                                              lowerLimits=self.ll,
                                              upperLimits=self.ul,
                                              jointRanges=self.jr,
                                              restPoses=self.rp
                                              )
                                              
                             
    # Simulate the movement of the motors to the calculated endpoint
    p.setJointMotorControlArray(self.robot, range(self.numJoints), p.POSITION_CONTROL, self.joint_pos_angle)      
    print(self.joint_pos_angle)

    # Give some time for the simulation to remain open for observation.
    # If more time is required change the 900 ---> 9000.
    # Remember to navigate in the GUI you need to press Ctrl + mouse buttons
    for _ in range(900):
      p.stepSimulation()
      time.sleep(1/200)
    
      
    p.disconnect()

    return self.joint_pos_angle

# ================================================================================================================================
# ================================================================================================================================




# ================================================================
# |================== To test inverse kinematics =================|
# ================================================================

# cap_coordinates = [1.1, 0, 0]
# ik = inverse_kinematics()
# pos = ik.get_motor_position_angles(cap_coordinates)

# ================================================================
# ================================================================




# ================================================================
# |========= To test the initial position of the robot ==========|
# ================================================================
# clid = p.connect(p.GUI)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())

# p.loadURDF("sphere2red.urdf", [0, 1.4, 1.5], useFixedBase=1)
# robot = p.loadURDF("bb_test.urdf", [0, 0, 0], useFixedBase=1)
# numJoints = p.getNumJoints(robot)
# rp = [0, -0.657, 0.55*math.pi, 0, 0.3, 0]

# for i in range(numJoints):
#   p.resetJointState(robot, i, rp[i])

# while True:
#   try:
#     a=1
#   except KeyboardInterrupt:
#     exit()
# ================================================================
# ================================================================