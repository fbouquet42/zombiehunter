#Python Lib
import time
import sys
import os
import pygame
pygame.init()

#Local Lib
from lib import Env

#TOADJUST: machinegun? explosion? waves? bosslive?
pwd = os.path.dirname(os.path.realpath(__file__))
env = Env(sys.argv, pwd)

clock = pygame.time.Clock()

#Welcome Menu
env.mod.menus.welcome(env)

#Start the game
if not env.closed:
    env.start()

#loop game
while not env.closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.closed = True

    env.display()
    pygame.display.update()

    if env.pause:
        env.mod.menus.pause(env)
    if env.closed:
        pass
    elif not env.players_alive:
        env.mod.menus.game_over(env)
    elif env.credits:
        env.mod.menus.credits(env)
    clock.tick(30)

pygame.quit()
quit()
