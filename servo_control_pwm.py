import RPi.GPIO as GPIO
import pigpio
import time

# Setting the servo pins
servo1 = 12
servo2 = 19

# Creating servo 1
pwm1 = pigpio.pi()
pwm1.set_mode(servo1, pigpio.OUTPUT)
pwm1.set_PWM_frequency(servo1, 50)


# Creating servo 2
pwm2 = pigpio.pi()
pwm2.set_mode(servo2, pigpio.OUTPUT)
pwm1.set_PWM_frequency(servo2, 50)

# Testing area
if __name__ == "__main__":
    # 500: 0 Degrees
    # 1500: 90 Degrees
    # 1 Degree Addition = 1000/90, aka: 11.1 recurring
    print("0 Degrees ")
    pwm1.set_servo_pulsewidth(servo1, 500)
    pwm2.set_servo_pulsewidth(servo2, 500)
    time.sleep(3)

    print("15 Degrees")
    pwm1.set_servo_pulsewidth(servo1, 500 + (1000/90 * 15))
    pwm2.set_servo_pulsewidth(servo2, 500 + (1000/90 * 15))
    time.sleep(3)

    print("0 Degrees ")
    pwm1.set_servo_pulsewidth(servo1, 500)
    pwm2.set_servo_pulsewidth(servo2, 500)


    # Turning off the servo
    # pwm1.set_PWM_dutycycle(servo1, 0)
    # pwm1.set_PWM_frequency(servo1, 0)
    # pwm2.set_PWM_dutycycle(servo2, 0)
    # pwm2.set_PWM_frequency(servo2, 0)
