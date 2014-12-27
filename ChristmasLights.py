import RPi.GPIO as GPIO
import time
import itertools

import contextlib

@contextlib.contextmanager
def autocleanup():
    yield
    GPIO.cleanup()

# A list of patterns. A pattern is a list of
# times to have the switch on, then off for
# and can be as long and complex as you like.
# Of course, a pattern must have an even
# number of instructions.
patterns = [(0.1, 0.1),
            (0.25, 0.1, 0.1, 0.1),
            ]


for pattern in patterns:
    if len(pattern) % 2 != 0:
        raise ValueError('One of the patterns does not have '
                         'an even number of instructions')

patterns = iter(patterns)


pattern = None
next_state = None
def button_pressed(channel):
    global pattern, next_state
    pattern = itertools.cycle(next(patterns))
    next_state = True

# Pick the first pattern.
button_pressed(None)
    
LIGHT_CHANNEL = 6
BUTTON_CHANNEL = 12

GPIO.setmode(GPIO.BCM)


with autocleanup():
    GPIO.setup(BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON_CHANNEL, GPIO.RISING,
                          callback=button_pressed, bouncetime=300)

    GPIO.setup(LIGHT_CHANNEL, GPIO.OUT)
    count = 0
    while count < 500:
        # Get the next in the pattern.
        sleep_time = next(pattern)
    #for time in pattern:
        GPIO.output(LIGHT_CHANNEL, next_state)
        next_state = not next_state
        count += 1
        time.sleep(sleep_time)
