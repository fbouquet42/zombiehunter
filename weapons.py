import tools
import pygame
import bullets
from threading import Thread

class   Weapon:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def update(self, **kwargs):
        pass

    def not_pressed(self, **kwargs):
        pass

class   SubmachineGun(Weapon):
    def __init__(self, env, player):
        super().__init__(player.dimensions)
        self.delay = 8
        self.heatup = self.delay * 4.5
        self.heatmax = self.heatup * 10 - self.delay * 9
        self.degree_1 = self.heatup * 4 - self.delay * 4
        self.degree_2 = self.heatmax - self.heatup * 2
        self.cooldown = 0
        self.overheating = False
        self.temperature = 0
        self.img = []
        self.img.append(tools.set_imgs(env.img_src + 'weapons/', "submachine_gun_0", self.dimensions))
        self.img.append(tools.set_imgs(env.img_src + 'weapons/', "submachine_gun_1", self.dimensions))
        self.img.append(tools.set_imgs(env.img_src + 'weapons/', "submachine_gun_2", self.dimensions))
        self.img.append(tools.set_imgs(env.img_src + 'weapons/', "submachine_gun_3", self.dimensions))
        self.bullet = bullets.Bullet.build_class(env, player)

    def display(self, env, direction, x, y, fitting):
        if not self.overheating:
            if self.temperature < self.degree_1:
                img = self.img[3][direction]
            elif self.temperature < self.degree_2:
                img = self.img[2][direction]
            else:
                img = self.img[1][direction]
        else:
            img = self.img[0][direction]
        tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        if self.cooldown:
            return
        self.temperature += self.heatup
        if self.temperature > self.heatmax:
            self.temperature += (self.heatup // 2)
            self.cooldown += self.temperature + 4
            self.overheating = True
        else:
            self.cooldown += self.delay
        bullet = self.bullet(player.x, player.y, player.direction)
        t = Thread(target=bullet.move, args=())
        t.daemon = True
        env.bullets.append(bullet)
        t.start()

    def update(self):
        if self.temperature:
            self.temperature -= 1
        else:
            self.overheating = False
        if self.cooldown:
            self.cooldown -= 1
            

class   Crossbow(Weapon):
    def __init__(self, env, player):
        super().__init__(player.dimensions)
        self.loading = 0
        self.loaded = 17
        self.overloaded = 114
        self.img_unloaded = tools.set_imgs(env.img_src + 'weapons/', "crossbow_unloaded", self.dimensions)
        self.img_loaded = tools.set_imgs(env.img_src + 'weapons/', "crossbow_loaded", self.dimensions)
        self.img_overloaded = tools.set_imgs(env.img_src + 'weapons/', "crossbow_overloaded", self.dimensions)
        self.arrow = bullets.Arrow.build_class(env, player)
        self.rocket = bullets.Rocket.build_class(env, player)

    def display(self, env, direction, x, y, fitting):
        if self.loading > self.overloaded:
            img = self.img_overloaded[direction]
        elif self.loading > self.loaded:
            img = self.img_loaded[direction]
        else:
            img = self.img_unloaded[direction]
        tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        self.loading += 1

    def not_pressed(self, env, player):
        if self.loading > self.overloaded:
            rocket = self.rocket(player.x, player.y, player.direction)
            t = Thread(target=rocket.move, args=())
            t.daemon = True
            env.bullets.append(rocket)
            t.start()
        elif self.loading > self.loaded:
            arrow = self.arrow(player.x, player.y, player.direction)
            t = Thread(target=arrow.move, args=())
            t.daemon = True
            env.bullets.append(arrow)
            t.start()
        self.loading = 0

weapons = {'jack' : Crossbow, 'baltazar' : SubmachineGun}

def set_weapon(env, player):
    return weapons[player.name](env=env, player=player)
