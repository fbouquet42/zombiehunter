#Python Lib
from threading import Thread

#Local Module
import .tools
import .bullets
import .weapons
import .monsters
import .menus

class Env:
    def set_imgs(self):
        self.background_basic = self.mod.tools.load_img(self, 'background_basic', self.width, self.height)
        self.background_hell = self.mod.tools.load_img(self, 'background_hell', self.width, self.height)
        self.main_title = self.mod.tools.load_img(self, 'main_title', self.player_dimensions * 4, self.player_dimensions * 4)
        self.title_position = (0.2 * self.width, 0.05 * self.height)
        env.background = env.background_basic

    def __init__(self, width, height, img_folder, player_dimensions):
        ###Debug
        self.debug = False

        env.closed = False

        ###Paths
        self.img_folder = img_folder

        ###Size
        self.width = width
        self.height = height

        ###Menus
        self.pause = False
        self.quit = False

        ###Modules
        class   LocalModules:
            tools = tools
            bullets = bullets
            weapons = weapons
            monsters = monsters
            menus = menus

        self.mod = LocalModules

        ###Game
        self.player_dimensions = player_dimensions
        #Explosion
        self.jerk = False
        #Daemon
        self.furious = 0
        #Necromancer
        self.walking_dead = 0

        ###Data
        self.players =[]
        self.monsters = []
        self.bullets = []
        self.titles = []

        #Set Images
        self.set_imgs()

    def start(self):
        update_tick = Thread(target=events.update_tick, args=(self, ))
        update_tick.daemon = True
        spawner = Thread(target=events.wave_1, args=(self, ))
        spawner.daemon = True
        update_tick.start()
        spawner.start()

    def usage(self):
        print("usage: python3 main.py [-debug]")

    def parsing(self, argv):
        if len(argv) == 1:
            return
        elif argv[1] == "-debug":
            self.debug = True
        else:
            self.usage()
    def display(self):
        self.GameWindow.blit(self.background, (0, 0))
        self.mod.events.display(self)
