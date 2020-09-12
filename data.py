"""
Script to collect data in all stages of the flight.
Data that will be collected will be put into a csv file:
    -Location
    -Altitude
    -to be determined

Need to create an iterable object in order to record data in the CSV format
We will be using a list as the iterable object

First we read csv_number.txt and find the number.
Then we write the number + 1 to the csv_number.txt file
Then we create a CSV file with the number in the name and write whatever we want

This system ensures that all the CSV files have names in ascending order so we
can store data from each flight effortlessly.
"""

import csv
import os


# data should be passed in as a list, csv_number as int
def write_data_to_csv(data, csv_number):
    # If file does not exist yet, create it but write nothing to it
    filename = 'CSV Files/data_points.csv_' + str(csv_number)
    if not os.path.isfile(filename):
        print("NO FILE, making it right now. Also adding header ")
        with open("CSV Files/data_points.csv_" + str(csv_number), "w", newline="") as temp_file:
            csv_writer = csv.writer(temp_file, delimiter=",")
            csv_writer.writerow(
                ["heading", "roll", "pitch", "sys", "gyro", "acceleration", "mag", "x_quat", "y_quat", "z_quat",
                 "w_quat", "x_accel", "y_accel", "z_accel", "x_grav", "y_grav", "z_grav", "cur_time"])
            temp_file.close()

    # The file exists, so we just append to it our data
    with open("CSV Files/data_points.csv_" + str(csv_number), "a", newline="") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",")
        csv_writer.writerow(list(data))
