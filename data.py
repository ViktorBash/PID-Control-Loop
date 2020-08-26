"""
Script to collect data in all stages of the flight.
Data that will be collected will be put into a csv file:
    -Location
    -Altitude
    -

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

    # If file does not exist yet, create it
    filename = 'CSV Files/data_points.csv_' + str(csv_number)
    if not os.path.isfile(filename):
        print("NO FILE, making it right now")
        with open("CSV Files/data_points.csv_" + str(csv_number), "w", newline="") as temp_file:
            temp_file.close()

    with open("CSV Files/data_points.csv_" + str(csv_number), "a", newline="") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",")
        csv_writer.writerow(list(data))

        # Dummy code just to make sure writing to CSV file is working
        # for i in range(10):
        #     csv_writer.writerow([i, i + 1, i - 5])


# Testing environment
if __name__ == "__main__":
    write_data_to_csv(["ree", "yee"], 1)
    write_data_to_csv([1, 2, 3, 4, 69, 78], 2)
