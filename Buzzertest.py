import RPi.GPIO as GPIO
import time
import contextlib

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

with autocleanup():
    GPIO.setup(17, GPIO.OUT)
    for i in range(20):
        GPIO.output(17, i%2==1)
        time.sleep(0.2)
