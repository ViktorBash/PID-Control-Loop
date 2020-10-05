"""
This script will plot data from the CSV files and save it as PNG using matplotlib.

TODO:
    -Plot x accel, y accel, z accel
    -Plot x grav, y grav, z grav
    - Change font
    -Change window title
    -Change color
    -Change x axis (time) to show seconds rounded
"""

# matplotlib for plotting, pandas for working with the CSV file, numpy later on for the line of best fit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import datetime
# Get correct CSV file from user
csv_file_number = input("Enter the number of the csv file you want to analyze: ")
data = pd.read_csv("../CSV Files/data_points_" + str(csv_file_number) + ".csv")

# Units will be added and each ting that will be plotted will also have the label ere to get
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
