import RPi.GPIO as GPIO

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

with autocleanup():
    GPIO.setup(17, GPIO.IN)
    for i in range(20):
        GPIO.input(17, i%2==1)
        time.sleep(0.2)
