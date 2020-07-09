"""
Script to collect data in all stages of the flight.
Data that will be collected:
    -Location
    -Altitude
    -

Need to create an iterable object in order to record data in the CSV format
We will be using a list as the iterable object
"""

import csv

with open("csv_number.txt", "r") as file:
    number = file.readlines()
    number = int(number[0])
    file.close()

    # number_to_write = [str(number)]
with open("csv_number.txt", "w") as file:
    new_number = number + 1
    file.write(str(new_number))
    file.close()

with open(f"CSV Files/data_points.csv_{number}", "w", newline="") as new_file:
    csv_writer = csv.writer(new_file, delimiter=",")

    # Dummy code just to make sure writing to CSV file is working
    for i in range(10):
        csv_writer.writerow([i, i + 1, i - 5])

