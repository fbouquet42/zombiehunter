#library
import pygame
import time

#local lib
from env import Env
import events
import menu

#initialization
pygame.init()
env = Env(width=1366, height=768, img_src='img/', player_dimensions=180, debug=True)

env.GameManager = pygame.display.set_mode((env.width,env.height))
pygame.display.set_caption('Zombie Hunters')

env.background_basic = pygame.image.load(env.img_src + 'background_basic.png')
env.background_hell = pygame.image.load(env.img_src + 'background_hell.png')
env.background = env.background_basic

clock = pygame.time.Clock()

#players initialization
crashed = menu.mainmenu(env, clock)

#Start the game
if not crashed:
    env.start()

#loop game
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    env.pressed = pygame.key.get_pressed()
    if env.pressed[pygame.K_ESCAPE]:
        menu.pausemenu(env)
    elif not env.pause:
        env.GameManager.blit(env.background, (0, 0))
        events.display(env)
        pygame.display.update()
        if not env.players_alive:
            break
        clock.tick(40)

if not crashed:
    menu.endmenu(env, clock)
pygame.quit()
quit()
