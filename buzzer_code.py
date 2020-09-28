"""

"""
import RPi.GPIO as GPIO
# Setup
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.HIGH)


# Low
def low():
    GPIO.output(buzzer_pin, GPIO.HIGH)


# high
def high():
    GPIO.output(buzzer_pin, GPIO.LOW)
