from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Tentacle


class _BaseTentacles:
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

    def growing(self):
        i = 0
        while i != len(self.tentacles):
            if not self.tentacles[i].lives:
                del self.tentacles[i]
            else:
                i += 1
        if len(self.tentacles):
            tentacle = Tentacle(self.env, self.monster, self, self.tentacles[0].x, self.tentacles[0].y, len(self.tentacles))
            self.tentacles[0].following = True
            self.tentacles[0].target = tentacle
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

class Kraken(DefaultMonster):
    name = "kraken"
    lives = 1710
    #450 570 690
    # + 3 necromancer spawns
    rapidity = 4
    attack = 3
    id_nb = 8
    degeneration = 550

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)

        self.hitbox = set_hitbox_monster(env, self, 0.7)
        Tentacle.build_class()
        self.tentacles_headers = []
        for i in range(1, 5):
            self.tentacles_headers.append(_BaseTentacles(env, self, i))

        self.next_enlargement()

    def next_enlargement(self):
        self.expand = randint(100, 230)

    def growing(self):
        for tentacles_header in self.tentacles_headers:
            tentacles_header.growing()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
#        elif self.furious:
#            img = self.img_furious[self.direction]
#        elif self.spelling:
#            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        self._debug()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            for tentacles_header in self.tentacles_headers:
                tentacles_header.update()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
                for tentacles_header in self.tentacles_headers:
                    tentacles_header.update()
            if self._quit():
                return

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if not self.lives:
            pass
        elif self.expand:
            self.expand -= 1
        else:
            self.growing()
            self.next_enlargement()
