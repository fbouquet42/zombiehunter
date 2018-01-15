import time
import pygame
import tools

from player import set_hitbox_bullet
class   Bullet:
    def __init__(self, env, player):
        self.x = player.x
        self.y = player.y
        self.limitx = env.width + 100
        self.limity = env.height + 100
        self.env = env
        self.player = player
        self.direction = player.direction
        self.dimensions = player.dimensions
        self.img = player.weapon.bullet_type.img[player.direction]
        self.rapidity = player.weapon.bullet_type.rapidity
        self.hitbox = set_hitbox_bullet(env, self)
        tools.move(self, self.direction)

    def move(self):
        tools.move(self, self.direction)
        if self.x < -100 or self.y < -100 or self.y > self.limity or self.x > self.limitx:
            return False
        self.hitbox.update_coords(self)
        for player in self.env.players:
            if player is not self.player and player.x <= (self.x + self.hitbox.dimensions) and self.x <= (player.x + player.hitbox.dimensions) and player.y <= (self.y + self.hitbox.dimensions) and self.y <= (player.y + player.hitbox.dimensions):
                if not player.injured and player.lives:
                    player.injured += 20
                    player.lives -= 1
                return False
        return True

direction = {1 : 0, 2 : 2, 3 : 1, 4 : 4, 6 : 3, 8 : 6, 9 : 7, 12 : 5}
def move(env):

    for player in env.players:
        if not player.lives:
            continue
        moving = 0
        if env.pressed[player.up]:
            moving += 1
        if env.pressed[player.left]:
            moving += 2
        if env.pressed[player.down]:
            moving += 4
        if env.pressed[player.right]:
            moving += 8
        try:
            player.move(direction[moving])
        except KeyError:
            pass
        if env.pressed[player.shoot] and not player.weapon.cooldown:
            env.bullets.append(Bullet(env, player))
            player.weapon.cooldown += player.weapon.cadence


def display(env):
    for player in env.players:
        fitting = 0.23 if player.direction % 2 else 0
        if not player.lives:
            env.GameManager.blit(player.img_dead[player.direction], (int(player.x - player.dimensions * fitting), int(player.y - player.dimensions * fitting)))
        elif player.injured:
            env.GameManager.blit(player.img_injured[player.direction], (int(player.x - player.dimensions * fitting), int(player.y - player.dimensions * fitting)))
        else:
            env.GameManager.blit(player.img[player.direction], (int(player.x - player.dimensions * fitting), int(player.y - player.dimensions * fitting)))
        if player.lives:
            env.GameManager.blit(player.weapon.img[player.direction], (int(player.x - player.dimensions * fitting), int(player.y - player.dimensions * fitting)))
        if env.debug:
            env.GameManager.blit(player.hitbox.img, (int(player.hitbox.x), int(player.hitbox.y)))

def update(env):
    move(env)
    display(env)

def auto(env):
    while True:
        i = 0
        while i != len(env.bullets):
            if not env.bullets[i].move():
                del env.bullets[i]
            else:
                fitting = 0.23 if env.bullets[i].direction % 2 else 0
                env.GameManager.blit(env.bullets[i].img, (int(env.bullets[i].x - env.bullets[i].dimensions * fitting), int(env.bullets[i].y - env.bullets[i].dimensions * fitting)))
                if env.debug:
                    env.GameManager.blit(env.bullets[i].hitbox.img, (int(env.bullets[i].hitbox.x - env.bullets[i].hitbox.dimensions * fitting), int(env.bullets[i].hitbox.y - env.bullets[i].hitbox.dimensions * fitting)))
                i += 1

        for monster in env.monsters:
            monster.move()
        for player in env.players:
            if player.weapon.cooldown:
                player.weapon.cooldown -= 1
            if player.injured:
                player.injured -= 1
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
