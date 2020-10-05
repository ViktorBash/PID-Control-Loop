"""
Script to that has a function to write data to a CSV file.
write_data_to_csv() is called with a csv number and either writes to a new file or appends to an existing one the data
it is given. It then closes. This ensures that if the rocket breaks at some point that all the data leading up to that
point will still be written to the CSV file.
"""

import csv
import os


# data should be passed in as a list, csv_number as int
def write_data_to_csv(data, csv_number):
    # If file does not exist yet, create it
    filename = 'CSV Files/data_points_' + str(csv_number) + '.csv'
    if not os.path.isfile(filename):
        print("NO FILE, making it right now. Also adding header ")
        # The file doesn't exist so we make it and write to it + add a header at the top
        with open("CSV Files/data_points_" + str(csv_number) + ".csv", "w", newline="") as temp_file:
            csv_writer = csv.writer(temp_file, delimiter=",")
            csv_writer.writerow(
                ["timestamp", "heading", "roll", "pitch", "sys", "gyro", "acceleration", "mag", "x_quat", "y_quat",
                 "z_quat", "w_quat", "x_accel", "y_accel", "z_accel", "x_grav", "y_grav", "z_grav", "pressure",
                 "temperature", "altitude"
                 ])
            temp_file.close()

    # The file exists, so we just append to it our data
    with open("CSV Files/data_points_" + str(csv_number) + ".csv", "a", newline="") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",")
        csv_writer.writerow(data)
