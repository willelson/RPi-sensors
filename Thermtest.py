import glob
import os
import time

devices = glob.glob("/sys/bus/w1/devices/28-*")
device1 = devices[0]
fname = os.path.join(device1, 'w1_slave')

with open(fname, 'r') as fob:
    sensor_data = fob.read().strip()
    temp = float(sensor_data[-5:])/1000
    print temp, "Degrees Celcius"
