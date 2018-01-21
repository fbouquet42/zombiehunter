import tools
import pygame
import time
from threading import Thread

class HitboxBullet:
    def update_coords(self, bullet):
        self.x = int(bullet.x + self.resize)
        self.y = int(bullet.y + self.resize)

    def __init__(self, bullet, resize):
        self.resize = int(bullet.dimensions * ((1.00 - resize) / 2))
        self.update_coords(bullet)
        self.dimensions = int(bullet.dimensions * resize)

def set_hitbox_bullet(env, bullet, resize=0.12):
    hitbox = HitboxBullet(bullet, resize)
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class   Bullet:
    rapidity = 28
    def build_class(env, player):
        Bullet.dimensions = player.dimensions
        Bullet.img = tools.set_imgs(env.img_src + "bullets/", "bullet", player.dimensions)
        Bullet.player = player
        Bullet.env = env
        Bullet.limitx = env.width + 100
        Bullet.limity = env.height + 100
        return Bullet

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self)
        tools.move(self, self.direction)

    def display(self, env):
        tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def limits_reached(self):
        if self.x < -100 or self.y < -100 or self.y > self.limity or self.x > self.limitx:
            return True
        return False
    
    def target_hitted(self):
        ret = False
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                player.hitted()
                ret = True
        for monster in self.env.monsters:
            if monster.affected(self):
                monster.hitted()
                ret = True
        return ret

    def dead(self):
        self.alive = False

    def move(self):
        while True:
            tools.move(self, self.direction)
            if self.limits_reached():
                return self.dead()
            self.hitbox.update_coords(self)
            if self.target_hitted():
                return self.dead()
            time.sleep(0.01)

class   Arrow:
    rapidity = 22
    def build_class(env, player):
        Arrow.dimensions = player.dimensions
        Arrow.img = tools.set_imgs(env.img_src + "bullets/", "arrow", player.dimensions)
        Arrow.player = player
        Arrow.env = env
        Arrow.limitx = env.width + 100
        Arrow.limity = env.height + 100
        return Arrow

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self)
        tools.move(self, self.direction)

    def display(self, env):
        tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def limits_reached(self):
        if self.x < -100 or self.y < -100 or self.y > self.limity or self.x > self.limitx:
            return True
        return False
    
    def target_hitted(self):
        ret = False
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                player.hitted()
                ret = True
        for monster in self.env.monsters:
            if monster.affected(self):
                monster.hitted()
                ret = True
        return ret

    def dead(self):
        self.alive = False

    def move(self):
        while True:
            tools.move(self, self.direction)
            if self.limits_reached():
                return self.dead()
            self.hitbox.update_coords(self)
            if self.target_hitted():
                return self.dead()
            time.sleep(0.01)

class   Explosion:
    lifetime = 25
    def build_class(env, player):
        Explosion.dimensions = player.dimensions
        Explosion.img = tools.set_imgs(env.img_src + "bullets/", "explosion", player.dimensions)
        Explosion.player = player
        Explosion.env = env
        return Explosion

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self, 0.8)

    def display(self, env):
        tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def dead(self):
        self.alive = False

    def target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()
        for monster in self.env.monsters:
            if monster.affected(self):
                monster.hitted()

    def explose(self):
        while True:
            self.lifetime -= 1
            if not self.lifetime % 5:
                self.env.jerk = not self.env.jerk
            if not self.lifetime:
                self.env.jerk = False
                return self.dead()
            self.target_hitted()
            time.sleep(0.01)

class   Rocket:
    rapidity = 20
    def build_class(env, player):
        Rocket.dimensions = player.dimensions
        Rocket.img = tools.set_imgs(env.img_src + "bullets/", "rocket", player.dimensions)
        Rocket.player = player
        Rocket.env = env
        Rocket.limitx = env.width + 100
        Rocket.limity = env.height + 100
        Rocket.explosion = Explosion.build_class(env, player)
        return Rocket

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        tools.move(self, self.direction)

    def display(self, env):
        tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def limits_reached(self):
        if self.x < -100 or self.y < -100 or self.y > self.limity or self.x > self.limitx:
            return True
        return False

    def explose(self):
        explosion = self.explosion(self.x, self.y, self.direction)
        t = Thread(target=explosion.explose, args=())
        t.daemon = True
        self.env.bullets.append(explosion)
        t.start()

    def target_hitted(self):
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                self.explose()
                return True
        for monster in self.env.monsters:
            if monster.affected(self):
                self.explose()
                return True
        return False

    def dead(self):
        self.alive = False

    def move(self):
        while True:
            tools.move(self, self.direction)
            if self.rapidity < 34:
                self.rapidity += 1
            if self.limits_reached():
                return self.dead()
            self.hitbox.update_coords(self)
            if self.target_hitted():
                return self.dead()
            time.sleep(0.01)
