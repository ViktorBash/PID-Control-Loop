"""
This script plots data from a CSV file and saves all the figures as PDFs and PNGs.

TODO: Change x axis (time) to show seconds rounded

HOW TO CUSTOMIZE GRAPHS:

For a custom color when plotting data:
    plt.plot(data["timestamp"], data[key], 'c')
The "c" is a color, there are a plethora of color codes here:
https://matplotlib.org/3.1.0/gallery/color/named_colors.html

For a custom font for any text:
    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
    plt.title("Graph of " + key + " for CSV data " + csv_file_number, fontdict=font)
Use fontdict=. This can be done for title, labels, etc
"""


# matplotlib for plotting, pandas for working with the CSV file
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style


# Get correct CSV file from user
csv_file_number = input("Enter the number of the csv file you want to analyze: ")
data = pd.read_csv("../CSV Files/data_points_" + str(csv_file_number) + ".csv")

# This dict will help to create unique labels for the graphs
labels = {"heading": "Heading",
          "roll": "Roll",
          "pitch": "Pitch",
          "x_quat": "X Quaternion",
          "y_quat": "Y Quaternion",
          "z_quat": "Z Quaternion",
          "w_quat": "W Quaternion",
          "x_accel": "X Acceleration",
          "y_accel": "Y Acceleration",
          "z_accel": "Z Acceleration",
          "x_grav": "X Gravity",
          "y_grav": "Y Gravity",
          "z_grav": "Z Gravity",
          "pressure": "Pressure",
          "temperature": "Temperature (C°)",
          "altitude": "Altitude",
          }

# Matplotlib plot style
style.use("ggplot")

# Iterate through the labels dict to plot everything in the dict (only 2 variables: time and y)
for key in labels:
    cur_plot = plt.figure(list(labels.keys()).index(key))
    plt.plot(data["timestamp"], data[key])
    plt.xlabel("Time")
    plt.title("Graph of " + key + " for CSV data " + csv_file_number)
    plt.ylabel(labels[key])
    plt.savefig(key + "_data_" + csv_file_number + ".png")
    plt.savefig(key + "_data_" + csv_file_number + ".pdf")


# Plot all 3 euler angles together
cur_plot = plt.figure(len(labels) + 1)
plt.plot(data["timestamp"], data['heading'], label="Heading")
plt.plot(data["timestamp"], data['roll'], label="Roll")
plt.plot(data["timestamp"], data['pitch'], label="Pitch")
plt.title("3 Euler Angles")
plt.legend()
plt.show()


# # Plot all 4 quaternions together
cur_plot = plt.figure(len(labels) + 2)
plt.plot(data["timestamp"], data['x_quat'], label="X Quat")
plt.plot(data["timestamp"], data['y_quat'], label="Y Quat")
plt.plot(data["timestamp"], data['z_quat'], label="Z Quat")
plt.plot(data["timestamp"], data['w_quat'], label="W Quat")
plt.title("4 Quaternions")
plt.legend()
plt.show()
plt.savefig("all_quat_data_" + csv_file_number + ".png")
plt.savefig("all_quat_data_" + csv_file_number + ".pdf")


# # Plot all accelerations together
cur_plot = plt.figure(len(labels) + 3)
plt.plot(data["timestamp"], data['x_accel'], label="X Accel")
plt.plot(data["timestamp"], data['y_accel'], label="Y Accel")
plt.plot(data["timestamp"], data['z_accel'], label="Z Accel")
plt.title("3 Accelerations")
plt.legend()
plt.show()
plt.savefig("all_accel_data_" + csv_file_number + ".png")
plt.savefig("all_accel_data_" + csv_file_number + ".pdf")


# Plot all gravities together
cur_plot = plt.figure(len(labels) + 4)
plt.plot(data["timestamp"], data['x_grav'], label="X Grav")
plt.plot(data["timestamp"], data['y_grav'], label="Y Grav")
plt.plot(data["timestamp"], data['z_grav'], label="Z Grav")
plt.title("4 Gravities")
plt.legend()
plt.show()
plt.savefig("all_gravity_data_" + csv_file_number + ".png")
plt.savefig("all_gravity_data_" + csv_file_number + ".pdf")
