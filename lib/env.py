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
        self.credits = False
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
        self.player_dimensions = int(self.width / 7.6)
        #Explosion
        self.jerk = False
        #Daemon
        self.furious = 0
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
        self.GameWindow = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

    def start_players(self):
        keys_managers = []
        for player in self.players:
            t = Thread(target=self.mod.events.keys_manager, args=(self, player,))
            t.daemon = True
            keys_managers.append(t)

        for t in keys_managers:
            t.start()

    def start(self):
        update_tick = Thread(target=self.mod.events.update_tick, args=(self, ))
        update_tick.daemon = True
        spawner = Thread(target=self.mod.waves.loop, args=(self, ))
        spawner.daemon = True

        update_tick.start()
        spawner.start()

    def clear(self):
        self.monsters.clear()
        for player in self.players:
            player.destroy = True
        self.players.clear()
        self.bullets.clear()
        self.jerk = False
        self.furious = 0
        self.walking_dead = 0
        self.retry = 1

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
                    if self.debug_wave < 1 or self.debug_wave > len(self.mod.monsters.tab):
                        self.debug_wave = 1
                except ValueError:
                    self.debug_wave = 1
        else:
            self.usage()

    def display(self):
        self.GameWindow.blit(self.background, (0, 0))
        self.mod.events.display(self)
