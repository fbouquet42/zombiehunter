
def     process_distance(tracked, tracker):
    x = (tracked.x + tracked.half) - (tracker.x + tracker.half)
    y = (tracked.y + tracked.half) - (tracker.y + tracker.half)
    distance = int((x ** 2 + y ** 2) ** 0.5)
    return x, y, distance
