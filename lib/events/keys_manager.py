import pygame

def keys_manager(env, player):
    tick = env.mod.tools.Tick()

    while True:
        tick.sleep()
        while env.pause or env.quit:
            tick.sleep()

        if not player.lives:
            if env.walking_dead and not player.possessed:
                player.undead(env)
            continue

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            env.pause = True

        direction = env.mod.tools.set_direction(pressed, player)

        if direction < 0:
            pass
        elif player.fixed:
            player.move(direction, player.rapidity // 2)
        else:
            player.move(direction)
        if pressed[player.shoot]:
            player.weapon.pressed(env, player)
        else:
            player.weapon.not_pressed(env=env, player=player)

