
def limits(obj, limitx, limity):
    if obj.x > limitx:
        obj.x = limitx
    if obj.y > limity:
        obj.y = limity
    if obj.x < -obj.half:
        obj.x = -obj.half
    if obj.y < -obj.half:
        obj.y = -obj.half
