sign = lambda x: (1, -1)[x < 0]

def force_move(obj, x, y, direction, rapidity=0, set_direction=True):
    value = abs(x) + abs(y)

    if not rapidity:
        rapidity = obj.rapidity
    if set_direction:
        obj.direction = direction

    yfactor = (value - abs(y)) / value
    xfactor = (value - abs(x)) / value
    obj.y, obj.x = obj.y + sign(y) * (rapidity / ( yfactor ** 0.5)), obj.x + sign(x) * (rapidity / ( xfactor ** 0.5))
