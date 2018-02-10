#Python Lib
from threading import Thread

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   HellStar(DefaultBullet):
    def build_class(env, monster):
        HellStar.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "hell_star", monster.dimensions)
        HellStar.img_off = env.mod.tools.set_imgs(env.img_folder + "bullets/", "hell_star_off", monster.dimensions)
        HellStar.monster = monster
        HellStar.minion = monster.minion
        return HellStar

    def __init__(self, x, y, direction):
        super.__init__(x, y, direction)
        self.summoning = 0
        self.hitbox = set_hitbox_bullet(self.env, self, 0.40)

    def display(self, env):
        if self.summoning and not self.monster.fire_star:
            self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        else:
            self.tools.display(env, self.img_off[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)
    
    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()

    def move(self):
        while True:
            if self.monster.fire_star:
                self.summoning = 600
            if not self.monster.fire_star and self.summoning:
                self._target_hitted()
            if not (self.summoning + 100) % 220:
                monster = self.minion(self.env, self.x, self.y)
                t = Thread(target=monster.move, args=())
                t.daemon = True
                self.env.monsters.append(monster)
                t.start()
            if not self.monster.lives:
                return self._dead()
            if self.summoning:
                self.summoning -= 1
            if self._quit():
                return
