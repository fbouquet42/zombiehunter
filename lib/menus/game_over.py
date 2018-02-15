import pygame
import time

#from . import failure
from . import welcome

class   _Tick:
    def __init__(self):
        self.time = time.time()
        self.before_loop = self.time

def game_over(env):
    env.quit = True
    #if env.retry:
    #    return failure()
    go_title = env.mod.tools.load_img(env, 'menus/' + 'GO_menu', env.height, env.height)
    title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection_failure', env.height, env.height)
    position = [(title_position,0), (title_position, env.height * 0.15), (title_position, env.height * 0.3)]
    up = pygame.K_w
    down = pygame.K_s
    approve = pygame.K_r

    tick = _Tick()
    action = 2
    exe = False
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

        env.GameWindow.blit(env.background, (0, 0))

        for player in env.players:
            player.display_score(env)

        env.GameWindow.blit(go_title, (title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick))
        exe = time.time() - tick.before_loop > 0.8

    env.clear()
    welcome(env)
