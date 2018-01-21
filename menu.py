import pygame
from players import Player
import tools

def mainmenu(env, clock):
    main_title = pygame.image.load(env.img_src + "main_title.png")
    main_title = pygame.transform.scale(main_title, (env.player_dimensions * 4, env.player_dimensions * 4))
    title_player_one = pygame.image.load(env.img_src + "players/title_player_one.png")
    title_player_one = pygame.transform.scale(title_player_one, (env.player_dimensions, env.player_dimensions))
    title_player_two = pygame.image.load(env.img_src + "players/title_player_two.png")
    title_player_two = pygame.transform.scale(title_player_two, (env.player_dimensions, env.player_dimensions))
    x_main = 0.2 * env.width
    y_main = 0.05 * env.height
    x1 = 0.25 * env.width - env.player_dimensions // 2
    x2 = 0.75 * env.width - env.player_dimensions // 2
    y = 0.5 * env.height
    player_one = Player(env=env, dimensions=env.player_dimensions, name='jack')
    player_two = Player(env=env, dimensions=env.player_dimensions, name='baltazar')

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
        tools.display(env, main_title, x_main, y_main)
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
    return False
