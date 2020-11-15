"""
Main script which calls other scripts/functions during the rocket's life.

1. Ground Idle -
2. Power Flight - detected when liftoff
    Acceleration threshold to measure whether we have taken off. We are above the threshold for 0.1 seconds is also
    another prerequisite.
3. Unpowered Flight - burnout
    If accelerator is less than a certain amount of m/seconds squared. For greater than 0.1 seconds
4. Ballistic Descent - apogee
    To detect apogee: we compare two different readings that are one second apart to see if we are ascending or
    descending.
5. Chute Descent - pyro fire
    If we fired the parachutes. If we are at a certain altitude fire the chutes and switch to the chute state.
6. Landing - if acceleration is almost or near zero for more than 10 seconds.

Guidance Navigation and Control

More Directions:
Will hold the code to connect a Raspberry Pi and it's connected components to the PID controller to allow for feedback
between the two.

One PID loop will be for the x axis, and one will be for the y axis. These pid loops will execute independently of
each other, with each one controlling one servo motor.

Control Flow: (Happening continuously)
Get input from gyroscope connected to Pi, convert to degrees for X and Y.
Put degrees into two PID objects for X and Y, get the output necessary (degrees).
Take the output and send it to the thrust vector control system.

"""


# IMPORT STATEMENTS
import board
import busio
import adafruit_bmp3xx

from simple_pid import PID

from data import write_data_to_csv

import sys
import logging
from Adafruit_BNO055 import BNO055

import time
from datetime import datetime

import RPi.GPIO as GPIO

import servo_control


# Get the current csv_number and update the csv_number to write to the correct filename for no data loss
def find_update_csv_number():
    with open("csv_number.txt", "r") as file:  # Get the number
        number = file.readlines()
        number = int(number[0])
        file.close()

    with open("csv_number.txt", "w") as file: # Update it so we won't be written over
        new_number = number + 1
        file.write(str(new_number))
        file.close()
    return number  # The number we will use to write data to
csv_number = find_update_csv_number()  # CSV number that will be used later to write to csv


# STAGES OF FLIGHT
ground_idle = True
power_flight = False
unpowered_flight = False
ballistic_descent = False
chute_descent = False
landing = False


# Time: seconds, acceleration/altitude: meters
WAIT = 0.5
SLEEP = 0.01
ACCEL_LEVEL = 1  # Acceleration level
DEPLOY_CHUTE_ALTITUDE = 50
STOPPED_ACCELERATION = 0.05
CHUTE_DESCENT_WAIT = 0.5  # How much to wait until we check the acceleration again to transition to chute descent

acceleration = 0  # Get acceleration from IMU


# CONFIGURATION FOR IMU CONTROLLER

# Raspberry Pi configuration with serial UART
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Calibrating the IMU
print("CALIBRATION VALUES BEFORE (sys, gyro, accel, mag): ")
print(bno.get_calibration_status())

bno.set_calibration(bno.get_calibration())


# CONFIGURATION OF BAROMETRIC CONTROLLER
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2


# IMU Dict
imu_data = {
            # uncommented is currently unused but may be valuable later
            "heading": None,
            "roll": None,
            "pitch": None,
            "sys": None,
            "gyro": None,
            "acceleration": None,
            "mag": None,
            "x_quaternion": None,
            "y_quaternion": None,
            "z_quaternion": None,
            "w_quaternion": None,
            "x_accelerometer": None,
            "y_accelerometer": None,
            "z_accelerometer": None,
            'x_gravity': None,
            'y_gravity': None,
            'z_gravity': None,
        }


# For comparing acceleration
other_variables = {
    "average_acceleration": 0,
    "past_average_acceleration": 0
}


# Barometric dict
barometric_dict = {
        "pressure": None,
        "temperature": None,
        "altitude": None,
}


# Function to get average acceleration
def get_average_acceleration():
    try:
        average_acceleration = imu_data['x_accelerometer'] + imu_data['y_accelerometer'] + imu_data['z_accelerometer']
        average_acceleration = average_acceleration / 3
        other_variables['past_average_acceleration'] = other_variables['average_acceleration']
        other_variables['average_acceleration'] = average_acceleration
    except Exception as e:
        pass
    return


# PID loop setup
proportional = 0.0206310292526927
integral = 0.000965837060148333
derivative = 0.108213442401603
setpoint = 0

pid_x = PID(proportional, integral, derivative, setpoint=setpoint)
pid_y = PID(proportional, integral, derivative, setpoint=setpoint)


# Things to change:
#     Use of heading, pitch, roll
#     Servo1 and servo2
#     PID and setpoint values
# Function for interacting with the PID loop
def pid_interact_x():
    error_x = imu_data['pitch'] - setpoint
    output_x = pid_x(error_x)
    print(f"VALUES, HEADING: {imu_data['heading']}, ROLL: {imu_data['roll']}, PITCH: {imu_data['pitch']}")
    print(f"OUTPUT_X: {output_x}")
    servo_control.move_servo_1(output_x)


