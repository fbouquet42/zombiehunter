import pygame
from .env import Env

info = pygame.display.Info

env = Env(width=info.current_w, height=info.current_h, img_folder='img/', player_dimensions=info.current_w // 7)

env.GameWindow = pygame.display.set_mode((env.width, env.height), pygame.FULLSCREEN)
pygame.display.set_caption('Zombie Hunters')

env.menus.welcome(env)
