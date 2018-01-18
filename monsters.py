import tools
import pygame
import weapons

class HitboxMonster:
    def update_coords(self, monster):
        self.x = int(monster.x + self.resize)
        self.y = int(monster.y + self.resize)

    def __init__(self, monster, resize):
        self.resize = int(monster.dimensions * ((1.00 - resize) / 2))
        self.update_coords(monster)
        self.dimensions = int(monster.dimensions * resize)

def set_hitbox_monster(env, monster, resize=0.24):
    hitbox = HitboxPlayer(monster, resize)
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class Zombie:
    def __init__(self, env, x, y, weapon=None):
        self.x = env.width * x
        self.y = env.height * y
        self.dimensions = env.player_dimensions
        self.half = self.dimensions // 2

        self.lives = 2
        self.direction = 0
        self.rapidity = 7
        self.injured = 0

        self.img = tools.set_imgs(env.img_src + 'players/', "zombie", self.dimensions)
        self.hitbox = set_hitbox_player(env, self)
        self.weapon = weapon(env, self)
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

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        tools.display(env, img, self.x, self.y, fitting)
        if self.lives:
            self.weapon.display(env, self.direction, self.x, self.y, fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        self.weapon.update()
