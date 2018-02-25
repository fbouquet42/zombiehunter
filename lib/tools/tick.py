import time

def     _clock(obj, wait):
    t = time.time()
    diff = t - obj.time
    return wait - diff

class   Tick:
    def __init__(self):
        self.time = time.time()

    def sleep(self, wait=0.04):
        t_sleep = _clock(self, wait)
        if t_sleep > 0.002:
            time.sleep(t_sleep)
        self.time = time.time()
