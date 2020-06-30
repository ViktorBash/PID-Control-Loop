"""
PID loop in Python (Proportional, Integral Derivative)
"""

import time


class PID:
    """
    PID Controller
    Takes in P, I and D parameters and current_time to create PID object. Continuously provide feedback through
    the update() function and access PID.output for the output.
    """

    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):
        """Initialize PID object """
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00

        if current_time is not None:
            self.current_time = current_time
        else:
            self.current_time = time.time()

        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clear PID computation/values"""

        self.setPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, error, current_time=None):
        """
        Will take in current error as feedback_value and calculate based off of it the output.
        """

        if current_time is not None:
            self.current_time = current_time
        else:
            self.current_time = time.time()

        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if self.ITerm < -self.windup_guard:
                self.ITerm = - self.windup_guard
            elif self.ITerm > self.windup_guard:
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and error for next calculation
            self.last_time = self.current_time
            self.last_error = error
            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

        # We can only move about 9 degrees, so output can't be larger than 9 degrees
        if self.output > 9:
            self.output = 9

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sample time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time
