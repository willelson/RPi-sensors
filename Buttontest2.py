import RPi.GPIO as GPIO
import time
import contextlib

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()

count = 0

def button_pressed(channel):
    global count
    count += 1
    print count, "button pressed!"
    


GPIO.setmode(GPIO.BCM)

with autocleanup():
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.RISING, callback=button_pressed, bouncetime=300)
    while count < 15:
        time.sleep(0.001)
            

