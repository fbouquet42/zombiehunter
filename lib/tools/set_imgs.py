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
