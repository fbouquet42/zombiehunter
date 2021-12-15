import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Thorns(DefaultBullet):
    lifetime = 25
    attack = 2
    poison = 140

    def build_class(env):
        Thorns.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "thorns", env.player_dimensions)
        Thorns.img_warning = env.mod.tools.set_imgs(env.img_folder + "bullets/", "thorns_warning", env.player_dimensions)
        return Thorns

    def __init__(self, x, y, direction, monster, timer):
        super().__init__(x, y, direction)
        self.monster = monster
        self.hitbox = set_hitbox_bullet(self.env, self, 0.88)
        self.timer = timer

    def display(self, env):
        if not self.timer and not self.monster.thorny:
            self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        else:
            self.tools.display(env, self.img_warning[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                if player.lives:
                    player.poisoned = self.poison
        for monster in self.env.monsters:
            if not monster.forest and monster.affected(self):
                monster.hitted(attack=self.attack)
                monster.poisoned = self.poison

    def explose(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            if self.monster.thorny:
                pass
            elif self.timer:
                self.timer -= 1
            else:
                self._target_hitted()
                self.lifetime -= 1
            if not self.lifetime or not self.monster.lives:
                return self._dead()
            if self._quit():
                return

