
def move(obj, direction, rapidity=0):
    if not rapidity:
        rapidity = obj.rapidity
    obj.direction = direction
    if direction == 0:
        obj.y -= rapidity
    elif direction == 1:
        obj.y, obj.x = obj.y - (rapidity / (2 ** 0.5)), obj.x - (rapidity / (2 ** 0.5))
    if direction == 2:
        obj.x -= rapidity
    elif direction == 3:
        obj.y, obj.x = obj.y + (rapidity / (2 ** 0.5)), obj.x - (rapidity / (2 ** 0.5))
    if direction == 4:
        obj.y += rapidity
    elif direction == 5:
        obj.y, obj.x = obj.y + (rapidity / (2 ** 0.5)), obj.x + (rapidity / (2 ** 0.5))
    if direction == 6:
        obj.x += rapidity
    elif direction == 7:
        obj.y, obj.x = obj.y - (rapidity / (2 ** 0.5)), obj.x + (rapidity / (2 ** 0.5))
