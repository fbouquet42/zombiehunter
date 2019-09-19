from . import DefaultWeapon

class   SubmachineGunUp(DefaultWeapon):
    name = 'submachine_gun_tier2'

    def __init__(self, env, player):
        self.tools = env.mod.tools

        self.dimensions = player.dimensions

        self.delay = 4
        self.cooldown = 0
        self.active = False

        self.img = self.tools.set_imgs(env.img_folder + 'weapons/', self.name, self.dimensions)
        self.img_pressed = self.tools.set_imgs(env.img_folder + 'weapons/', self.name + '_pressed', self.dimensions)
        self.bullet = env.mod.bullets.BulletUp.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.active:
            img = self.img_pressed[direction]
        else:
            img = self.img[direction]
        self.tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        if self.cooldown:
            return
        self.active = True
        self.cooldown += self.delay
        self._shoot(env, player, self.bullet)

    def update(self):
        if self.cooldown:
            self.cooldown -= 1

    def not_pressed(self, env, player):
        self.active = False
