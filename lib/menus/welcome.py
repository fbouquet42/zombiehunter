import pygame
import time

class   _Tick:
    def __init__(self):
        self.time = time.time()
        self.before_loop = self.time

def welcome(env):
    env.quit = True
    welcome_title = env.mod.tools.load_img(env, 'menus/' + 'welcome_menu', env.height, env.height)
    env.title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection', env.height, env.height)
    position = [(env.title_position,0), (env.title_position, int(env.height * 0.15)), (env.title_position, int(env.height * 0.3))]
    up = pygame.K_w
    down = pygame.K_s
    approve = pygame.K_r

    tick = _Tick()
    action = 0
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
        elif action < 2 and pressed[down]:
            action += 1
            time.sleep(env.mod.tools.clock(tick, wait=0.1))
        elif action and pressed[up]:
            action -= 1
            time.sleep(env.mod.tools.clock(tick, wait=0.1))

        env.GameWindow.blit(env.background, (0, 0))
        env.GameWindow.blit(welcome_title, (env.title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick))
        exe = time.time() - tick.before_loop > 0.5

    if not action:
        env.players.append(env.mod.players.Player(env=env, keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_r), x=int(0.45* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='jack'))
    elif action == 1:
        env.players.append(env.mod.players.Player(env=env, keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_r), x=int(0.2* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='jack'))
        env.players.append(env.mod.players.Player(env=env, keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_SPACE), x=int(0.7* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='baltazar'))
    else:
        env.closed = True
    env.players_alive = len(env.players)
    env.quit = False
