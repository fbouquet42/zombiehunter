from . import DefaultWeapon
from threading import Thread

class   AbaddonUp(DefaultWeapon):
    first = 15
    second = 23
    third = 27
    fourth = 30
    fifth = 33
    big = 56
    explodes = 72
    name = 'abaddon_tier2'
    tier_up = True

    @classmethod
    def pre_build(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_empty = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_empty_tier2", cls.dimensions)
        cls.img_first = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_tier2_1", cls.dimensions)
        cls.img_second = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_tier2_2", cls.dimensions)
        cls.img_third = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_tier2_3", cls.dimensions)
        cls.img_fourth = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_tier2_4", cls.dimensions)
        cls.img_fifth = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_tier2_5", cls.dimensions)
        cls.img_big = cls.tools.set_imgs(env.img_folder + 'weapons/', "abaddon_big_tier2", cls.dimensions)
        cls.img_night = cls.tools.set_imgs(env.img_folder + 'players/', "abaddon_tier2_night", cls.dimensions)
        cls.img_night_injured = cls.tools.set_imgs(env.img_folder + 'players/', "abaddon_tier2_night_injured", cls.dimensions)
        env.mod.bullets.FireBallUp.pre_build(env)
        env.mod.bullets.DevilExplosionUp.pre_build(env)
        return cls

    def __init__(self, env, player):
        self.player = player
        self.env = env

        self.loading = 0
        self.delay = 0


        self.ball = env.mod.bullets.FireBallUp.build_class(env, player, self)
        self.explosion = env.mod.bullets.DevilExplosionUp.build_class(env, player, self)

        self.player_img_night = self.player.img_night
        self.player_img_injured_night = self.player.img_injured_night
        self.player.img_night = self.img_night
        self.player.img_injured_night = self.img_night_injured
        self.player.img_abaddon = self.player.img_abaddon_tier2
        self.player.img_abaddon_injured = self.player.img_abaddon_tier2_injured

        self.player.max_lives += 41
        self.player.lives += 41
        self.player.hitbox = env.mod.players.set_hitbox_player(env, self.player, 0.46)

    def desequip(self):
        self.player.max_lives -= 82
        self.player.lives -= 82
        self.player.img_night = self.player_img_night
        self.player.img_injured_night = self.player_img_injured_night
        self.hitbox = set_hitbox_player(env, self.player)
        self.player.abaddon = False

    def display(self, env, direction, x, y, fitting):
        if self.loading > self.big:
            img = self.img_big[direction]
        elif self.loading > self.fifth:
            img = self.img_fifth[direction]
        elif self.loading > self.fourth:
            img = self.img_fourth[direction]
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
        if self.loading > self.fifth:
            self._shoot(env, player, self.ball)
            self.delay = 8
        elif self.loading > self.fourth:
            self._shoot(env, player, self.ball)
            self.delay = 6
        elif self.loading > self.third:
            self._shoot(env, player, self.ball)
            self.delay = 4
        elif self.loading > self.second:
            self._shoot(env, player, self.ball)
            self.delay = 2
        elif self.loading > self.first:
            self._shoot(env, player, self.ball)
        self.loading = 0

    def update(self):
        if not self.delay:
            return
        self.delay -= 1
        if not self.delay % 2:
            self._shoot(self.env, self.player, self.ball)
