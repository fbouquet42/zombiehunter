from . import DefaultWeapon
from threading import Thread

class   Aguni(DefaultWeapon):
    name = 'aguni'

    def __init__(self, env, player):
        self.tools = env.mod.tools

        self.player = player
        self.dimensions = player.dimensions

        self.delay = 13
        self.cooldown = 0
        self.fury = 0
        self.player_lives = player.lives

        self.img_calm = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_calm', self.dimensions)
        self.img_enraged = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_enraged', self.dimensions)
        self.tooth = env.mod.bullets.Tooth.build_class(env, player, self)
        self.devil_tooth = env.mod.bullets.DevilTooth.build_class(env, player, self)

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
            self.fury -= 1
            if not self.fury:
                self.player.rage = False
        elif self.player_lives < self.player.lives:
            self.player.lives = self.player.lives
        elif self.player_lives > self.player.lives:
            self.fury = 180
            self.player.rage = True
