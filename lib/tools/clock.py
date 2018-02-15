import time

def clock(obj, wait=0.04):
    t = time.time()
    diff = t - obj.time
    obj.time = t
    if diff < wait:
        return wait - diff
    else:
        return 0
