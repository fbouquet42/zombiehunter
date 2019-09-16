from . import DefaultWeapon

class   SubmachineGun(DefaultWeapon):
    name = 'submachine_gun_full'

    def __init__(self, env, player):
        self.tools = env.mod.tools

        self.dimensions = player.dimensions

        self.delay = 5
        self.heatup = self.delay * 12
        self.heatdown = 0.
        self.heatmax = self.heatup * 23
        self.degree_1 = self.heatup * 14
        self.degree_2 = self.heatup * 20

        self.cooldown = 0
        self.overheating = False
        self.temperature = 0

        self.img_red = self.tools.set_imgs(env.img_folder + 'weapons/', "submachine_gun_0", self.dimensions)
        self.img_orange = self.tools.set_imgs(env.img_folder + 'weapons/', "submachine_gun_1", self.dimensions)
        self.img_yellow = self.tools.set_imgs(env.img_folder + 'weapons/', "submachine_gun_2", self.dimensions)
        self.img_green = self.tools.set_imgs(env.img_folder + 'weapons/', "submachine_gun_3", self.dimensions)
        self.img_blue = self.tools.set_imgs(env.img_folder + 'weapons/', "submachine_gun_full", self.dimensions)
        self.bullet = env.mod.bullets.Bullet.build_class(env, player)

    def display(self, env, direction, x, y, fitting):
        if not self.overheating:
            if not self.temperature:
                img = self.img_blue[direction]
            elif self.temperature < self.degree_1:
                img = self.img_green[direction]
            elif self.temperature < self.degree_2:
                img = self.img_yellow[direction]
            else:
                img = self.img_orange[direction]
        else:
            img = self.img_red[direction]
        self.tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        if self.cooldown or self.overheating:
            return
        self.temperature += self.heatup
        if self.temperature > self.heatmax:
            self.temperature += int(self.heatmax * 0.5)
            self.overheating = True
        else:
            self.cooldown += self.delay
        self._shoot(env, player, self.bullet)
        self.heatdown = 0.

    def update(self):
        if self.temperature:
            self.temperature -= int(self.heatdown)
            self.temperature = 0 if self.temperature < 0 else self.temperature
            if self.heatdown >= 9.:
                self.heatdown = 9.
            else:
                self.heatdown += 0.2
        else:
            self.overheating = False
        if self.cooldown:
            self.cooldown -= 1
