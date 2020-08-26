"""
Controller for the barometric pressure sensor (BMP388).

"""

import time
import board
import busio
import adafruit_bmp3xx


# I2C setup
def run_barometer():

    i2c = busio.I2C(board.SCL, board.SDA)
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    bmp.pressure_oversampling = 8
    bmp.temperature_oversampling = 2
    return [bmp.pressure, bmp.temperature]