def pid_interact_y():
    error_y = imu_data['roll'] - setpoint
    output_y = pid_y(error_y)
    print(f"OUTPUT_Y: {output_y}")
    servo_control.move_servo_2(output_y)


# Setup for the button that will arm the rocket
# button_pin = 13
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# STAGES OF FLIGHT
# Loop before we enter power flight (ground idling at this point)

buzzer_pin = 17  # For BCM
button_pin = 27  # For BCM (13=27)

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while ground_idle:
    # Run the buzzer (set it up, buz, turn off, destroy, then repeat)
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.cleanup(buzzer_pin)
    time.sleep(1)

    # Check if the button has been pressed, if it has go to the next stage
    if GPIO.input(button_pin) == GPIO.HIGH:
        power_flight = True
        ground_idle = False
        print("BUTTON PRESSED - GOING TO POWERED FLIGHT")

# Cleanup the button and setup the buzzer to play a loud sound continuously now
GPIO.cleanup(button_pin)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.LOW)

while power_flight:
    # GPIO.output(buzzer_pin, GPIO.LOW)
    get_average_acceleration()

    # Check if acceleration has fallen more than the accel level
    if other_variables['past_average_acceleration'] - other_variables['average_acceleration'] >= ACCEL_LEVEL:

        print("POWER FLIGHT FIRST CHECK SUCCESS, ACCEL FALLEN")
        # Wait, then get acceleration and check if it changed again
        time.sleep(WAIT)
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        get_average_acceleration()

        # Check again after waiting to make sure it's not a fluke and that the acceleration has changed
        if other_variables['past_average_acceleration'] - other_variables['average_acceleration'] >= ACCEL_LEVEL:
            power_flight = False
            unpowered_flight = True
            print("MOVING TO UNPOWERED FLIGHT FROM POWER FLIGHT")
            break
        else:
            continue
    else:  # We did not trigger next stage, read/write data
        imu_data['heading'], imu_data['roll'], imu_data['pitch'] = bno.read_euler()
        imu_data['sys'], imu_data['gyro'], imu_data['acceleration'], imu_data['mag'] = bno.get_calibration_status()
        imu_data['x_quaternion'], imu_data['y_quaternion'], imu_data['z_quaternion'], imu_data['w_quaternion'] = bno.read_quaternion()
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        imu_data['x_gravity'], imu_data['y_gravity'], imu_data['z_gravity'] = bno.read_gravity()
        barometric_dict = {
            "pressure": bmp.pressure,
            "temperature": bmp.temperature,
            "altitude": bmp.altitude,
        }

        # Get timestamp for CSV file
        timestamp = datetime.now()

        # Write all the data to the CSV file
        write_data_to_csv([
            timestamp,
            imu_data['heading'],
            imu_data['roll'],
            imu_data['pitch'],
            imu_data['sys'],
            imu_data['gyro'],
            imu_data['acceleration'],
            imu_data['mag'],
            imu_data['x_quaternion'],
            imu_data['y_quaternion'],
            imu_data['z_quaternion'],
            imu_data['w_quaternion'],
            imu_data['x_accelerometer'],
            imu_data['y_accelerometer'],
            imu_data['z_accelerometer'],
            imu_data['x_gravity'],
            imu_data['y_gravity'],
            imu_data['z_gravity'],
            barometric_dict['pressure'],
            barometric_dict['temperature'],
            barometric_dict['altitude'],
        ], csv_number)

        # Code to test out the servo
        # servo_control.move_servo_2(25)
        # servo_control.move_servo_1(-25)
        pid_interact_x()
        pid_interact_y()


while unpowered_flight:
    altitude = 100  # Get altitude from barometer
    cur_altitude = 90  # Get altitude from barometer
    if cur_altitude < altitude:  # We are falling now if true
        unpowered_flight = False
        ballistic_descent = True
        print("MOVING TO BALLISTIC DESCENT FROM UNPOWERED FLIGHT")
        break
    else:  # We did not trigger next stage, read/write data
        imu_data['heading'], imu_data['roll'], imu_data['pitch'] = bno.read_euler()
        imu_data['sys'], imu_data['gyro'], imu_data['acceleration'], imu_data['mag'] = bno.get_calibration_status()
        imu_data['x_quaternion'], imu_data['y_quaternion'], imu_data['z_quaternion'], imu_data[
            'w_quaternion'] = bno.read_quaternion()
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        imu_data['x_gravity'], imu_data['y_gravity'], imu_data['z_gravity'] = bno.read_gravity()
        barometric_dict = {
            "pressure": bmp.pressure,
            "temperature": bmp.temperature,
            "altitude": bmp.altitude,
        }

        # Get timestamp for CSV file
        timestamp = datetime.now()

        # Write all the data to the CSV file
        write_data_to_csv([
            timestamp,
            imu_data['heading'],
            imu_data['roll'],
            imu_data['pitch'],
            imu_data['sys'],
            imu_data['gyro'],
            imu_data['acceleration'],
            imu_data['mag'],
            imu_data['x_quaternion'],
            imu_data['y_quaternion'],
            imu_data['z_quaternion'],
            imu_data['w_quaternion'],
            imu_data['x_accelerometer'],
            imu_data['y_accelerometer'],
            imu_data['z_accelerometer'],
            imu_data['x_gravity'],
            imu_data['y_gravity'],
            imu_data['z_gravity'],
            barometric_dict['pressure'],
            barometric_dict['temperature'],
            barometric_dict['altitude'],
        ], csv_number)
        pid_interact_x()
        pid_interact_y()

