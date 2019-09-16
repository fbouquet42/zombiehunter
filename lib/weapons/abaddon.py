from . import DefaultWeapon
from threading import Thread

class   Abaddon(DefaultWeapon):
    first = 16
    second = 25
    third = 30
    big = 56
    explodes = 72
    name = 'abaddon'

    def __init__(self, env, player):
        self.tools = env.mod.tools
        self.dimensions = player.dimensions

        self.player = player
        self.env = env

        self.loading = 0
        self.delay = 0

        self.img_empty = self.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_empty", self.dimensions)
        self.img_first = self.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_1", self.dimensions)
        self.img_second = self.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_2", self.dimensions)
        self.img_third = self.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_3", self.dimensions)
        self.img_big = self.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_big", self.dimensions)

        self.ball = env.mod.bullets.FireBall.build_class(env, player)
        self.explosion = env.mod.bullets.DevilExplosion.build_class(env, player)

    def display(self, env, direction, x, y, fitting):
        if self.loading > self.big:
            img = self.img_big[direction]
        elif self.loading > self.third:
            img = self.img_third[direction]
        elif self.loading > self.second or self.delay > 4:
            img = self.img_second[direction]
        elif self.loading > self.first or self.delay:
            img = self.img_first[direction]
        else:
            img = self.img_empty[direction]
        self.tools.display(env, img, x, y, fitting)

    def _explose(self):
        explosion = self.explosion(self.player.x, self.player.y, self.player.direction)
        t = Thread(target=explosion.explose, args=())
        t.daemon = True
        self.env.bullets.append(explosion)
        t.start()

    def pressed(self, env, player):
        self.loading += 1
        if self.loading > self.explodes:
            self.loading = 0
            self._explose()

    def not_pressed(self, env, player):
        if self.loading > self.third:
            self._shoot(env, player, self.ball)
            self.delay = 7
        elif self.loading > self.second:
            self._shoot(env, player, self.ball)
            self.delay = 3
        elif self.loading > self.first:
            self._shoot(env, player, self.ball)
        self.loading = 0

    def update(self):
        if not self.delay:
            return
        self.delay -= 1
        if not self.delay % 4:
            self._shoot(self.env, self.player, self.ball)
