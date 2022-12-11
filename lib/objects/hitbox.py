import pygame

class _Hitbox:
    def update_coords(self, monster):
        self.x = int(monster.x + self.resize)
        self.y = int(monster.y + self.resize)

    def __init__(self, monster, resize):
        self.resize = int(monster.dimensions * ((1.00 - resize) / 2))
        self.update_coords(monster)
        self.dimensions = int(monster.dimensions * resize)

def set_hitbox(env, monster, resize=0.24):
    hitbox = _Hitbox(monster, resize)
    if env.debug:
        img = pygame.image.load(env.img_folder + "hitbox.png")
        img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    else:
        img = None
    hitbox.img = img
    return hitbox
