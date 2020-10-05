"""
Two functions to control the two servo motors for the project
"""

from gpiozero import Servo
from gpiozero.tools import sin_values
import time
from time import sleep

# Setup servo 1
servo1 = Servo(12)
# Setup servo 2
servo2 = Servo(19)


def move_servo_1(angle):
    servo1.angle = angle


def move_servo_2(angle):
    servo2.angle = angle


# For testing purposes
if __name__ == "__main__":
    pass
