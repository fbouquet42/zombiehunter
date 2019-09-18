from . import DefaultWeapon
from threading import Thread

#Idea : more life ?

class   Abaddon(DefaultWeapon):
    first = 16
    second = 25
    third = 30
    big = 56
    explodes = 72
    name = 'abaddon'

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_empty = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_empty", cls.dimensions)
        cls.img_first = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_1", cls.dimensions)
        cls.img_second = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_2", cls.dimensions)
        cls.img_third = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_3", cls.dimensions)
        cls.img_big = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_big", cls.dimensions)

        env.mod.bullets.FireBall.pre_build(env)
        env.mod.bullets.DevilExplosion.pre_build(env)

    def __init__(self, env, player):
        self.player = player
        self.env = env

        self.loading = 0
        self.delay = 0


        self.ball = env.mod.bullets.FireBall.build_class(env, player)
        self.explosion = env.mod.bullets.DevilExplosion.build_class(env, player)

        self.player.max_lives += 82
        self.player.lives += 82
        self.player.hitbox = env.mod.players.set_hitbox_player(env, self.player, 0.26)
        self.player.abaddon = True

    def desequip(self):
        self.player.max_lives -= 82
        self.player.lives -= 82
        self.hitbox = set_hitbox_player(env, self.player)
        self.player.abaddon = False

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
            self.delay = 6
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
        if not self.delay % 3:
            self._shoot(self.env, self.player, self.ball)
