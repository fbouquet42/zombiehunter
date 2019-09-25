
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class Fly(DefaultMonster):
    max_lives = 105
    lives_big = 70
    name = "fly"
    id_nb = 16
    degeneration = 250
    insect = True

    @classmethod
    def build_class(cls):
        cls.sniff = int(cls.dimensions * 1.5)
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_healed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_healed', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_big = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', 'big_' + cls.name, cls.dimensions)
        cls.img_big_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', 'big_' + cls.name + '_injured', cls.dimensions)
        cls.img_big_healed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', 'big_' + cls.name + '_healed', cls.dimensions)
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.env = env
        self.hitbox_small = set_hitbox_monster(env, self)
        self.hitbox_big = set_hitbox_monster(env, self, 0.46)
        self.hitbox = self.hitbox_small

        self.rapidity = randint(5, 10)
        self.rapidity = 7 if self.rapidity < 7 else self.rapidity

        self.lives = 40
        self.healed = 0

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

        if self.lives and self.lives < self.max_lives and d_objective > self.sniff:
            for player in self.env.players:
                if player.lives:
                    continue
                x, y, distance = self.tools.process_distance(player, self)
                if target is None or d_objective > distance:
                    if not x and not y:
                        return None, None
                    d_objective = distance
                    x_objective = x
                    y_objective = y
                    target = player
            for monster in self.env.monsters:
                if monster.lives:
                    continue
                x, y, distance = self.tools.process_distance(monster, self)
                if target is None or d_objective > distance:
                    if not x and not y:
                        return None, None
                    d_objective = distance
                    x_objective = x
                    y_objective = y
                    target = monster
        return x_objective, y_objective, d_objective, target

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            if self.lives >= self.lives_big and self.lives - attack < self.lives_big:
                self.hitbox = self.hitbox_small.update_coords(self)
                self.attack = 1
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.id_nb, 1
        return None, None

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                if self.lives and self.lives < self.max_lives and not self.stoned and not player.lives:
                    if self.lives < self.lives_big and self.lives + 1 == self.lives_big:
                        self.hitbox = self.hitbox_big.update_coords(self)
                        self.attack = 2
                    self.lives += 1
                player.hitted(attack=self.attack)

        if self.lives and self.lives < self.lives_big and not self.stoned:
            for monster in self.env.monsters:
                if not monster.lives and monster.affected(self):
                    if self.lives < self.lives_big and self.lives + 1 == self.lives_big:
                        self.hitbox = self.hitbox_big.update_coords(self)
                        self.attack = 2
                    self.lives += 1
                    monster.degeneration = monster.degeneration - 25 if monster.degeneration > 25 else 0

    def is_healed(self):
        if self.lives and self.lives < self.max_lives:
            if self.lives < self.lives_big and self.lives + 10 >= self.lives_big:
                self.hitbox = self.hitbox_big.update_coords(self)
                self.attack = 2
            self.lives = self.lives + 10 if self.lives + 10 < self.max_lives else self.max_lives
            self.healed = 18

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.lives >= self.lives_big:
            if self.injured:
                img = self.img_big_injured[self.direction]
            elif self.healed:
                self.healed -= 1
                img = self.img_big_healed[self.direction]
            else:
                img = self.img_big[self.direction]
        else:
            if self.injured:
                img = self.img_injured[self.direction]
            elif self.healed:
                self.healed -= 1
                img = self.img_healed[self.direction]
            else:
                img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            if self.lives < self.lives_big:
                self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
            else:
                self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        self._debug()

