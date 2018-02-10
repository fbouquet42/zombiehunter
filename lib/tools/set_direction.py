
_mask = {1 : 0, 2 : 2, 3 : 1, 4 : 4, 6 : 3, 8 : 6, 9 : 7, 12 : 5}
def set_direction(pressed, player):
    moving = 0
    if pressed[player.up]:
        moving += 1
    if pressed[player.left]:
        moving += 2
    if pressed[player.down]:
        moving += 4
    if pressed[player.right]:
        moving += 8
    try:
        direction = _mask[moving]
    except KeyError:
        direction = -1
    return direction
