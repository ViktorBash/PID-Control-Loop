"""
Will control the BNO055 IMU made for the Raspberry Pi
"""

import adafruit_bno055
from busio import I2C
from board import SDA, SCL
from time import sleep

i2c = I2C(SCL, SDA)
sensor = adafruit_bno055.BNO055(i2c)
while True:
    print(sensor.temperature)
    print(sensor.euler)
    print(sensor.gravity)
    sleep(05.5)
