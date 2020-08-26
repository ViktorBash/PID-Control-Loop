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

import time
import datetime
from imu_controller import run_imu_controller
from barometric_pressure_sensor_controller import run_barometer
from data import write_data_to_csv


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
SLEEP = 0.01
ACCEL_LEVEL = 1  # Acceleration level
DEPLOY_CHUTE_ALTITUDE = 50
STOPPED_ACCELERATION = 0.05

acceleration = 0  # Get acceleration from IMU


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
    else:
        imu_data_dict = run_imu_controller()
        barometer_data_dict = run_barometer()

        print(str(imu_data_dict))
        print(str(barometer_data_dict))

        write_data_to_csv([str(datetime.datetime.now())], csv_number)
        write_data_to_csv([str(imu_data_dict)], csv_number)
        write_data_to_csv([str(barometer_data_dict)], csv_number)

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
    else:
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
    else:
        time.sleep(SLEEP)

while ballistic_descent:
    para_altitude = 10  # Get altitude from barometer
    if para_altitude <= DEPLOY_CHUTE_ALTITUDE:
        ballistic_descent = False
        chute_descent = True
        break
    else:
        time.sleep(WAIT)

while chute_descent:
    acceleration = acceleration  # Get acceleration from IMU
    if acceleration <= STOPPED_ACCELERATION:
        time.sleep(10)
        if acceleration <= STOPPED_ACCELERATION:
            chute_descent = False
            landing = True
            break
    else:
        acceleration -= 1  # Remove
        time.sleep(WAIT)

while landing:
    landing = False  # Remove

