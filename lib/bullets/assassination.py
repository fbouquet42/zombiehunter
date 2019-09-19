#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Assassination(DefaultBullet):
    attack=90
    from_player = True
    name = "shadow_daggers"

    def __init__(self, env, player, weapon):
        self.env = env
        self.player = player
        self.weapon = weapon
        self.x = self.player.x
        self.y = self.player.y
        self.hitbox = set_hitbox_bullet(self.env, self, 0.46)

    def process(self):
        self.x = self.player.x
        self.y = self.player.y
        self.hitbox.update_coords(self)
        for monster in self.env.monsters:
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value
                    self.weapon.xp += self.player.score.values[id_nb] * value
