"""
Will test pid here
"""

from pid_loop import PID
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


def test_pid(P=0.2, I=0, D=0):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID(P, I, D)

    pid.SetPoint = 1
    pid.setSampleTime(0.01)

    length = 120

    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, length):
        pid.update(feedback)
        output = pid.output
        # if pid.SetPoint >= 0:
        #     feedback += (output - (1 / i))
        if i > 9:
            pid.SetPoint = 65
        time.sleep(0.02)
        feedback = abs(pid.SetPoint - output)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)

    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
    plt.xlim((0, length))
    plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
    plt.xlabel('time (s)')
    plt.ylabel('Degrees')
    plt.title('TEST PID')

    plt.ylim(-180, 180)

    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    test_pid(0.2, 0, 0)
#    test_pid(0.8, L=50)
