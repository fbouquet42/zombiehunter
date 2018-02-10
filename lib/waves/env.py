from threading import Thread
import events
import monsters
import pygame

class Env:
    def __init__(self, width, height, img_folder, player_dimensions, debug=False):
        self.debug = debug
        self.width = width
        self.height = height
        self.player_dimensions = player_dimensions
        self.pause = False
        self.quit = False
        self.img_folder = img_folder
        self.jerk = False
        self.walking_dead = 0

        import tools
        self.tools = tools


        self.furious = 0
        self.fire_star = 0
        self.players =[]
        self.monsters = []
        self.bullets = []
        self.titles = []
        self.monster_type = {}
        self.monster_type['zombie'] = monsters.Zombie.build_class(self)
        self.monster_type['cyclops'] = monsters.Cyclops.build_class(self)
        self.monster_type['jack_lantern'] = monsters.JackLantern.build_class(self)
        self.monster_type['minion'] = monsters.Minion.build_class(self)
        self.monster_type['necromancer'] = monsters.Necromancer.build_class(self)
        self.monster_type['harpy'] = monsters.Harpy.build_class(self)
        self.main_title = pygame.image.load(self.img_src + "main_title.png")
        self.main_title = pygame.transform.scale(self.main_title, (self.player_dimensions * 4, self.player_dimensions * 4))
        self.title_position = (0.2 * self.width, 0.05 * self.height)

    def start(self):
        update_tick = Thread(target=events.update_tick, args=(self, ))
        update_tick.daemon = True
        spawner = Thread(target=events.wave_5, args=(self, ))
        spawner.daemon = True
        update_tick.start()
        spawner.start()

    def spawn_boss(self):
        x = randint(-200, 0)
        y = randint(-200, 0)
        boss = monsters.Daemon(self, x, y)
        t = Thread(target=boss.move, args=())
        t.daemon = True
        self.monsters.append(boss)
        t.start()
        return boss

    def spawn(self, name, nb=1):
        while nb:
            x = randint(-200, 0)
            y = randint(-200, 0)
            monster = self.monster_type[name](self, x, y)
            t = Thread(target=monster.move, args=())
            t.daemon = True
            self.monsters.append(monster)
            t.start()
            nb -= 1