while ballistic_descent:
    para_altitude = 10  # Get altitude from barometer
    if para_altitude <= DEPLOY_CHUTE_ALTITUDE:
        ballistic_descent = False
        chute_descent = True
        print("MOVING TO CHUTE DESCENT FROM BALLISTIC DESCENT")
        break
    else:  # We did not trigger next stage, read/write data
        imu_data['heading'], imu_data['roll'], imu_data['pitch'] = bno.read_euler()
        imu_data['sys'], imu_data['gyro'], imu_data['acceleration'], imu_data['mag'] = bno.get_calibration_status()
        imu_data['x_quaternion'], imu_data['y_quaternion'], imu_data['z_quaternion'], imu_data[
            'w_quaternion'] = bno.read_quaternion()
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        imu_data['x_gravity'], imu_data['y_gravity'], imu_data['z_gravity'] = bno.read_gravity()
        barometric_dict = {
            "pressure": bmp.pressure,
            "temperature": bmp.temperature,
            "altitude": bmp.altitude,
        }

        # Get timestamp for CSV file
        timestamp = datetime.now()

        # Write all the data to the CSV file
        write_data_to_csv([
            timestamp,
            imu_data['heading'],
            imu_data['roll'],
            imu_data['pitch'],
            imu_data['sys'],
            imu_data['gyro'],
            imu_data['acceleration'],
            imu_data['mag'],
            imu_data['x_quaternion'],
            imu_data['y_quaternion'],
            imu_data['z_quaternion'],
            imu_data['w_quaternion'],
            imu_data['x_accelerometer'],
            imu_data['y_accelerometer'],
            imu_data['z_accelerometer'],
            imu_data['x_gravity'],
            imu_data['y_gravity'],
            imu_data['z_gravity'],
            barometric_dict['pressure'],
            barometric_dict['temperature'],
            barometric_dict['altitude'],
        ], csv_number)
        pid_interact_x()
        pid_interact_y()

while chute_descent:
    # Get average acceleration from x,y and z accel from IMU
    acceleration = (imu_data['x_accelerometer'] + imu_data['y_accelerometer'] + imu_data['z_accelerometer'])/3
    if acceleration <= STOPPED_ACCELERATION:
        # TODO: Get acceleration level again before comparing
        time.sleep(CHUTE_DESCENT_WAIT)
        if acceleration <= STOPPED_ACCELERATION:
            chute_descent = False
            landing = True
            print("MOVING TO LANDING :D")
            break
    else:  # We did not trigger next stage, read/write data
        imu_data['heading'], imu_data['roll'], imu_data['pitch'] = bno.read_euler()
        imu_data['sys'], imu_data['gyro'], imu_data['acceleration'], imu_data['mag'] = bno.get_calibration_status()
        imu_data['x_quaternion'], imu_data['y_quaternion'], imu_data['z_quaternion'], imu_data[
            'w_quaternion'] = bno.read_quaternion()
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        imu_data['x_gravity'], imu_data['y_gravity'], imu_data['z_gravity'] = bno.read_gravity()
        barometric_dict = {
            "pressure": bmp.pressure,
            "temperature": bmp.temperature,
            "altitude": bmp.altitude,
        }

        # Get timestamp for CSV file
        timestamp = datetime.now()

        # Write all the data to the CSV file
        write_data_to_csv([
            timestamp,
            imu_data['heading'],
            imu_data['roll'],
            imu_data['pitch'],
            imu_data['sys'],
            imu_data['gyro'],
            imu_data['acceleration'],
            imu_data['mag'],
            imu_data['x_quaternion'],
            imu_data['y_quaternion'],
            imu_data['z_quaternion'],
            imu_data['w_quaternion'],
            imu_data['x_accelerometer'],
            imu_data['y_accelerometer'],
            imu_data['z_accelerometer'],
            imu_data['x_gravity'],
            imu_data['y_gravity'],
            imu_data['z_gravity'],
            barometric_dict['pressure'],
            barometric_dict['temperature'],
            barometric_dict['altitude'],
        ], csv_number)
        pid_interact_x()
        pid_interact_y()

while landing:
    landing = False  # Remove
    # Setting the servos back to 0 degrees
    servo_control.move_servo_2(0)
    servo_control.move_servo_1(0)
