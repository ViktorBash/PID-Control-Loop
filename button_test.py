import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

pin = 13
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(pin) == GPIO.HIGH:
        print("Button pushed")
