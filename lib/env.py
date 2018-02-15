#Python Lib
import pygame
from threading import Thread

#Local Module
from . import tools
from . import bullets
from . import weapons
from . import monsters
from . import players
from . import menus
from . import events
from . import waves

class Env:
    def set_imgs(self):
        self.background_basic = self.mod.tools.load_img(self, 'background_basic', self.width, self.height)
        self.background_hell = self.mod.tools.load_img(self, 'background_hell', self.width, self.height)
        self.background = self.background_basic

    def __init__(self, argv, pwd):
        ##Init
        info = pygame.display.Info()

        ###Debug
        self.debug = False
        self.debug_wave = 1

        self.closed = False

        ###Paths
        self.pwd = pwd
        self.img_folder = pwd + '/img/'

        ###Size
        self.width = info.current_w
        self.height = info.current_h

        ###Menus
        self.retry = 1
        self.pause = False
        self.quit = False

        ###Modules
        class   LocalModules:
            tools = tools
            bullets = bullets
            weapons = weapons
            monsters = monsters
            players = players
            menus = menus
            events = events
            waves = waves

        self.mod = LocalModules

        ###Game
        self.player_dimensions = self.width // 8
        #Explosion
        self.jerk = False
        #Daemon
        self.furious = False
        #Necromancer
        self.walking_dead = 0

        ###Data
        self.players = []
        self.monsters = []
        self.bullets = []
        self.titles = []

        #Set Images
        self.set_imgs()

        #Build DefaultWeapon
        self.mod.weapons.DefaultWeapon.build_class(self)

        self.parsing(argv)
        self.pressed = (0,) * 323
        self.GameWindow = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

    def start(self):
        update_tick = Thread(target=self.mod.events.update_tick, args=(self, ))
        update_tick.daemon = True
        keys_manager = Thread(target=self.mod.events.keys_manager, args=(self, ))
        keys_manager.daemon = True
        spawner = Thread(target=self.mod.waves.loop, args=(self, ))
        spawner.daemon = True
        keys_manager.start()
        update_tick.start()
        spawner.start()

    def clear(self):
        self.monsters.clear()
        self.players.clear()
        self.bullets.clear()
        self.jerk = False
        self.furious = False
        self.walking_dead = 0
        self.retry = 1
        self.pressed = (0,) * 323

    def usage(self):
        print("usage: python3 main.py [-debug [wave_nb]]")

    def parsing(self, argv):
        if len(argv) == 1:
            return
        elif argv[1] == "-debug":
            self.debug = True
            if len(argv) > 2:
                try:
                    self.debug_wave = int(argv[2])
                    if self.debug_wave < 0 or self.debug_wave >= len(self.mod.monsters.tab):
                        self.debug_wave = 1
                except ValueError:
                    self.debug_wave = 1
        else:
            self.usage()

    def display(self):
        self.GameWindow.blit(self.background, (0, 0))
        self.mod.events.display(self)