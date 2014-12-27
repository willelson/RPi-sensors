import contextlib
from collections import namedtuple
from datetime import datetime, timedelta
import itertools
import time
import sys

import RPi.GPIO as GPIO


PWM = namedtuple('PWM', ['frequency', 'duty', 'time'])


class ChristmasLights(object):
    def __init__(self, patterns):
        # A variable to tell us if we should terminate a run loop.
        self._poisoned = False

        self._patterns_iter = itertools.cycle(patterns)
        self._button_events = {'down': None, 'up': None}

        #: An infinite loop of on/off pattern.
        self._pattern = None

    def next_pattern(self):
        try:
            pattern = next(self._patterns_iter)
        except StopIteration:
            # We've run out of patterns, so poison the run loop.
            self._poisoned = True
        else:
            self.set_pattern(pattern) 

    def set_pattern(self, pattern):
        self._pattern = itertools.cycle(pattern)
        # Stop program waiting in run function
        self.waiting = False

    def confirm_interruption(self):
        """
        A *blocking* raw input to interrup the display.

        This would normally be called in a new thread with:

        import thread
        thread.start_new_thread(self.confirm_interruption, tuple())
        
        """
        msg = 'Type "yes" to interrupt the display: '
        answer = None
        while answer not in ['y', 'yes']:
            answer = raw_input(msg).lower().strip()
        self._poisoned = True

    def non_blocking_confirm_interrupt(self):
        import threading
        thread = threading.Thread(target=self.confirm_interruption)
        thread.daemon = False
        thread.start()

    def non_blocking_confirm_interrupt(self):
        import select
        print sys.stdin
        sys.stdin._RPCProxy__methods['fileno'] = 1
        msg = 'Type "yes" to interrupt the display: '
        answer = None
        while answer not in ['y', 'yes']:
            sys.stdout.write(msg)
            select.select([sys.stdin], [], [], 0)
            answer = sys.stdin.readline().lower().strip()
        self._poisoned = True
        
    def run(self):
        for _ in self._run():
            pass

    def _run(self, timer_step=0.1):
        """The loop of our Christmas display."""
        self._poisoned = False
        self.next_pattern()
        while self._poisoned == False:
            pwm = next(self._pattern)
            self.light_pwm.ChangeDutyCycle(pwm.duty)
            self.light_pwm.ChangeFrequency(pwm.frequency)
            start = datetime.now()
            self.waiting = True
            yield
            while self.waiting and datetime.now() - start < timedelta(seconds = pwm.time):
                time.sleep(timer_step)
                yield
        
        self._poisoned = False

    def button_down_event(self, channel):
        last = self._button_events['down']
        now = datetime.now()
        if last is not None and now - last < timedelta(milliseconds=500):
            print('Clicked in {}. Exiting.'.format(now - last))
            self._poisoned = True
        else:
            self._button_events['down'] = datetime.now()
            self.next_pattern()

    @contextlib.contextmanager
    def setup(self, button_channel, light_channel):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(light_channel, GPIO.OUT)

        GPIO.add_event_detect(button_channel, GPIO.FALLING,
                              callback=self.button_down_event,
                              bouncetime=150)
        self.light_pwm = GPIO.PWM(light_channel, 1)
        self.light_pwm.start(0)
        yield
        self.light_pwm.stop()
        GPIO.cleanup()


fade_step_len = 0.1
steps = range(1, 100, 5)
STOCK_PATTERNS = [
                    [PWM(i-0.75, 50, 2) for i in range(1, 15, 1)],
                    [PWM(100, i, fade_step_len) for i in steps] + [PWM(100, i, fade_step_len) for i in steps[::-1]],
                    [PWM(2, 50, 2), PWM(2, 100, 2)],
                    [PWM(2, 100, 20)],
                 ]
STOCK_PATTERN_NAMES = ["Will's fader",
                       "Fade in fade out",
                       "Blink then solid",
                       "Solid"]

if __name__ == '__main__':
    display = ChristmasLights(STOCK_PATTERNS)
    with display.setup(button_channel=12, light_channel=6):
        print('Click twice within half a second to terminate.')
        display.run()
