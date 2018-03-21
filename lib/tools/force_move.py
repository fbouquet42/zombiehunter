sign = lambda x: (1, -1)[x < 0]

def force_move(obj, x, y, direction, rapidity=0, set_direction=True):
    value = abs(x) + abs(y)
    if not value:
        return

    if not rapidity:
        rapidity = obj.rapidity
    if set_direction:
        obj.direction = direction

    factor = abs(y) / value
    if factor:
        yfactor = 1 / factor
        obj.y += sign(y) * (rapidity / ( yfactor ** 0.5))
    if factor < 1:
        xfactor = 1 / (1 - factor)
        obj.x += sign(x) * (rapidity / ( xfactor ** 0.5))

