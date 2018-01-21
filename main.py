#library
import pygame
import time

#local lib
from env import Env
import events
import menu

#initialization
pygame.init()
env = Env(width=1366, height=768, img_src='src/', player_dimensions=180, debug=False)

env.GameManager = pygame.display.set_mode((env.width,env.height))
pygame.display.set_caption('Zombie Hunters')

env.background = pygame.image.load(env.img_src + 'background_basic.png')

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
        env.pause = not env.pause
    elif not env.pause:
        env.GameManager.blit(env.background, (0, 0))
        events.display(env)
        pygame.display.update()
        clock.tick(40)
pygame.quit()
quit()
