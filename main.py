#library
import pygame
import time

#local lib
from env import Env
from players import Player
import events

#initialization
pygame.init()
env = Env(width=1366, height=768, img_src='src/', player_dimensions=180, debug=False)

env.GameManager = pygame.display.set_mode((env.width,env.height))
pygame.display.set_caption('Zombie Hunters')

env.background = pygame.image.load(env.img_src + 'background_basic.png')

clock = pygame.time.Clock()

#players initialization
env.players.append(Player(env=env, x=0.25, y=0.5, dimensions=env.player_dimensions, name='jack', keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE)))
env.players.append(Player(env=env, x=0.75, y=0.5, dimensions=env.player_dimensions, name='baltazar', keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_RETURN)))

env.start()
#loop game
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    env.pressed = pygame.key.get_pressed()
    if env.pressed[pygame.K_ESCAPE]:
        env.pause = not env.pause
        if env.pause:
            print("Score: %i" % (env.score))
    elif not env.pause:
        env.GameManager.blit(env.background, (0, 0))
        events.display(env)
        pygame.display.update()
        clock.tick(40)
pygame.quit()
quit()
