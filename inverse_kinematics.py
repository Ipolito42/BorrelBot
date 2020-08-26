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

    p.resetSimulation()
    p.loadURDF("plane.urdf", [0, 0, -0.3])
    self.robot = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=1)
    p.resetBasePositionAndOrientation(self.robot, [0, 0, 0], [0, 0, 0, 1])
    self.robotEndEffectorIndex = 6
    self.numJoints = p.getNumJoints(self.robot)

    p.setGravity(0, 0, -9.81)
    self.camera_joint = 3

    #lower limits for null space
    self.ll = [-1.082, -1.179, -0.786,-2.244, -1.122]
    #upper limits for null space
    self.ul = [1.082, 1.5327, 0.786, 1.4025, 0.9537]
    #joint ranges for null space
    self.jr = [5.8, 4, 5.8, 4, 5.8]
    #restposes for null space
    self.rp = [0, 0, 0, 0.5 * math.pi, 0.5 * math.pi, 0.5 * math.pi, 0]
    #joint damping coefficents
    self.jd = [0.1, 0.1, 0.1, 0.1, 0.1]


    
    for i in range(self.numJoints):
      p.resetJointState(self.robot, i, self.rp[i])



  def get_motor_position_angles(self, destination_coordinates):
    
    self.initialize_GUI()
    # Get the camera position

    camera_position = np.array(p.getJointInfo(self.robot, self.camera_joint)[14])
    self.destination_coordinates = destination_coordinates
    # Correct for the camera location
    self.destination_coordinates += camera_position
    # Correct to grab the bottle 3cm below the cap
    self.destination_coordinates -= np.array([0, 0, 0.03])

    self.joint_pos_angle = p.calculateInverseKinematics(self.robot,
                                              self.robotEndEffectorIndex, 
                                              self.destination_coordinates,
                                              lowerLimits=self.ll,
                                              upperLimits=self.ul,
                                              jointRanges=self.jr,
                                              restPoses=self.rp)
                             
    for i in range(self.numJoints):
      p.setJointMotorControl2(bodyIndex = self.robot,
                              jointIndex = i,
                              controlMode = p.POSITION_CONTROL,
                              targetPosition = self.joint_pos_angle[i],
                              targetVelocity = 5

                              )


    # jointPoses = p.calculateInverseKinematics(kukaId,
#                                                   kukaEndEffectorIndex,
#                                                   pos)
#                                                   # lowerLimits=ll,
#                                                   # upperLimits=ul,
#                                                   # jointRanges=jr,
#                                                   # restPoses=rp)


    for _ in range(30):
      p.stepSimulation()
      time.sleep(1./10.)
      
    p.disconnect()

    return self.joint_pos_angle

ik = inverse_kinematics()
pos = ik.get_motor_position_angles([-1,2,1])



# print("asdjnaskdjnasdkjnasdkjnasdjnasdkjnasdkjnasdkjnasdkjnasdkjnaskdn", numJoints)
# while True:
#   try:
#     a=1
#   except KeyboardInterrupt:
#     break
# if (numJoints != 6):
#   exit()

# end_dest = False
# destination_coordinates = [0,2,0.3]


# while not end_dest:

#   p.stepSimulation()
#   # Calculate the destination coordinates from an image
  
#   joint_info = p.getJointInfo(robot, camjoint)
#   joint_axis, joint_parentFramePos, joint_parentFrameOrn  = joint_info[13], joint_info[14], joint_info[15]
#   # destination_coordinates += joint_parentFrameOrn # Not sure which one of the three works correctly

#   print(destination_coordinates)
#   joint_pos = p.calculateInverseKinematics(robot,
#                                             robotEndEffectorIndex, 
#                                             destination_coordinates)
#   for i in range(numJoints):
#     p.setJointMotorControl2(bodyIndex = robot,
#                             jointIndex = i,
#                             controlMode = control_mode,
#                             targetPosition = joint_pos[i]
#                             # , targetVelocity = 1
#                             )

#   #Need end condition
#   if KeyboardInterrupt:
#     exit()



