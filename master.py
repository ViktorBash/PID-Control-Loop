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

TODO: Start using acceleration and other data to change between stages
"""

import datetime
from barometric_pressure_sensor_controller import run_barometer
from data import write_data_to_csv
import sys
import logging
from Adafruit_BNO055 import BNO055
import time


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


csv_number = find_update_csv_number()

ground_idle = True
power_flight = False
unpowered_flight = False
ballistic_descent = False
chute_descent = False
landing = False


# Time: seconds, acceleration/altitude: meters
WAIT = 0.5
SLEEP = 0.5
ACCEL_LEVEL = 1  # Acceleration level
DEPLOY_CHUTE_ALTITUDE = 50
STOPPED_ACCELERATION = 0.05

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


# STAGES OF FLIGHT

# Loop before we enter power flight (ground idling at this point)
while ground_idle:
    if acceleration >= ACCEL_LEVEL:  # Check acceleration
        time.sleep(WAIT)
        if acceleration >= ACCEL_LEVEL:  # Check again after waiting to make sure it's not a fluke
            ground_idle = False
            power_flight = True
            break
        else:
            time.sleep(SLEEP)
            continue
    else:  # We did not trigger next stage, read/write data
        # print("blank")
        # heading, roll, pitch = bno.read_euler()
        imu_data['heading'], imu_data['roll'], imu_data['pitch'] = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        # sys, gyro, acceleration, mag = bno.get_calibration_status()
        imu_data['sys'], imu_data['gyro'], imu_data['acceleration'], imu_data['mag'] = bno.get_calibration_status()
        # OTHER USEFUL VALUES
        # Orientation as a quaternion:
        # x_quaternion, y_quaternion, z_quaternion, w_quaternion = bno.read_quaternion()
        imu_data['x_quaternion'], imu_data['y_quaternion'], imu_data['z_quaternion'], imu_data['w_quaternion'] = bno.read_quaternion()

        # Sensor temperature in degrees Celsius:
        # temp_c = bno.read_temp()
        # Magnetometer data (in micro-Teslas):
        # x,y,z = bno.read_magnetometer()
        # Gyroscope data (in degrees per second):
        # x,y,z = bno.read_gyroscope()
        # Accelerometer data (in meters per second squared):
        # x_accelerometer, y_accelerometer, z_accelerometer = bno.read_accelerometer()
        imu_data['x_accelerometer'], imu_data['y_accelerometer'], imu_data['z_accelerometer'] = bno.read_accelerometer()
        # Linear acceleration data (i.e. acceleration from movement, not gravity returned in meters per second squared):
        # x,y,z = bno.read_linear_acceleration()
        # Gravity acceleration data (i.e. acceleration just from gravity returned in meters per second squared):
        imu_data['x_gravity'], imu_data['y_gravity'], imu_data['z_gravity'] = bno.read_gravity()

        # imu_data = {
        #     # uncommented is currently unused but may be valuable later
        #     "heading": heading,
        #     "roll": roll,
        #     "pitch": pitch,
        #     "sys": sys,
        #     "gyro": gyro,
        #     "acceleration": acceleration,
        #     "mag": mag,
        #     "x_quaternion": x_quaternion,
        #     "y_quaternion": y_quaternion,
        #     "z_quaternion": z_quaternion,
        #     "w_quaternion": w_quaternion,
        #     "x_accelerometer": x_accelerometer,
        #     "y_accelerometer": y_accelerometer,
        #     "z_accelerometer": z_accelerometer,
        # }

        barometric_data = run_barometer()
        print(barometric_data)
        print(imu_data)
        time.sleep(SLEEP)


while power_flight:
    if acceleration < ACCEL_LEVEL:  # Check acceleration
        time.sleep(WAIT)
        if acceleration < ACCEL_LEVEL:  # Check again after waiting to make sure it's not a fluke
            power_flight = False
            unpowered_flight = True
            break
        else:
            time.sleep(SLEEP)
            continue
    else: # We did not trigger next stage, read/write data
        acceleration -= 1  # Remove later
        time.sleep(SLEEP)

while unpowered_flight:
    altitude = 100  # Get altitude from barometer
    time.sleep(WAIT)
    cur_altitude = 90  # Get altitude from barometer
    if cur_altitude < altitude:  # We are falling now if true
        unpowered_flight = False
        ballistic_descent = True
        break
    else: # We did not trigger next stage, read/write data
        time.sleep(SLEEP)

while ballistic_descent:
    para_altitude = 10  # Get altitude from barometer
    if para_altitude <= DEPLOY_CHUTE_ALTITUDE:
        ballistic_descent = False
        chute_descent = True
        break
    else: # We did not trigger next stage, read/write data
        time.sleep(WAIT)

while chute_descent:
    acceleration = acceleration  # Get acceleration from IMU
    if acceleration <= STOPPED_ACCELERATION:
        time.sleep(10)
        if acceleration <= STOPPED_ACCELERATION:
            chute_descent = False
            landing = True
            break
    else:  # We did not trigger next stage, read/write data
        acceleration -= 1  # Remove
        time.sleep(WAIT)

while landing:
    landing = False  # Remove

