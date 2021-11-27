
#Python Lib
import pygame
import time
from random import randint

#Current Module
from . import set_hitbox_monster

#Monster idea
#1200 (2400) madness -- spider -- octopus -- rat king -- dog (dammage zone) -- millipede -- virus -- display something on target

class DefaultMonster:
    injured = 0
    injured_gradient = 16
    attack = 1
    direction = 0
    degeneration = 400
    hunt = True
    poisoned = 0
    inflamed = 0
    forest = False
    rooted = False
    stoned = False
    potion_effect = True
    invulnerable = 0
    insect = False

    def build_class(env):
        DefaultMonster.env = env
        DefaultMonster.dimensions = env.player_dimensions
        DefaultMonster.img_invulnerable = env.mod.tools.set_imgs(env.img_folder + 'monsters/', 'invulnerable', DefaultMonster.dimensions)
        DefaultMonster.img_invulnerable_large = env.mod.tools.set_imgs(env.img_folder + 'monsters/', 'invulnerable_large', DefaultMonster.dimensions)
        DefaultMonster.img_inflamed = env.mod.tools.set_imgs(env.img_folder + 'bullets/', 'inflamed', DefaultMonster.dimensions)
        DefaultMonster.img_inflamed_large = env.mod.tools.set_imgs(env.img_folder + 'bullets/', 'inflamed_large', DefaultMonster.dimensions)
        DefaultMonster.half = DefaultMonster.dimensions // 2
        DefaultMonster.tools = env.mod.tools
        return DefaultMonster

    def _father_init(self, x, y):
        self.x = x + self.env.width + 200 if x > -100 else x
        self.y = y + self.env.height + 200 if y > -100 else y
        self.target = self.env.players[0]

    def affected(self, bullet):
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False


    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.id_nb, 1
        return None, None


    def _find_target(self):
        d_objective = -1
        target = None
        x_objective = 0
        y_objective = 0
        for player in self.env.players:
            if not player.lives:
                continue
            x, y, distance = self.tools.process_distance(player, self)
            if target is None or d_objective > distance:
                if not x and not y:
                    return None, None
                d_objective = distance
                x_objective = x
                y_objective = y
                target = player
        return x_objective, y_objective, d_objective, target


    def _determine_direction(self, x, y):
        if not y or abs(x / y) > 0.66:
            if x < 0:
                direction = 2
            else:
                direction = 6
        elif abs(x / y) < 0.33:
            if y < 0:
                direction = 0
            else:
                direction = 4
        else:
            if x < 0 and y < 0:
                direction = 1
            elif x < 0:
                direction = 3
            elif y > 0:
                direction = 5
            else:
                direction = 7
        return direction


    def _sniff_fresh_flesh(self):
        x, y, distance, target = self._find_target()
        if target is None:
            return None, None
        self.target = target
        return self._determine_direction(x, y), distance


    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)


    def _action(self):
        if not self.stoned:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def _quit(self):
        self.tick.sleep()
        while self.env.pause:
            if self.env.quit:
                return True
            self.tick.sleep()
        return self.env.quit

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return


    def _debug(self):
        if self.env.debug and (self.lives or self.env.walking_dead) and self.hunt:
            pygame.draw.line(self.env.GameWindow, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            self.tools.display(self.env, self.hitbox.img, self.hitbox.x, self.hitbox.y)


    def reset_bad_effect(self):
        self.poisoned = 0
        self.inflamed = 0
        self.injured = 0

    def set_on_fire(self, n):
        if not self.invulnerable:
            self.inflamed = n

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.inflamed:
            self.inflamed -= 1
            if self.inflamed == 0:
                if randint(0, 6):
                    self.inflamed = 12
            if not self.inflamed % 12:
                self.lives -= 1
                self.injured += 6
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
