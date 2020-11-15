"""
Two functions to control the two servo motors for the project
"""

from gpiozero import Servo, AngularServo
from gpiozero.tools import sin_values
import time
from time import sleep

# Setup servo 1
# servo1 = Servo(12)
servo1 = AngularServo(12, min_angle=-90, max_angle=90)
# Setup servo 2
# servo2 = Servo(19)
servo2 = AngularServo(19, min_angle=-90, max_angle=90)

# How much the servo will be able to move
top_limit = 15
bottom_limit = -15


def move_servo_1(angle):
    if angle > top_limit:
        angle = top_limit
    if angle < bottom_limit:
        angle = bottom_limit
    servo1.angle = angle


def move_servo_2(angle):
    if angle > top_limit:
        angle = top_limit
    if angle < bottom_limit:
        angle = bottom_limit
    servo2.angle = angle


# For testing purposes
if __name__ == "__main__":
    while True:
        move_servo_1(20)
        move_servo_2(-20)
        time.sleep(1)
        move_servo_1(-20)
        move_servo_2(20)
        time.sleep(1)
