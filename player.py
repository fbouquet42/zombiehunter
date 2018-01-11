from display import set_imgs
import pygame


class Hitbox:
    def update_coords(self, player):
        self.x = int(player.x + player.dimensions * 0.1)
        self.y = int(player.y + player.dimensions * 0.1)

    def __init__(self, player, dimensions):
        self.update_coords(player)
        self.dimensions = dimensions

def set_hitbox(env, player):
    hitbox = Hitbox(player, int(player.dimensions * 0.8))
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class   Weapon:
    def update_coords(self, player):
        self.x = int(player.x + player.dimensions * 0.8 - self.dimensions * 0.45)
        self.y = int(player.y - self.dimensions * 0.5)
        self.direction = player.direction
        if self.direction == 1:
            self.x -= int(player.dimensions * 0.4)
        elif self.direction == 2:
            self.x -= int(player.dimensions * 0.9)
        elif self.direction == 3:
            self.x -= int(player.dimensions * 0.9)
            self.y += int(player.dimensions * 0.5)
        elif self.direction == 4:
            self.x -= int(player.dimensions * 0.8)
            self.y += int(player.dimensions * 0.9)
        elif self.direction == 5:
            self.x -= int(player.dimensions * 0.5)
            self.y += player.dimensions
        elif self.direction == 6:
            self.y += int(player.dimensions * 0.9)
        elif self.direction == 7:
            self.y += int(player.dimensions * 0.4)
            self.x += int(player.dimensions * 0.2)
        self.curr_img = self.img[self.direction]

    def __init__(self, env, player, dimensions, name):
        self.dimensions = dimensions
        self.name = name
        set_imgs(env, self)
        self.update_coords(player)
        self.is_attr = True

class   Bullet:
    def __init__(self, env, name, dimensions, rapidity):
        self.dimensions = dimensions
        self.name = name
        self.rapidity = rapidity
        set_imgs(env, self)
        env.to_display.pop(-1)

    def move(self, direction):
        self.direction = direction
        self.curr_img = self.img[direction]
        if direction == 0:
            self.y -= self.rapidity
        elif direction == 1:
            self.y, self.x = self.y - (self.rapidity / (2 ** 0.5)), self.x - (self.rapidity / (2 ** 0.5))
        if direction == 2:
            self.x -= self.rapidity
        elif direction == 3:
            self.y, self.x = self.y + (self.rapidity / (2 ** 0.5)), self.x - (self.rapidity / (2 ** 0.5))
        if direction == 4:
            self.y += self.rapidity
        elif direction == 5:
            self.y, self.x = self.y + (self.rapidity / (2 ** 0.5)), self.x + (self.rapidity / (2 ** 0.5))
        if direction == 6:
            self.x += self.rapidity
        elif direction == 7:
            self.y, self.x = self.y - (self.rapidity / (2 ** 0.5)), self.x + (self.rapidity / (2 ** 0.5))
        self.hitbox.update_coords(self)
        for attr in self.attributes:
            attr.update_coords(self)

def set_attrs(env, player):
    attrs = []
    if player.name == "jack":
        attrs.append(Weapon(env=env, player=player, dimensions=70, name="crossbow_unloaded"))
        player.bullet = Bullet(env=env, name="arrow", dimensions=35, rapidity=26)
    elif player.name == "baltazar":
        attrs.append(Weapon(env=env, player=player, dimensions=100, name="submachine_gun_3"))
        player.bullet = Bullet(env=env, name="bullet", dimensions=30, rapidity=32)
    return attrs

class Player:
    def __init__(self, env, x, y, dimensions, name, keys):
        self.x = env.width * x
        self.y = env.heigth * y
        self.up, self.left, self.down, self.right, self.shoot = keys

        self.alive = True
        self.lives = 4
        self.direction = 0
        self.rapidity = 16

        self.dimensions = dimensions
        self.name = name

        set_imgs(env, self)
        self.hitbox = set_hitbox(env, self)
        self.attributes = set_attrs(env, self)
        self.is_attr = False

    def move(self, direction):
        self.direction = direction
        self.curr_img = self.img[direction]
        if direction == 0:
            self.y -= self.rapidity
        elif direction == 1:
            self.y, self.x = self.y - (self.rapidity / (2 ** 0.5)), self.x - (self.rapidity / (2 ** 0.5))
        if direction == 2:
            self.x -= self.rapidity
        elif direction == 3:
            self.y, self.x = self.y + (self.rapidity / (2 ** 0.5)), self.x - (self.rapidity / (2 ** 0.5))
        if direction == 4:
            self.y += self.rapidity
        elif direction == 5:
            self.y, self.x = self.y + (self.rapidity / (2 ** 0.5)), self.x + (self.rapidity / (2 ** 0.5))
        if direction == 6:
            self.x += self.rapidity
        elif direction == 7:
            self.y, self.x = self.y - (self.rapidity / (2 ** 0.5)), self.x + (self.rapidity / (2 ** 0.5))
        self.hitbox.update_coords(self)
        for attr in self.attributes:
            attr.update_coords(self)
