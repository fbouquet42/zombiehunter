import tools
import pygame
import weapons

class HitboxPlayer:
    def update_coords(self, player):
        self.x = int(player.x + player.dimensions * 0.38)
        self.y = int(player.y + player.dimensions * 0.38)

    def __init__(self, player, dimensions):
        self.update_coords(player)
        self.dimensions = dimensions

def set_hitbox_player(env, player):
    hitbox = HitboxPlayer(player, int(player.dimensions * 0.24))
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class Player:
    def __init__(self, env, x, y, dimensions, name, keys):
        self.x = env.width * x
        self.y = env.height * y
        self.dimensions = dimensions
        self.half = self.dimensions // 2
        self.limitx = env.width - self.half
        self.limity = env.height - self.half
        self.up, self.left, self.down, self.right, self.shoot = keys

        self.alive = True
        self.lives = 4
        self.direction = 0
        self.rapidity = 9
        self.injured = 0

        self.name = name

        self.img = tools.set_imgs(env.img_src + 'players/', self.name, self.dimensions)
        self.hitbox = set_hitbox_player(env, self)
        self.weapon = weapons.set_weapon(env, self)
        self.img_injured = tools.set_imgs(env.img_src + 'players/', self.name + '_injured', self.dimensions)
        self.img_dead = tools.set_imgs(env.img_src + 'players/', self.name + '_dead', self.dimensions)

        env.players.append(self)

    def move(self, direction):
        tools.move(self, direction)
        if self.x > self.limitx:
            self.x = self.limitx
        if self.y > self.limity:
            self.y = self.limity
        if self.x < -self.half:
            self.x = -self.half
        if self.y < -self.half:
            self.y = -self.half
        self.hitbox.update_coords(self)
