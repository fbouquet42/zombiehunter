from . import DefaultWeapon
from threading import Thread

class   AguniUp(DefaultWeapon):
    name = 'aguni_tier2'
    tier_up = True

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_calm = cls.tools.set_imgs(env.img_folder + 'weapons/', 'aguni_calm_tier2', cls.dimensions)
        cls.img_enraged = cls.tools.set_imgs(env.img_folder + 'weapons/', 'aguni_enraged_tier2', cls.dimensions)

        env.mod.bullets.ToothUp.pre_build(env)
        env.mod.bullets.DevilToothUp.pre_build(env)

    def __init__(self, env, player):
        self.player = player

        self.delay = 12
        self.cooldown = 0
        self.fury = 0
        self.player_lives = player.lives

        self.tooth = env.mod.bullets.ToothUp.build_class(env, player, self)
        self.devil_tooth = env.mod.bullets.DevilToothUp.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if not self.fury:
            img = self.img_calm[direction]
        else:
            img = self.img_enraged[direction]
        self.tools.display(env, img, x, y, fitting)

    def _greatShoot(self, env, player, bullet):
        left = bullet(player.x, player.y, player.direction, 0)
        obj = bullet(player.x, player.y, player.direction, 1)
        right = bullet(player.x, player.y, player.direction, 2)
        l = Thread(target=left.move, args=())
        t = Thread(target=obj.move, args=())
        r = Thread(target=right.move, args=())
        l.daemon = True
        t.daemon = True
        r.daemon = True
        env.bullets.append(left)
        env.bullets.append(obj)
        env.bullets.append(right)
        l.start()
        t.start()
        r.start()

    def pressed(self, env, player):
        if self.cooldown:
            return
        self.cooldown = self.delay
        if not self.fury:
            self._shoot(env, player, self.tooth)
        else:
            self._greatShoot(env, player, self.devil_tooth) 

    def update(self):
        if self.cooldown:
            self.cooldown -= 1
        if self.fury:
            if self.player_lives > self.player.lives:
                self.player_lives = self.player.lives
                self.fury = 197
            self.fury -= 1
            if not self.fury:
                self.player.rage = False
            if not self.player.lives:
                self.fury = 0
        elif self.player_lives < self.player.lives:
            self.player_lives = self.player.lives
        elif self.player_lives > self.player.lives:
            self.fury = 176
            self.player.rage = True
