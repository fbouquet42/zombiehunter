import pygame
import time

#from . import failure
from . import welcome

class   _Tick:
    def __init__(self):
        self.time = time.time()
        self.before_loop = self.time

def credits(env):
    env.quit = True
    credits_title = env.mod.tools.load_img(env, 'menus/' + 'credits_menu', env.height, env.height)
    title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection', env.height, env.height)
    position = [(title_position,0), (title_position, env.height * 0.15), (title_position, env.height * 0.3)]
    up = pygame.K_w
    down = pygame.K_s
    approve = pygame.K_r

    tick = _Tick()
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
        elif pressed[up]:
            for player in env.players:
                player.score.up()
            time.sleep(env.mod.tools.clock(tick, wait=0.1))
        elif pressed[down]:
            for player in env.players:
                player.score.down()
            time.sleep(env.mod.tools.clock(tick, wait=0.1))

        env.GameWindow.blit(env.background, (0, 0))

        for player in env.players:
            player.score.display(env, (0, 21, 108))

        env.GameWindow.blit(credits_title, (title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick))
        exe = time.time() - tick.before_loop > 0.8

    env.credits = False
    env.clear()
    welcome(env)
