import pygame

def set_imgs(folder, name, dimensions):
    tab = []
    tab.append(pygame.image.load(folder + name + '.png'))
    tab[0] = pygame.transform.scale(tab[0], (dimensions, dimensions))
    tab.append(pygame.transform.rotate(tab[0], 45))
    tab.append(pygame.transform.rotate(tab[0], 90))
    tab.append(pygame.transform.rotate(tab[0], 135))
    tab.append(pygame.transform.rotate(tab[0], 180))
    tab.append(pygame.transform.rotate(tab[0], 225))
    tab.append(pygame.transform.rotate(tab[0], 270))
    tab.append(pygame.transform.rotate(tab[0], 315))
    return tab

def move(obj, direction):
    obj.direction = direction
    if direction == 0:
        obj.y -= obj.rapidity
    elif direction == 1:
        obj.y, obj.x = obj.y - (obj.rapidity / (2 ** 0.5)), obj.x - (obj.rapidity / (2 ** 0.5))
    if direction == 2:
        obj.x -= obj.rapidity
    elif direction == 3:
        obj.y, obj.x = obj.y + (obj.rapidity / (2 ** 0.5)), obj.x - (obj.rapidity / (2 ** 0.5))
    if direction == 4:
        obj.y += obj.rapidity
    elif direction == 5:
        obj.y, obj.x = obj.y + (obj.rapidity / (2 ** 0.5)), obj.x + (obj.rapidity / (2 ** 0.5))
    if direction == 6:
        obj.x += obj.rapidity
    elif direction == 7:
        obj.y, obj.x = obj.y - (obj.rapidity / (2 ** 0.5)), obj.x + (obj.rapidity / (2 ** 0.5))
