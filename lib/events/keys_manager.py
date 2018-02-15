import pygame
import time
from threading import Thread

class _Tick:
    def __init__(self):
        self.time = time.time()

def keys_manager(env):
    tick = _Tick()
    while True:
        players_alive = 0
        env.pressed = pygame.key.get_pressed()
        if env.pressed[pygame.K_ESCAPE]:
            env.pause = True
        for player in env.players:
            if not player.lives:
                if env.walking_dead and not player.possessed:
                    player.undead(env)
                continue
            direction = env.mod.tools.set_direction(env.pressed, player)
            if direction >= 0:
                player.move(direction)
            if env.pressed[player.shoot]:
                player.weapon.pressed(env, player)
            else:
                player.weapon.not_pressed(env=env, player=player)
            players_alive += 1
        env.players_alive = players_alive
        time.sleep(env.mod.tools.clock(tick))
        while env.pause or env.quit:
            time.sleep(env.mod.tools.clock(tick))
