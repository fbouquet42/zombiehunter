#Current Module
from . import DefaultMonster


class Vortex(DefaultMonster):
    name = "zombie"
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
        direction = self._determine_direction(x, y)
        self.tools.move(target, direction, rapidity=self.rapidity, set_direction=False)
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
