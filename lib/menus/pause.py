import pygame
import time

from . import welcome

class   _Tick:
    def __init__(self):
        self.time = time.time()

def pause(env):
    env.pause = True
    welcome_title = env.mod.tools.load_img(env, 'menus/' + 'pause_menu', env.height, env.height)
    title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection', env.height, env.height)
    position = [(title_position,0), (title_position, env.height * 0.15), (title_position, env.height * 0.3)]
    up = pygame.K_w
    down = pygame.K_s
    approve = pygame.K_r

    tick = _Tick()
    action = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.closed = True
                return
        pressed = pygame.key.get_pressed()
        if pressed[approve]:
            break
        elif not action and pressed[down]:
            action += 2
        elif action and pressed[up]:
            action -= 2

        env.GameWindow.blit(env.background, (0, 0))
        env.GameWindow.blit(welcome_title, (title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick, wait=0.25))

    env.pause = False
    if not action:
        return
    env.clear()
    welcome(env)
