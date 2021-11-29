
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class GiantSpider(DefaultMonster):
    max_lives = 260
    lives = 260
    name = "giant_spider"
    id_nb = 18
    degeneration = 500
    insect = True #I know it's not the case but unless you know python, you don't know I write that

    @classmethod
    def build_class(cls):
        cls.sniff = int(cls.dimensions * 2)
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_healed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_healed', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_burried = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_burried', cls.dimensions)
        cls.img_burried_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_burried_injured', cls.dimensions)
        cls.img_burried_healed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_burried_healed', cls.dimensions)
        cls.img_burried_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_burried_dead', cls.dimensions)
        cls.img_burried_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_burried_possessed', cls.dimensions)
        return cls


    class   Target:
        is_player = False
        def __init__(self, env, half, sniff):
            self.x = randint(sniff, env.width - (sniff + half))
            self.y = randint(sniff, env.height - (sniff + half))
            self.half = half

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.env = env
        self.hitbox_small = set_hitbox_monster(env, self)
        self.hitbox_big = set_hitbox_monster(env, self, 0.46)
        self.hitbox = self.hitbox_big

        self.rapidity = randint(4, 8)
        self.rapidity = 5 if self.rapidity < 5 else self.rapidity

        self.burried = False
        self.healed = 0
        self.target = self.Target(env, self.half, self.sniff)

    def is_healed(self):
        if self.lives and self.lives < self.max_lives:
            self.lives = self.lives + 10 if self.lives + 10 < self.max_lives else self.max_lives
            self.healed = 18

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            self.injured = 12
            if self.burried:
                self.lives -= attack // 2
                self.lives = 0 if self.lives < 0 else self.lives
                return self.id_nb, attack // 2
            else:
                self.lives -= attack
                self.lives = 0 if self.lives < 0 else self.lives
                return self.id_nb, attack
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
        if not self.burried and not self.target.is_player and d_objective > self.sniff:
            x, y, distance = self.tools.process_distance(self.target, self)
            return x, y, distance, self.target

        return x_objective, y_objective, d_objective, target

    def _action(self):
        if not self.stoned:
            direction, distance = self._sniff_fresh_flesh()
            if direction is None:
                return
            self.direction = direction
            if distance <= self.sniff:
                if not self.target.is_player:
                    self.burried = True
                    self.hitbox = self.hitbox_small.update_coords(self)
                else:
                    if self.burried:
                        self.burried = False
                        self.hitbox = self.hitbox_big.update_coords(self)
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                    self.hitbox.update_coords(self)
            elif self.target.is_player:
                self.burried = True
                self.hitbox = self.hitbox_small.update_coords(self)
            else:
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)

        self._target_hitted()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.burried:
                if self.env.walking_dead:
                    img = self.img_burried_possessed[self.direction]
                else:
                    img = self.img_burried_dead[self.direction]
            else:
                if self.env.walking_dead:
                    img = self.img_possessed[self.direction]
                else:
                    img = self.img_dead[self.direction]
        elif self.burried:
            if self.injured:
                img = self.img_burried_injured[self.direction]
            elif self.healed:
                self.healed -= 1
                img = self.img_burried_healed[self.direction]
            else:
                img = self.img_burried[self.direction]
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
            if self.burried:
                self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
            else:
                self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        self._debug()

