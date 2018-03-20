from threading import Thread

from . import Tentacle

class BaseTentacles:
    def __init__(self, env, monster, identity):
        self.half = monster.half
        self.pos = int(monster.half * 0.8)
        self.env = env
        self.tools = env.mod.tools
        self.monster = monster
        self.id = identity
        self.target = env.players[0]
        self.update()

        self.tentacles = []
        for i in range(0, 6):
            self.growing()

    def _find_target(self):
        d_objective = -1
        target = None
        x_objective = 0
        y_objective = 0
        for player in self.env.players:
            if not player.lives:
                continue
            x, y, distance = self.tools.process_distance(player, self)
            if target is None or d_objective > distance:
                if not x and not y:
                    return None, None
                d_objective = distance
                x_objective = x
                y_objective = y
                target = player
        return target

    def _kill_tentacles(self):
        i = 0
        while i != len(self.tentacles):
            if not self.tentacles[i].lives:
                del self.tentacles[i]
            else:
                i += 1

    def spore_popping(self):
        self._kill_tentacles()
        if not len(self.tentacles):
            self.growing()
        self.tentacles[0].spore = True

    def growing(self):
        self._kill_tentacles()
        if len(self.tentacles):
            tentacle = Tentacle(self.env, self.monster, self, self.tentacles[0].x, self.tentacles[0].y, len(self.tentacles))
            self.tentacles[0].following = True
            self.tentacles[0].target = tentacle
            if self.tentacles[0].spore:
                self.tentacles[0].spore = False
                tentacle.sporing = self.tentacles[0].sporing
                tentacle.spore = True
                self.tentacles[0].loading()
        else:
            tentacle = Tentacle(self.env, self.monster, self, self.x, self.y, 0)
        t = Thread(target=tentacle.move, args=())
        t.daemon = True
        self.env.monsters.append(tentacle)
        t.start()
        self.tentacles.insert(0, tentacle)

    def update(self):
        if self.id < 3:
            self.x = self.monster.x - self.pos
        else:
            self.x = self.monster.x + self.pos
        if self.id % 2:
            self.y = self.monster.y - self.pos
        else:
            self.y = self.monster.y + self.pos
        target = self._find_target()
        if target is not None:
            self.target = target
