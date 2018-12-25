from . import DefaultWeapon
from threading import Thread

class   Aguni(DefaultWeapon):
    name = 'aguni'

    def __init__(self, env, player):
        self.tools = env.mod.tools

        self.dimensions = player.dimensions

        self.delay = 11
        self.cooldown = 0
        self.rage = 99
        self.count = 0

        self.img_calm = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_calm', self.dimensions)
        self.img_angry = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_angry', self.dimensions)
        self.img_enraged = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_enraged', self.dimensions)
        self.tooth = env.mod.bullets.Tooth.build_class(env, player, self)
        self.devil_tooth = env.mod.bullets.DevilTooth.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.rage < 5:
            img = self.img_calm[direction]
        elif self.rage < 9:
            img = self.img_angry[direction]
        else:
            img = self.img_enraged[direction]
        self.tools.display(env, img, x, y, fitting)

    def bringOn(self):
        self.rage += 1

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
        if self.rage < 9:
            self._shoot(env, player, self.tooth)
        else:
            if self.count < 2:
                self.count += 1
            else:
                self.rage = 0
                self.count = 0
            self._greatShoot(env, player, self.devil_tooth) 

    def update(self):
        if self.cooldown:
            self.cooldown -= 1
