import pygame
import time

class   _Tick:
    def __init__(self):
        self.time = time.time()

def welcome(env):
    welcome_title = env.mod.tools.load_img(env, 'menus/' + 'welcome_menu', env.height, env.height)
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
        elif action < 2 and pressed[down]:
            action += 1
        elif action and pressed[up]:
            action -= 1

        env.GameManager.blit(env.background, (0, 0))
        env.GameManager.blit(welcome_title, (title_position, 0))
        env.GameManager.blit(selection, position[action])
        pygame.display.update()
        time.sleep(env.mod.tools.clock(tick, wait=0.25))

    if not action:
        env.players.append(env=env, keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_r), x=int(0.45* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='jack')
    if action == 1:
        env.players.append(env=env, keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_r), x=int(0.2* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='jack')
        env.players.append(env=env, keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_SPACE), x=int(0.7* env.width), y=int(0.5 *env.height), dimensions=env.player_dimensions, name='baltazar')
    else:
        env.closed = True
    env.quit = False
