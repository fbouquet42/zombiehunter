import pygame
from players import Player
import tools
import time

def endmenu(env, clock):
    myfont = pygame.font.SysFont('Comic Sans MS', 40)
    score_player_one = myfont.render(str(env.players[0].score), False, (8, 0, 107))
    score_player_two = myfont.render(str(env.players[1].score), False, (8, 0, 107))
    x1 = 0.25 * env.width - env.player_dimensions // 2
    x2 = 0.75 * env.width - env.player_dimensions // 2
    y = 0.5 * env.height
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        env.GameManager.blit(env.background, (0, 0))
        tools.display(env, env.main_title, env.title_position[0], env.title_position[1])
        tools.display(env, env.players[0].title, x1, y)
        tools.display(env, env.players[1].title, x2, y)
        env.GameManager.blit(score_player_one,(x1 + env.players[0].half, y + env.players[0].half))
        env.GameManager.blit(score_player_two,(x2 + env.players[1].half, y + env.players[1].half))

        pygame.display.update()
        clock.tick(3)


def pausemenu(env):
    if not hasattr(pausemenu, 'time'):
        env.pause = True
        pausemenu.time = time.time()
    elif not env.pause and time.time() - pausemenu.time > 1:
        env.pause = True
        pausemenu.time = time.time()
    elif env.pause and time.time() - pausemenu.time > 1:
        env.pause = False
        pausemenu.time = time.time()

def mainmenu(env, clock):
    title_player_one = pygame.image.load(env.img_src + "players/title_player_one.png")
    title_player_one = pygame.transform.scale(title_player_one, (env.player_dimensions, env.player_dimensions))
    title_player_two = pygame.image.load(env.img_src + "players/title_player_two.png")
    title_player_two = pygame.transform.scale(title_player_two, (env.player_dimensions, env.player_dimensions))
    player_one = Player(env=env, dimensions=env.player_dimensions, name='jack')
    player_two = Player(env=env, dimensions=env.player_dimensions, name='baltazar')
    x1 = 0.25 * env.width - env.player_dimensions // 2
    x2 = 0.75 * env.width - env.player_dimensions // 2
    y = 0.5 * env.height

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        env.pressed = pygame.key.get_pressed()
        if env.pressed[pygame.K_SPACE] or env.pressed[pygame.K_RETURN]:
            break
        if env.pressed[pygame.K_a] or env.pressed[pygame.K_d] or env.pressed[pygame.K_LEFT] or env.pressed[pygame.K_RIGHT]:
            buff = player_two
            player_two = player_one
            player_one = buff
        env.GameManager.blit(env.background, (0, 0))
        tools.display(env, env.main_title, env.title_position[0], env.title_position[1])
        tools.display(env, title_player_one, x1, y)
        tools.display(env, title_player_two, x2, y)
        tools.display(env, player_one.img[0], x1, y)
        tools.display(env, player_two.img[0], x2, y)
        pygame.display.update()
        clock.tick(10)

    player_one.selected(env, title_player_one, (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE), x1, y)
    player_two.selected(env, title_player_two, (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_RETURN), x2, y)
    env.players.append(player_one)
    env.players.append(player_two)
    env.players_alive = 2
    return False
