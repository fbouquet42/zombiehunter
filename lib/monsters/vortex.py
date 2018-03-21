#Current Module
from . import DefaultMonster


class Vortex(DefaultMonster):
    name = "vortex"
    rapidity = 8

    @classmethod
    def build_class(cls, env, boss):
        cls.env = env
        cls.tools = env.mod.tools
        cls.players = env.players
        cls.monsters = env.monsters
        cls.boss = boss
        cls.dimensions = boss.dimensions

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _pull(self, target):
        x, y, _ = self.tools.process_distance(self, target)
        self.tools.force_move(target, x, y, direction=0, rapidity=self.rapidity if target.rapidity > self.rapidity else 2, set_direction=False)
        target.hitbox.update_coords(target)

    def update(self):
        self.tick = self.tools.Tick()
        while self.boss.spelling:
            for player in self.players:
                self._pull(player)
            for monster in self.monsters:
                if not monster.rooted:
                    self._pull(monster)
            if self._quit():
                return
