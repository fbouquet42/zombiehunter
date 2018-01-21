import multiprocessing as mp
from threading import Thread
import events
import monsters

class Env:
    def __init__(self, width, height, img_src, player_dimensions, debug=False):
        self.debug = debug
        self.score = 0
        self.width = width
        self.height = height
        self.player_dimensions = player_dimensions
        self.pause = False
        self.img_src = img_src
        self.jerk = False
        self.players =[]
        self.monsters = []
        self.bullets = []
        self.zombie = monsters.Zombie.build_class(self)

    def start(self):
        update_tick = Thread(target=events.update_tick, args=(self, ))
        update_tick.daemon = True
        spawner = Thread(target=events.spawner, args=(self, ))
        spawner.daemon = True
        update_tick.start()
        spawner.start()

    def spawn(self, x, y):
        zombie = monsters.Zombie(self, x, y)
        t = Thread(target=zombie.move, args=())
        t.daemon = True
        self.monsters.append(zombie)
        t.start()
