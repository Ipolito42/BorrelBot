# BorrelBot
BorrelBot is a mobile robotic arm to fetch beers. This project is part of the Robotics course in LIACS, Leiden University.

## Requirements
1) The Maestro library for servo control via python scripts.
https://github.com/FRC4564/Maestro

2) The OpenCV library for image recognition.
https://opencv.org/

3) The tinyik library for the Inverse Kinematics calculations.
https://github.com/lanius/tinyik

and the standard python package libraries.

## File Index

**maestro.py** : The necessary functions to work with servos
**camera_code.py** : Script for image recognition i.e. to identiy bottle caps
**set_destination.py** : Script to calculate servo steps based on inverse kinematics
**tryout.py** : Script for testing
**servo_positions.txt** : Contains info for the servo characteristics
