import RPi.GPIO as GPIO
from time import time
TRIG_PIN = 18
DETAILS_AMOUNT = 6
CIRCLE_LENGHT = 3.1416 * 0.4815


def initialize(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)


def take_val(prev_time, length=CIRCLE_LENGHT, details=DETAILS_AMOUNT):
    return length/(details*(time() - prev_time))


def pin_status(pin):
    return GPIO.input(pin)


if __name__ == '__main__':
    initialize(TRIG_PIN)
    while True:
        print(take_val(TRIG_PIN))
