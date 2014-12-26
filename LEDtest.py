import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

for i in range(0,20,1):
    GPIO.output(26, i%2==1)
    GPIO.output(6, i%2==0)
    time.sleep(0.75)

GPIO.cleanup()
