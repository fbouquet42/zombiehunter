import tools
import pygame
import weapons

class HitboxPlayer:
    def update_coords(self, player):
        self.x = int(player.x + self.resize)
        self.y = int(player.y + self.resize)

    def __init__(self, player, resize):
        self.resize = int(player.dimensions * ((1.00 - resize) / 2))
        self.update_coords(player)
        self.dimensions = int(player.dimensions * resize)

def set_hitbox_player(env, player, resize=0.24):
    hitbox = HitboxPlayer(player, resize)
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class Player:
    lives = 4
    direction = 0
    rapidity = 17
    injured = 0
    score = 0

    def __init__(self, env, dimensions, name):
        self.dimensions = dimensions
        self.half = self.dimensions // 2
        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.name = name

        self.img = tools.set_imgs(env.img_src + 'players/', self.name, self.dimensions)
        self.img_injured = tools.set_imgs(env.img_src + 'players/', self.name + '_injured', self.dimensions)
        self.img_dead = tools.set_imgs(env.img_src + 'players/', self.name + '_dead', self.dimensions)
        self.img_possessed = tools.set_imgs(env.img_src + 'players/', self.name + '_possessed', self.dimensions)
        self.possessed = False

    def selected(self, env, title, keys, x, y):
        self.up, self.left, self.down, self.right, self.shoot = keys
        self.x = x
        self.y = y
        self.title = title
        self.hitbox = set_hitbox_player(env, self)
        self.weapon = weapons.set_weapon(env, self)

    def affected(self, bullet):
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def hitted(self, attack=1):
        if self.lives and not self.injured:
            self.injured += 25
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives

    def move(self, direction):
        tools.move(self, direction)
        tools.limits(self, self.limitx, self.limity)
        self.hitbox.update_coords(self)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        if not self.possessed:
            tools.display(env, img, self.x, self.y, fitting)
        if self.lives:
            self.weapon.display(env, self.direction, self.x, self.y, fitting)
        if env.debug and self.lives:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        self.weapon.update()