# # #lower limits for null space
# # ll = [-.967, -2, -2.96, 0.19, -2.96]
# # #upper limits for null space
# # ul = [.967, 2, 2.96, 2.29, 2.96]
# # #joint ranges for null space
# # jr = [5.8, 4, 5.8, 4, 5.8]
# # #restposes for null space
# rp = [0, 0, 0, 0.5 * math.pi, 0]
# # #joint damping coefficents
# # jd = [0.1, 0.1, 0.1, 0.1, 0.1]

# for i in range(numJoints):
#   p.resetJointState(kukaId, i, rp[i])

# p.setGravity(0, 0, 0)
# t = 0.
# prevPose = [0, 0, 0]
# prevPose1 = [0, 0, 0]
# hasPrevPose = 0
# useNullSpace = 1

# useOrientation = 1
# #If we set useSimulation=0, it sets the arm pose to be the IK result directly without using dynamic control.
# #This can be used to test the IK result accuracy.
# useSimulation = 1
# useRealTimeSimulation = 0
# ikSolver = 0
# p.setRealTimeSimulation(useRealTimeSimulation)
# #trailDuration is duration (in seconds) after debug lines will be removed automatically
# #use 0 for no-removal
# trailDuration = 15

# i=0
# while 1:
#   i+=1
#   #p.getCameraImage(320,
#   #                 200,
#   #                 flags=p.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX,
#   #                 renderer=p.ER_BULLET_HARDWARE_OPENGL)
#   if (useRealTimeSimulation):
#     dt = datetime.now()
#     t = (dt.second / 60.) * 2. * math.pi
#   else:
#     t = t + 0.01

#   if (useSimulation and useRealTimeSimulation == 0):
#     p.stepSimulation()

#   for i in range(1):
#     pos = [-0.4, 0.2 * math.cos(t), 0. + 0.2 * math.sin(t)]
#     #end effector points down, not up (in case useOrientation==1)
#     orn = p.getQuaternionFromEuler([0, -math.pi, 0])

#     if (useNullSpace == 1):
#       if (useOrientation == 1):
        # jointPoses = p.calculateInverseKinematics(kukaId, kukaEndEffectorIndex, pos)#, orn, ll, ul,
#                                                   # jr, rp)
#       else:
#         jointPoses = p.calculateInverseKinematics(kukaId,
#                                                   kukaEndEffectorIndex,
#                                                   pos)
#                                                   # lowerLimits=ll,
#                                                   # upperLimits=ul,
#                                                   # jointRanges=jr,
#                                                   # restPoses=rp)
#     else:
#       if (useOrientation == 1):
#         jointPoses = p.calculateInverseKinematics(kukaId,
#                                                   kukaEndEffectorIndex,
#                                                   pos,
#                                                   orn,
#                                                   # jointDamping=jd,
#                                                   solver=ikSolver,
#                                                   maxNumIterations=100,
#                                                   residualThreshold=.01)
#       else:
#         jointPoses = p.calculateInverseKinematics(kukaId,
#                                                   kukaEndEffectorIndex,
#                                                   pos,
#                                                   solver=ikSolver)

#     if (useSimulation):
#       for i in range(numJoints):
#         p.setJointMotorControl2(bodyIndex=kukaId,
#                                 jointIndex=i,
#                                 controlMode=p.POSITION_CONTROL,
#                                 targetPosition=jointPoses[i],
#                                 targetVelocity=0,
#                                 force=500,
#                                 positionGain=0.03,
#                                 velocityGain=1)
#     else:
#       #reset the joint state (ignoring all dynamics, not recommended to use during simulation)
#       for i in range(numJoints):
#         p.resetJointState(kukaId, i, jointPoses[i])

#   ls = p.getLinkState(kukaId, kukaEndEffectorIndex)
#   if (hasPrevPose):
#     p.addUserDebugLine(prevPose, pos, [0, 0, 0.3], 1, trailDuration)
#     p.addUserDebugLine(prevPose1, ls[4], [1, 0, 0], 1, trailDuration)
#   prevPose = pos
#   prevPose1 = ls[4]
#   hasPrevPose = 1
