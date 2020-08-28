#!/usr/bin/env python
# coding: Latin-1

import pybullet as p
import time
import math
from datetime import datetime
import pybullet_data
import numpy as np




class inverse_kinematics():
  def __init__(self, 
				):
    pass

  
  def initialize_GUI(self):
    clid = p.connect(p.GUI)
    
    # if (clid < 0):
    #   p.connect(p.GUI)
    #   #p.connect(p.SHARED_MEMORY_GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # p.resetSimulation()
    p.loadURDF("plane.urdf", [0, 0, 0])
    self.robot = p.loadURDF("bb_test.urdf", [0, 0, 0], useFixedBase=1)
    # p.resetBasePositionAndOrientation(self.robot, [0, 0, 0], [0, 0, 0, 1])
    self.robotEndEffectorIndex = 5
    self.numJoints = p.getNumJoints(self.robot)
    print(self.numJoints)

    p.setGravity(0, 0, -9.81)
    self.camera_joint = 3

    #lower limits for null space
    self.ll = [-1.082, -1.179, -0.786, -2.244, -1.122, 0]
    #upper limits for null space
    self.ul = [1.082, 1.5327, 0.786, 1.4025, 0.9537, 0]
    #joint ranges for null space
    self.jr = [2*1.082, 1.5327+1.179, 2*0.786, 1.4025+2.244, 0.9537+1.122, 0]
    #restposes for null space
    self.rp = [0, -0.657, 0.55*math.pi, 0, 0.3, 0]
    #joint damping coefficents
    self.jd = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

  
    
    for i in range(self.numJoints):
      p.resetJointState(self.robot, i, self.rp[i])
    time.sleep(3)

  def get_motor_position_angles(self, destination_coordinates):
    
    self.initialize_GUI()
    # Get the camera position
    print(destination_coordinates)
    

    # camera_position = np.array(p.getJointInfo(self.robot, self.camera_joint)[14])
    camera_position = [0, 1.4, 1.5]
    self.destination_coordinates = destination_coordinates
    print("dest coord", destination_coordinates)
    # Correct for the camera location
    self.destination_coordinates += np.array(camera_position)
    print(self.destination_coordinates)
    print("cam", camera_position)
    # Correct to grab the bottle 3cm below the cap
    # self.destination_coordinates += np.array([0, 0, -0.03])
    # p.loadURDF("sphere2red.urdf", self.destination_coordinates, useFixedBase=1)
    # print("cam pos", camera_position)
    # print("dest coord", destination_coordinates)
    

    self.joint_pos_angle = p.calculateInverseKinematics(self.robot,
                                              self.robotEndEffectorIndex, 
                                              self.destination_coordinates,
                                              lowerLimits=self.ll,
                                              upperLimits=self.ul,
                                              jointRanges=self.jr,
                                              restPoses=self.rp
                                              )
                                              
                             
    # for i in range(self.numJoints-1):
    #   p.setJointMotorControl2(bodyIndex = self.robot,
    #                           jointIndex = i,
    #                           controlMode = p.POSITION_CONTROL,
    #                           targetPosition = self.joint_pos_angle[i],
    #                           targetVelocity = 5
    #                           )

    p.setJointMotorControlArray(self.robot, range(self.numJoints), p.POSITION_CONTROL, self.joint_pos_angle)      
    print(self.joint_pos_angle)

    for _ in range(900):
      p.stepSimulation()
      time.sleep(1/200)
    
      
    p.disconnect()

    return self.joint_pos_angle


# # For trial
# from set_destination import set_destination as sd
# ik = inverse_kinematics()
# pos = ik.get_motor_position_angles([1.1, 0, 0])
# kwstras = sd()
# kwstras.main(pos)

# clid = p.connect(p.GUI)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())

# p.loadURDF("sphere2red.urdf", [0, 1.4, 1.5], useFixedBase=1)
# robot = p.loadURDF("bb_test.urdf", [0, 0, 0], useFixedBase=1)
# numJoints = p.getNumJoints(robot)
# rp = [0, -0.657, 0.55*math.pi, 0, 0.3, 0]
# #joint damping coefficents
# jd = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

  
    
# for i in range(numJoints):
#   p.resetJointState(robot, i, rp[i])
# time.sleep(3)
# while True:
#   try:
#     a=1
#   except KeyboardInterrupt:
#     exit()
