import time
import pygame

direction = {1 : 0, 2 : 2, 3 : 1, 4 : 4, 6 : 3, 8 : 6, 9 : 7, 12 : 5}
def move(env):

    for player in env.players:
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
        if env.pressed[player.shoot]:
            env.bullets.append([player.x, player.y, player.bullet.img[player.direction], player.bullet.rapidity])

def display(env):
    for disp in env.to_display:
        fitting = 0
        if disp.direction % 2:
            fitting = 0.23
        env.GameManager.blit(disp.curr_img, (int(disp.x - disp.dimensions * fitting), int(disp.y - disp.dimensions * fitting)))
        if not disp.is_attr:
            if env.debug:
                env.GameManager.blit(disp.hitbox.img, (int(disp.hitbox.x), int(disp.hitbox.y)))
            for attr in disp.attributes:
                env.GameManager.blit(attr.curr_img, (int(attr.x - attr.dimensions * fitting), int(attr.y - attr.dimensions * fitting)))

def update(env):
    move(env)
    display(env)

def auto(env):
    while True:
        for bullet in env.bullets:
            bullet.move()
        time.sleep(0.01)
        while env.pause:
            time.sleep(0.01)
