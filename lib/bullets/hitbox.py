import pygame

class HitboxBullet:
    def update_coords(self, bullet):
        self.x = int(bullet.x + self.resize)
        self.y = int(bullet.y + self.resize)

    def __init__(self, bullet, resize):
        self.resize = int(bullet.dimensions * ((1.00 - resize) / 2))
        self.update_coords(bullet)
        self.dimensions = int(bullet.dimensions * resize)

def set_hitbox_bullet(env, bullet, resize=0.12):
    hitbox = HitboxBullet(bullet, resize)
    img = pygame.image.load(env.img_folder + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox
