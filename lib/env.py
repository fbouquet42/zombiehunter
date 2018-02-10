#Python Lib
from threading import Thread
import pygame

#Local Module
import tools
import bullets
import weapons
import monsters

class Env:
    def __init__(self, width, height, img_folder, player_dimensions, debug=False):
        ###Debug
        self.debug = debug

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

        self.mod = LocalModules

        ###Game
        self.player_dimensions = player_dimensions
        class   Game:
            #Explosion
            self.jerk = False
            #Daemon
            self.furious = 0
            #Necromancer
            self.walking_dead = 0

        self.game = Game

        ###Data
        self.players =[]
        self.monsters = []
        self.bullets = []
        self.titles = []


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
