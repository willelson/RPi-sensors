import RPi.GPIO as GPIO
import time
import contextlib

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()


GPIO.setmode(GPIO.BCM)

with autocleanup():
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if GPIO.wait_for_edge(6, GPIO.FALLING):
        print "Button pressed!"
            

