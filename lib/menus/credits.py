import pygame
import time

#from . import failure
from . import welcome

def credits(env):
    env.quit = True
    credits_title = env.mod.tools.load_img(env, 'menus/' + 'credits_menu', env.height, env.height)
    title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection', env.height, env.height)
    position = [(title_position,0), (title_position, env.height * 0.15), (title_position, env.height * 0.3)]
    up = pygame.K_w
    down = pygame.K_s
    approve = pygame.K_r
    left = pygame.K_a
    right = pygame.K_d

    tick = env.mod.tools.Tick()
    tick.before_loop = tick.time
    action = 2
    exe = False
    for player in env.players:
        player.score.calculate()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.closed = True
                return
        pressed = pygame.key.get_pressed()
        if not exe:
            pass
        elif pressed[approve]:
            break
        elif pressed[right]:
            for player in env.players:
                player.score.up()
            tick.sleep(0.1)
        elif pressed[left]:
            for player in env.players:
                player.score.down()
            tick.sleep(0.1)

        env.GameWindow.blit(env.background, (0, 0))

        for player in env.players:
            player.score.display(env, (0, 21, 108))

        env.GameWindow.blit(credits_title, (title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        tick.sleep()
        exe = time.time() - tick.before_loop > 0.7

    env.credits = False
    welcome(env)
