import pygame

class _HitboxPlayer:
    def update_coords(self, player):
        self.x = int(player.x + self.resize)
        self.y = int(player.y + self.resize)

    def __init__(self, player, resize):
        self.resize = int(player.dimensions * ((1.00 - resize) / 2))
        self.update_coords(player)
        self.dimensions = int(player.dimensions * resize)

def set_hitbox_player(env, player, resize=0.24):
    hitbox = _HitboxPlayer(player, resize)
    img = pygame.image.load(env.img_folder + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox
