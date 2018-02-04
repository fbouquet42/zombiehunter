import time
import pygame
import tools
import numpy as np
randint = lambda mini, maxi: np.random.randint(mini, maxi)

def keys_manager(env):
    players_alive = 0
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
        players_alive += 1
    env.players_alive = players_alive

def display(env):
    keys_manager(env)
    for player in env.players:
        player.display(env)
    i = 0
    while i != len(env.monsters):
        if not env.monsters[i].degeneration:
            del env.monsters[i]
        else:
            env.monsters[i].display(env)
            i += 1
    i = 0
    while i != len(env.bullets):
        if not env.bullets[i].alive:
            del env.bullets[i]
        else:
            env.bullets[i].display(env)
            i += 1
    for title in env.titles:
        tools.display(env, title, env.title_position[0], env.title_position[1])

def update_tick(env):
    while True:
        for player in env.players:
            player.update()
        for monster in env.monsters:
            monster.update()
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)


def wave_debug(env):
    wave_3(env)
    title = pygame.image.load(env.img_src + "wave_1.png")
    title = pygame.transform.scale(title, (env.player_dimensions * 4, env.player_dimensions * 4))
    env.titles.append(title)
    time.sleep(5)
    env.titles.remove(title)

    monsters = ['jack_lantern', 'zombie', 'cyclops']
    while True:
        for monster in monsters:
            env.spawn(monster)
        while len(env.monsters):
            time.sleep(0.1)
        while env.pause:
            time.sleep(0.01)

def wave_1(env):
    if env.debug:
        wave_debug(env)
        return
    title = pygame.image.load(env.img_src + "wave_1.png")
    title = pygame.transform.scale(title, (env.player_dimensions * 4, env.player_dimensions * 4))
    env.titles.append(title)
    time.sleep(5)
    env.titles.remove(title)

    zombies_wave = 0
    zombie_spawn = 55
    zombie = 0
    cyclops_spawn = 650
    cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
    while zombies_wave < 40:
        if not zombie:
            zombie = randint(zombie_spawn, zombie_spawn * 2)
            env.spawn('zombie')
            zombies_wave += 1
        if not cyclops:
            cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
            env.spawn('cyclops')
        zombie -= 1
        cyclops -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
    while len(env.monsters):
        time.sleep(0.1)
    wave_2(env)

def wave_2(env):

    for player in env.players:
        player.lives = 4

    title = pygame.image.load(env.img_src + "wave_2.png")
    title = pygame.transform.scale(title, (env.player_dimensions * 4, env.player_dimensions * 4))
    env.titles.append(title)
    time.sleep(5)
    env.titles.remove(title)

    zombie_spawn = 70
    zombie = 0
    cyclops_spawn = 635
    cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
    jack_lantern_spawn = 370
    jacks_wave = 0
    jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
    while jacks_wave < 9:
        if not zombie:
            zombie = randint(zombie_spawn, zombie_spawn * 2)
            env.spawn('zombie', randint(1, 3))
        if not cyclops:
            cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
            env.spawn('cyclops')
        if not jack_lantern:
            jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
            env.spawn('jack_lantern')
            jacks_wave += 1
        zombie -= 1
        cyclops -= 1
        jack_lantern -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
    while len(env.monsters):
        time.sleep(0.1)
    wave_3(env)

def wave_3(env):

    env.background = env.background_hell
    for player in env.players:
        player.lives = 4

    title = pygame.image.load(env.img_src + "wave_3.png")
    title = pygame.transform.scale(title, (env.player_dimensions * 4, env.player_dimensions * 4))
    env.titles.append(title)
    time.sleep(5)
    env.titles.remove(title)

    boss = env.spawn_boss()
    zombie_spawn = 150
    zombie = 0
    cyclops_spawn = 1100
    cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
    jack_lantern_spawn = 600
    jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
    while boss.lives:
        if not zombie:
            zombie = randint(zombie_spawn, zombie_spawn * 2)
            env.spawn('zombie')
        if not cyclops:
            cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
            env.spawn('cyclops')
        if not jack_lantern:
            jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
            env.spawn('jack_lantern')
        zombie -= 1
        cyclops -= 1
        jack_lantern -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)

    env.background = env.background_basic
    while len(env.monsters):
        time.sleep(0.1)
    wave_4(env)

def wave_4(env):

    for player in env.players:
        player.lives = 4

    title = pygame.image.load(env.img_src + "wave_4.png")
    title = pygame.transform.scale(title, (env.player_dimensions * 4, env.player_dimensions * 4))
    env.titles.append(title)
    time.sleep(5)
    env.titles.remove(title)

    zombie_spawn = 70
    zombie = 0
    cyclops_spawn = 600
    cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
    jack_lantern_spawn = 350
    jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
    while True:
        if not zombie:
            zombie = randint(zombie_spawn, zombie_spawn * 2)
            env.spawn('zombie', randint(1, 4))
        if not cyclops:
            cyclops = randint(cyclops_spawn, cyclops_spawn * 2)
            env.spawn('cyclops')
        if not jack_lantern:
            jack_lantern = randint(jack_lantern_spawn, jack_lantern_spawn * 2)
            env.spawn('jack_lantern')
        zombie -= 1
        cyclops -= 1
        jack_lantern -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
