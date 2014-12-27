from ChristmasLights2 import STOCK_PATTERNS, STOCK_PATTERN_NAMES, ChristmasLights
import tornado


import tornado.web
from tornado.ioloop import IOLoop, PeriodicCallback


class PatternHandler(tornado.web.RequestHandler):
    def initialize(self, lights):
        self.lights = lights

    def get(self):
        pattern_id = self.get_argument('pattern_id', None)
        if pattern_id is not None:
            pattern = STOCK_PATTERNS[int(pattern_id)]
            self.lights.set_pattern(pattern)
        self.write('Setting pattern to {}.<br>'.format(pattern_id))
        for pattern_id, pattern_name in enumerate(STOCK_PATTERN_NAMES):
            self.write('<a href="?pattern_id={}">{}</a><br>'.format(pattern_id,
                                                                    pattern_name))


if __name__ == '__main__':
    lights = ChristmasLights(STOCK_PATTERNS)
    handlers = [(r"/", PatternHandler, {'lights': lights})]
    application = tornado.web.Application(handlers, debug=True)  
    application.listen(80)
    running_lights = lights._run(timer_step=0)
    def next_step():
        next(running_lights)
    with lights.setup(button_channel=12, light_channel=6):
        loop = IOLoop.instance()
        callback = PeriodicCallback(next_step, 500, loop)
        callback.start()
        print('Click twice within half a second to terminate.')
        loop.start()
