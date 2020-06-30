"""
Will hold the code to connect a Raspberry Pi and it's connected components to the PID controller to allow for feedback
between the two.

One PID loop will be for the x axis, and one will be for the y axis. These pid loops will execute independently of
each other, with each one controlling one servo motor.

Control Flow: (Happening continuously)
Get input from gyroscope connected to Pi, convert to degrees for X and Y.
Put degrees into two PID objects for X and Y, get the output necessary (degrees).
Take the output and send it to the thrust vector control system.
"""



