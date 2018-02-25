import pygame
import time

#from . import failure
from . import welcome

def game_over(env):
    env.quit = True
    go_title = env.mod.tools.load_img(env, 'menus/' + 'GO_menu', env.height, env.height)
    if env.retry:
        retry_title = env.mod.tools.load_img(env, 'menus/' + 'fire_goblet', env.height, env.height)
    else:
        retry_title = env.mod.tools.load_img(env, 'menus/' + 'fire_goblet_off', env.height, env.height)
    title_position = (env.width - env.height) // 2
    selection = env.mod.tools.load_img(env, 'menus/' + 'selection_failure', env.height, env.height)
    position = [(title_position,0), (title_position, env.height * 0.15), (title_position, env.height * 0.3)]
    up = pygame.K_w
    down = pygame.K_s
    left = pygame.K_a
    right = pygame.K_d
    approve = pygame.K_r

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
            if action != 1 or env.retry:
                break
        elif action > 1 and pressed[up]:
            action -= 1
            tick.sleep(0.1)
        elif action < 2 and pressed[down]:
            action += 1
            tick.sleep(0.1)
        elif pressed[left]:
            for player in env.players:
                player.score.up()
            tick.sleep(0.1)
        elif pressed[right]:
            for player in env.players:
                player.score.down()
            tick.sleep(0.1)
            

        env.GameWindow.blit(env.background, (0, 0))

        for player in env.players:
            player.score.display(env, (110, 74, 0))

        env.GameWindow.blit(go_title, (title_position, 0))
        env.GameWindow.blit(retry_title, (title_position, 0))
        env.GameWindow.blit(selection, position[action])
        pygame.display.update()
        tick.sleep()
        exe = time.time() - tick.before_loop > 0.7

    if action == 1:
        env.monsters.clear()
        env.bullets.clear()
        env.jerk = False
        env.furious = 0
        env.walking_dead = 0
        env.retry -= 1
        for player in env.players:
            player.lives = player.max_lives
            player.score.total = 0
        env.quit = False
        return
    welcome(env)
