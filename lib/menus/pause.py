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
    position = [(title_position,0), (int(title_position * 1.25), 0), (int(title_position * 1.5), 0)]
    up = K_w
    down = K_s
    approve = K_r

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

        env.GameManager.blit(env.background, (0, 0))
        env.GameManager.blit(welcome_title, (title_position, 0))
        env.GameManager.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick, wait=0.25))

    env.pause = False
    if not action:
        return
    else:
        env.closed = True
    env.clear()
    welcome(env)
