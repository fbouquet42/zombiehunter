import time

def clock(obj, wait=0.03):
    t = time.time()
    diff = t - obj.time
    obj.time = t
    if diff < wait:
        return diff
    else:
        return 0
