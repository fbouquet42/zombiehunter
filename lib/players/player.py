import pygame
from threading import Thread

from . import set_hitbox_player

class Player:
    max_lives = 88
    lives = 88
    direction = 0
    rapidity = 11
    injured = 0
    score = 0
    font = pygame.font.SysFont('Comic Sans MS', 40)

    def _get_weapon(self, env):
        if self.name == 'jack':
            return env.mod.weapons.Crossbow(env, self)
        if self.name == 'baltazar':
            return env.mod.weapons.SubmachineGun(env, self)

    def undead(self, env):
        obj = env.mod.monsters.Undead(env, self)
        t = Thread(target=obj.move, args=())
        t.daemon = True
        self.possessed = True
        env.monsters.append(monster)
        t.start()

    def __init__(self, env, keys, x, y, dimensions, name):
        self.env = env
        self.tools = env.mod.tools

        self.up, self.left, self.down, self.right, self.shoot = keys
        self.xinitial = x
        self.yinitial = y
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.half = self.dimensions // 2

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.name = name

        self.img = self.tools.set_imgs(env.img_folder + 'players/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_dead', self.dimensions)
        self.img_possessed = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_possessed', self.dimensions)
        self.possessed = False

        self.hitbox = set_hitbox_player(env, self)
        self.weapon = self._get_weapon(env)

    def affected(self, bullet):
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def display_lives(self, env):
        live_percent = int((self.lives / self.max_lives) * 100)
        if live_percent > 70:
            img = self.font.render(str(live_percent), False, (13, 115, 5))
        elif live_percent > 35:
            img = self.font.render(str(live_percent), False, (222, 146, 13))
        else:
            img = self.font.render(str(live_percent), False, (152, 25, 0))
        self.tools.display(env, img, self.x, self.y)

    def display_score(self, env):
        score = self.font.render(str(self.score), False, (110, 74, 0))
        self.tools.display(env, self.img[0], self.xinitial, self.yinitial)
        self.tools.display(env, score, self.xinitial, self.yinitial)

    def hitted(self, attack=1):
        if self.lives:
            self.injured = 22
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives

    def move(self, direction):
        self.tools.move(self, direction)
        self.tools.limits(self, self.limitx, self.limity)
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
            self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives:
            self.weapon.display(env, self.direction, self.x, self.y, fitting)
        if env.debug and self.lives:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        self.weapon.update()