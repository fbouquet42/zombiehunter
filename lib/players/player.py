import pygame
from threading import Thread
from random import randint

from . import set_hitbox_player
from . import Score

class Player:
    max_lives = 82
    lives = 82
    direction = 0
    max_rapidity = 22
    rapidity = 22
    injured = 0
    font = pygame.font.SysFont('Comic Sans MS', 30)
    poisoned = 0
    inflamed = 0
    fixed = False
    destroy = False
    rage = False
    abaddon = False
    stoned = False
    shadow = False
    is_player = True

    def _get_weapon(self, env):
#        env.mod.weapons.MagicWand.build_class(env)
#        env.mod.weapons.ShadowDaggers.build_class(env)
#        env.mod.weapons.Abaddon.build_class(env)
#        env.mod.weapons.Aguni.build_class(env)
        if self.name == 'jack':
            return env.mod.weapons.Crossbow(env, self)
#            env.mod.weapons.DragonHead.build_class(env)
#            return env.mod.weapons.DragonHead(env, self)
#            return env.mod.weapons.Aguni(env, self)
#            return env.mod.weapons.Abaddon(env, self)
#            return env.mod.weapons.SubmachineGun(env, self)
            #env.mod.weapons.MagicWand.build_class(env)
#            env.mod.weapons.DevilBlade.build_class(env)
            #return env.mod.weapons.ShadowDaggers(env, self)
#            return env.mod.weapons.DevilBlade(env, self)
#            return env.mod.weapons.MagicWand(env, self)
        if self.name == 'baltazar':
            #env.mod.weapons.MagicWand.build_class(env)
            #return env.mod.weapons.MagicWand(env, self)
#            env.mod.weapons.DragonHead.build_class(env)
#            return env.mod.weapons.DragonHead(env, self)
            return env.mod.weapons.SubmachineGun(env, self)

    def undead(self, env):
        obj = env.mod.monsters.Undead(env, self)
        t = Thread(target=obj.move, args=())
        t.daemon = True
        self.possessed = True
        env.monsters.append(obj)
        t.start()

    def __init__(self, env, keys, x, y, dimensions, name):
        self.env = env
        self.tools = env.mod.tools

        self.up, self.left, self.down, self.right, self.shoot = keys
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.half = self.dimensions // 2

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.name = name

        self.img = self.tools.set_imgs(env.img_folder + 'players/', self.name, self.dimensions)
        self.img_enraged = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_enraged', self.dimensions)
        self.img_night = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_night', self.dimensions)
        self.img_enraged_night = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_enraged_night', self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_injured', self.dimensions)
        self.img_injured_night = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_injured_night', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_dead', self.dimensions)
        self.img_possessed = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_possessed', self.dimensions)
        self.img_shadow = self.tools.set_imgs(env.img_folder + 'players/', self.name + '_shadow', self.dimensions)
        self.img_inflamed = self.tools.set_imgs(env.img_folder + 'bullets/', 'inflamed', self.dimensions)
        self.possessed = False

        self.hitbox = set_hitbox_player(env, self)
        self.weapon = self._get_weapon(env)
        self.score = Score(env, self, x, y, dimensions)

    def affected(self, bullet):
        if self.shadow:
            return False
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def display_lives(self, env):
        if not self.lives or env.night:
            return
        live_percent = int((self.lives / self.max_lives) * 100)
        weapon_xp = ""
        for i in range(1, 4):
            if not self.weapon.tier_up and self.weapon.xp > (self.weapon.level_up // 4) * i:
                weapon_xp += "."
            else:
                break
        if live_percent > 66:
            img = self.font.render(str(live_percent) + weapon_xp, False, (13, 115, 5))
        elif live_percent > 33:
            img = self.font.render(str(live_percent) + weapon_xp, False, (222, 146, 13))
        else:
            img = self.font.render(str(live_percent) + weapon_xp, False, (152, 25, 0))
        self.tools.display(env, img, self.x, self.y)

    def hitted(self, attack=1):
        if self.lives:
            self.injured = 22
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                self.inflamed = 0
                self.score.kills[-1] += 1

    def move(self, direction, rapidity=0):
        if self.fixed:
            self.tools.move(self, direction, rapidity=rapidity if not self.stoned and not self.fixed else (self.rapidity - 6))
        elif rapidity:
            self.tools.move(self, direction, rapidity=rapidity if not self.stoned else (self.rapidity - 8))
        elif self.shadow or self.rage:
            self.tools.move(self, direction, rapidity=(self.rapidity + 5))
        else:
            self.tools.move(self, direction)
        self.tools.limits(self, self.limitx, self.limity)
        self.hitbox.update_coords(self)

    def _display_day(self, env, fitting):
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.shadow:
            img = self.img_shadow[self.direction]
        elif self.rage:
            img = self.img_enraged[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        if not self.possessed:
            self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.inflamed:
            self.tools.display(env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        if self.lives:
            self.weapon.display(env, self.direction, self.x, self.y, fitting)

    def _display_night(self, env, fitting):
        if not self.lives:
            return
        elif self.rage:
            img = self.img_enraged_night[self.direction]
        elif self.injured:
            img = self.img_injured_night[self.direction]
        else:
            img = self.img_night[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if env.night:
            self._display_night(env, fitting)
        else:
            self._display_day(env, fitting)
        if env.debug and self.lives:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def reset_bad_effect(self):
        self.stoned = False
        self.poisoned = 0
        self.inflamed = 0
        self.injured = 0
        self.possessed = False

    def update(self):
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        self.weapon.update()
        if self.inflamed:
            self.inflamed -= 1
            if self.inflamed == 0:
                if randint(0, 5):
                    self.inflamed = 7
            if not self.inflamed % 7:
                self.lives -= 1
                self.injured += 3
        if self.poisoned:
            self.poisoned -= 1
            if self.lives and not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
