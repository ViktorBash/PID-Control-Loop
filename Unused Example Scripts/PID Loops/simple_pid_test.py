from simple_pid import PID
import time
import random
from matplotlib import pyplot as plt
pid = PID(1, 0.5, 0.05, setpoint=0)

pid.sample_time = 0.01

output_list = []
time_list = [i for i in range(0, 101)]
input_list = []

# This will be our starting number (aka angle)
num = 15

for i in range(0, 101):
    # We append input and output before changing any values. Input is what the current number is and output is the
    # recommended value by the pid loop
    input_list.append(num)
    output = pid(num)
    output_list.append(output)

    if num < output:  # if num less than pid loop (aka output), bring num up
        num = num + 2
    if num > output:  # if num more than pid loop (aka output), bring num down
        num = num - 2
    print(num)

    time.sleep(0.01)

print("data is done")

plt.plot(time_list, output_list, label="Output")
plt.plot(time_list, input_list, label="Input")
plt.legend()
plt.show()

"""Question to ask: For pid loop that was made, what are the parameters/numbers you ended up with? Idea: Encapsulate 
the while statements into a function Put the function that interact with pid loop into a function as well Then use 
multiprocessing to run both functions in parallel (so function 1 can write to dicts while function 2 can read those 
dicts) 

"""