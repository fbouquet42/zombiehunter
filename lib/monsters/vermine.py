from random import randint

from . import DefaultMonster
from . import set_hitbox_monster

class   Vermine(DefaultMonster):
    name = "vermine"
    attack_on_suicide = 4
    lives = 10
    degeneration = 130
    target = None
    hunt = False
    turn = 7
    duration = 300

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.limitx = cls.env.width - cls.half
        cls.limity = cls.env.height - cls.half
        cls.vermine_squeeze = cls.env.mod.objects.VermineSqueeze.build_class(cls.env, cls.dimensions)
        return cls

    def __init__(self, father):
        self.x = father.x
        self.y = father.y
        self.hitbox = set_hitbox_monster(self.env, self, 0.24 * 0.9)
        self.father = father

        self.rapidity = randint(10, 16)
        self.wait = self.turn

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
        return None, None

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting) #maybe have to rework this
        self._debug()

    def _random_direction(self):
        if not self.wait:
            self.direction = randint(0, 7)
            self.wait = self.turn
        else:
            self.wait -= 1

    def _fuss(self):
        if not self.stoned:
            self._random_direction()
            self.tools.move(self, self.direction, self.rapidity + self.env.furious)
            self.hitbox.update_coords(self)
            self.tools.limits(self, self.limitx, self.limity)
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._fuss()
            if self._quit():
                return
        self.env.objects.append(self.vermine_squeeze(self.x, self.y))
        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                if self.lives:
                    player.hitted(attack=self.attack_on_suicide)
                    self.lives = 0
                else:
                    player.hitted(attack=self.attack)
                    if self.inflamed and not randint(0, 3):
                        player.inflamed = 1
        if self.inflamed:
            for monster in self.env.monsters:
                if monster == self:
                    continue
                elif monster.affected(self) and not monster.inflamed:
                    if not randint(0, 3):
                        monster.set_on_fire(1, self.master_of_flames)

    def update(self):
        super().update()
        if not self.father.lives:
                self.lives = 0
        if self.duration:
            self.duration -= 1
            if not self.duration:
                self.lives = 0
