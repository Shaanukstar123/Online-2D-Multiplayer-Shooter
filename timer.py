import time

class Timer(object):
    def __init__(self):
        self.start_time = None
        self.stop_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()

    @property
    def time_elapsed(self):
        if not self.has_started:
            return 0
        return int(time.time() - self.start_time)

    @property
    def has_started(self):
        return self.start_time != None

    @property
    def total_run_time(self):
        print("HAS IT STARTED: " + str(self.has_started))

        return self.stop_time - self.start_time

    def __enter__(self):
        self.start()
        return self
