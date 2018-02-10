import time

def clock(obj, wait=0.01):
    t = time.time()
    diff = t - self.time
    self.time = t
    if diff < wait:
        return diff
    else:
        return 0
