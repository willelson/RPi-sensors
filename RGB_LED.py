import RPi.GPIO as GPIO
import time
import contextlib

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()
    
@contextlib.contextmanager
def PWM(port, frequency, duty):
    a = GPIO.PWM(port, frequency)
    a.start(duty)
    yield
    a.stop()

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

frequency = 20

with autocleanup():
    with PWM(4, frequency, 80) as red:
        with PWM(17, frequency, 50) as green:
            with PWM(22, frequency, 50) as blue:
                time.sleep(5)
    


    


