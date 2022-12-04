#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   PoisonedGasLarge(DefaultBullet):
    rapidity = 8
    attack = 1
    name = "poisoned_gas_large"
    poison = 100
    ultimatum = 80

    @classmethod
    def build_class(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        return cls

    def __init__(self, x, y, direction, monster):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.24)
        self.monster = monster
        self.tools.move(self, self.direction)
    
    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                player.poisoned = self.poison
                ret = True
        return ret

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.tools.move(self, self.direction)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            self._target_hitted() #return doesnt matter
            self.ultimatum -= 1
            if not self.ultimatum:
                return self._dead()
            if self._quit():
                return
