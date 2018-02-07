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
    rapidity = 29
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
                self.player.score += monster.hitted()
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
            while self.env.pause:
                time.sleep(0.01)

class   HellStar:
    def build_class(env, monster):
        HellStar.dimensions = monster.dimensions
        HellStar.img = tools.set_imgs(env.img_src + "bullets/", "hell_star", monster.dimensions)
        HellStar.img_off = tools.set_imgs(env.img_src + "bullets/", "hell_star_off", monster.dimensions)
        HellStar.monster = monster
        HellStar.env = env
        return HellStar

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.summoning = 0
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self, 0.40)

    def display(self, env):
        if self.summoning and not self.monster.fire_star:
            tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        else:
            tools.display(env, self.img_off[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)
    
    def target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()

    def dead(self):
        self.alive = False

    def move(self):
        while True:
            if self.monster.fire_star:
                self.summoning = 600
            if not self.monster.fire_star and self.summoning:
                self.target_hitted()
            if not (self.summoning + 100) % 220:
                monster = self.env.monster_type['minion'](self.env, self.x, self.y)
                t = Thread(target=monster.move, args=())
                t.daemon = True
                self.env.monsters.append(monster)
                t.start()
            if not self.monster.lives:
                return self.dead()
            if self.summoning:
                self.summoning -= 1
            time.sleep(0.01)
            while self.env.pause:
                time.sleep(0.01)

class   DoubleBullet():
    rapidity = 22

    def build_class(env):
        DoubleBullet.dimensions = env.player_dimensions
        DoubleBullet.img = tools.set_imgs(env.img_src + "bullets/", "double_bullet", env.player_dimensions)
        DoubleBullet.env = env
        DoubleBullet.limitx = env.width + 100
        DoubleBullet.limity = env.height + 100
        return DoubleBullet

    def __init__(self, x, y, direction, monster):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.monster = monster
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
            if player.affected(self):
                player.hitted()
                ret = True
        for monster in self.env.monsters:
            if not monster is self.monster and monster.affected(self):
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
            while self.env.pause:
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
                player.hitted(attack=2)
                ret = True
        for monster in self.env.monsters:
            if monster.affected(self):
                self.player.score += monster.hitted(attack=2)
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
            while self.env.pause:
                time.sleep(0.01)

class   Explosion:
    lifetime = 40
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
        self.hitbox = set_hitbox_bullet(self.env, self, 0.88)

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
            if not monster.injured and monster.affected(self):
                self.player.score += monster.hitted()

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
            while self.env.pause:
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
            while self.env.pause:
                time.sleep(0.01)
