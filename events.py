import time
import pygame
import tools
import numpy as np
randint = lambda mini, maxi: np.random.randint(mini, maxi)

def keys_manager(env):
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

def display(env):
    keys_manager(env)
    for player in env.players:
        player.display(env)
    for monster in env.monsters:
        monster.display(env)
    i = 0
    while i != len(env.bullets):
        if not env.bullets[i].alive:
            del env.bullets[i]
        else:
            env.bullets[i].display(env)
            i += 1

def update_tick(env):
    while True:
        for player in env.players:
            player.update()
        for monster in env.monsters:
            monster.update()
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)

def spawner(env):
    rand = 0
    while True:
        if not rand:
            rand = randint(120, 220)
            env.spawn(randint(-200, 0), randint(-200, 0))
        rand -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
