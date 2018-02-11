import pygame
import os

from lib import Env

def init(argv):
    pwd = os.path.dirname(os.path.realpath(__file__))
    info = pygame.display.Info()
    env = Env(width=info.current_w, height=info.current_h, pwd=pwd, player_dimensions=info.current_w // 8)
    env.GameWindow = pygame.display.set_mode((env.width, env.height), pygame.FULLSCREEN)
    pygame.display.set_caption('Zombie Hunters')
    env.parsing(argv)
    env.mod.menus.welcome(env)
    return env
