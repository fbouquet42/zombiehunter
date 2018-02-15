import time

from . import DefaultMonster
from . import set_hitbox_monster

class FireBall(DefaultMonster):
    lives = 1
    name = "fire_ball"
    rapidity = 7
    ultimatum = 500
    attack = 20

    def build_class():
        FireBall.img = FireBall.tools.set_imgs(FireBall.env.img_folder + 'bullets/', FireBall.name, FireBall.dimensions)
        FireBall.img_dead = FireBall.tools.set_imgs(FireBall.env.img_folder + 'bullets/', FireBall.name + '_dead', FireBall.dimensions)
        return FireBall

    def __init__(self, env, x, y, target):
        self.x = x
        self.y = y
        self.hitbox = set_hitbox_monster(env, self)

        self.target = target

    def affected(self, bullet):
        return False

    def _target_hitted(self):
        for player in self.env.players:
            if player.lives and player.affected(self):
                player.hitted(attack=self.attack)
                self.ultimatum = 0

    def move(self):
        self.time = time.time()
        while self.ultimatum:
            x, y, _ = self.tools.process_distance(self.target, self)
            self.direction = self._determine_direction(x, y)
            self.tools.move(self, self.direction)
            self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return
            if self.ultimatum:
                self.ultimatum -= 1
            if not self.target.lives:
                self.ultimatum = 0

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.ultimatum:
            img = self.img_dead[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        self._debug()

    def update(self):
        if not self.ultimatum and self.degeneration:
            self.degeneration -= 1
