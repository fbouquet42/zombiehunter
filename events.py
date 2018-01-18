import time
import pygame
import tools

def update(env):
    for player in env.players:
        if not player.lives:
            continue
        direction = tools.set_direction(env.pressed, player)
        if direction >= 0:
            player.move(direction)
        if env.pressed[player.shoot]:
            player.weapon.pressed(env, player)
        else:
            player.weapon.not_pressed(env=env, player=player)

def auto(env):
    while True:
        for player in env.players:
            player.display(env)
            player.update()
        #for monster in env.monsters:
        #    monster.move()
        i = 0
        while i != len(env.bullets):
            if not env.bullets[i].move():
                del env.bullets[i]
            else:
                env.bullets[i].display(env)
                i += 1

        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
