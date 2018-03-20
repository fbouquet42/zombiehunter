import time

from . import DefaultMonster
from . import set_hitbox_monster

class Harpy(DefaultMonster):
    lives = 30
    name = "harpy"
    id_nb = 6
    gradient = 0
    gradient_max = 20
    rapidity_onflight = 14
    rapidity_onground = 12
    ultimatum_onflight = 170
    ultimatum_onground = 85
    rooted = True

    def build_class():
        Harpy.img = Harpy.tools.set_imgs(Harpy.env.img_folder + 'monsters/', Harpy.name, Harpy.dimensions)
        Harpy.img_injured = Harpy.tools.set_imgs(Harpy.env.img_folder + 'monsters/', Harpy.name + '_injured', Harpy.dimensions)
        Harpy.img_dead = Harpy.tools.set_imgs(Harpy.env.img_folder + 'monsters/', Harpy.name + '_dead', Harpy.dimensions)
        Harpy.img_shadow_scale = list(Harpy.tools.set_imgs(Harpy.env.img_folder + 'monsters/', Harpy.name + '_shadow', int(Harpy.dimensions * (0.6 + nb * 0.05))) for nb in range(0, 9))
        Harpy.img_possessed = Harpy.tools.set_imgs(Harpy.env.img_folder + 'monsters/', Harpy.name + '_possessed', Harpy.dimensions)
        return Harpy

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.shadow = 0
        self.list_hitbox = list(set_hitbox_monster(env, self, (0.6 + nb * 0.05) * 0.22) for nb in range(0, 9))
        self.hitbox = self.list_hitbox[self.shadow]
        self.list_dimensions = list((0.6 + nb * 0.05) * self.dimensions for nb in range(0, 9))
        self.dimensions = self.list_dimensions[self.shadow]
        self._fly()

    def _gradient_fly(self, shadow):
        self.list_hitbox[shadow].update_coords(self)
        self.shadow = shadow
        self.hitbox = self.list_hitbox[self.shadow]
        self.dimensions = self.list_dimensions[self.shadow]

    def _fly(self):
        if not self.lives:
            return
        self._gradient_fly(0)
        self.flying = True
        self.rapidity = self.rapidity_onflight
        self.ultimatum = self.ultimatum_onflight
        self.gradient = self.gradient_max

    def _on_ground(self):
        if not self.lives:
            return
        self._gradient_fly(8)
        self.flying = False
        self.rooted = False
        self.rapidity = self.rapidity_onground
        self.ultimatum = self.ultimatum_onground
        self.gradient = self.gradient_max

    def affected(self, bullet):
        if self.flying or not self.ultimatum:
            return False
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                if self.flying or not self.ultimatum:
                    return True
                else:
                    player.hitted(attack=self.attack)
        return False

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                self.tools.move(self, direction, 3 if not self.ultimatum else self.rapidity)
                self.hitbox.update_coords(self)
            if self._target_hitted():
                self.ultimatum = 0
            if self._quit():
                return

        self.rapidity = self.rapidity_onground
        self.flying = False
        self.rooted = False
        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif not self.ultimatum:
            img = self.img_shadow_scale[self.shadow][self.direction]
        elif self.flying:
            img = self.img_shadow_scale[0][self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting - (self.list_dimensions[8] - self.dimensions) // 2)
        self._debug()

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives:
            if self.degeneration:
                self.degeneration -= 1
        elif self.ultimatum:
            self.ultimatum -= 1
        else:
            self.rooted = True
            self.gradient -= 1
            if self.flying and not self.gradient:
                self._on_ground()
            elif not self.gradient:
                self._fly()
            elif self.flying:
                self._gradient_fly((self.gradient_max - self.gradient) // 4 + 1)
            else:
                self._gradient_fly((self.gradient) // 4 + 1)
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
