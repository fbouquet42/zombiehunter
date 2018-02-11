#Python Lib
import sys
import pygame
pygame.init()

#Local Lib
from lib import Env
import init

#TOADJUST: machinegun? explosion? waves? bosslive?
env = init.init(Env, sys.argv)
clock = pygame.time.Clock()

#Start the game
if not env.closed:
    env.start()

#loop game
while not env.closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.closed = True

    env.pressed = pygame.key.get_pressed()

    if env.pressed[pygame.K_ESCAPE]:
        env.mod.menus.pause(env)

    env.display()
    pygame.display.update()

    if not env.players_alive:
        env.closed = env.mod.menus.dead()
    clock.tick(40)

pygame.quit()
