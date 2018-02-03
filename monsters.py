import tools
import pygame
import bullets
from threading import Thread
import time
import numpy as np
randint = lambda mini, maxi: np.random.randint(mini, maxi)

#Monster idea
#dark_knight (??) -- necromancer -- garou (24 lives)

class HitboxMonster:
    def update_coords(self, monster):
        self.x = int(monster.x + self.resize)
        self.y = int(monster.y + self.resize)

    def __init__(self, monster, resize):
        self.resize = int(monster.dimensions * ((1.00 - resize) / 2))
        self.update_coords(monster)
        self.dimensions = int(monster.dimensions * resize)

def set_hitbox_monster(env, monster, resize=0.24):
    hitbox = HitboxMonster(monster, resize)
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class Zombie:
    lives = 2
    injured = 0
    direction = 0
    name = "zombie"
    degeneration = 400
    value = 1

    def build_class(env):
        Zombie.env = env
        Zombie.dimensions = env.player_dimensions
        Zombie.half = Zombie.dimensions // 2
        Zombie.img = tools.set_imgs(env.img_src + 'monsters/', Zombie.name, Zombie.dimensions)
        Zombie.img_injured = tools.set_imgs(env.img_src + 'monsters/', Zombie.name + '_injured', Zombie.dimensions)
        Zombie.img_dead = tools.set_imgs(env.img_src + 'monsters/', Zombie.name + '_dead', Zombie.dimensions)
        return Zombie

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y

        self.rapidity = randint(2, 7)
        self.rapidity = 4 if self.rapidity > 4 else self.rapidity
        self.hitbox = set_hitbox_monster(env, self)
        self.target = env.players[0]
        #self.weapon = weapon(env, self)

    def affected(self, bullet):
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def hitted(self, attack=1):
        if self.lives:
            self.injured += 12
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.value
        return 0
    
    def sniff_fresh_flesh(self):
        d_objective = -1
        target = None
        for player in self.env.players:
            if not player.lives:
                continue
            x = (player.x + player.half) - (self.x + self.half)
            y = (player.y + player.half) - (self.y + self.half)
            distance = int((x ** 2 + y ** 2) ** 0.5)
            if target is None or d_objective > distance:
                if not x and not y:
                    return None, None
                d_objective = distance
                x_objective = x
                y_objective = y
                target = player
        if target is None:
            return None, None
        self.target = target
        if not y_objective or abs(x_objective / y_objective) > 0.66:
            if x_objective < 0:
                direction = 2
            else:
                direction = 6
        elif abs(x_objective / y_objective) < 0.33:
            if y_objective < 0:
                direction = 0
            else:
                direction = 4
        else:
            if x_objective < 0 and y_objective < 0:
                direction = 1
            elif x_objective < 0:
                direction = 3
            elif y_objective > 0:
                direction = 5
            else:
                direction = 7
        return direction, d_objective

    def target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()

    def move(self):
        while True:
            if not self.lives:
                return
            direction, _ = self.sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
            self.target_hitted()
            time.sleep(0.01)
            while self.env.pause:
                time.sleep(0.01)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        tools.display(env, img, self.x, self.y, fitting)
        #if self.lives:
        #    self.weapon.display(env, self.direction, self.x, self.y, fitting)
        if env.debug and self.lives:
            pygame.draw.line(env.GameManager, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        #self.weapon.update()

class FireBall(Zombie):
    name = "fire_ball"
    degeneration = 400
    rapidity = 7
    ultimatum = 360

    def build_class(env):
        FireBall.img = tools.set_imgs(env.img_src + 'bullets/', FireBall.name, FireBall.dimensions)
        FireBall.img_dead = tools.set_imgs(env.img_src + 'bullets/', FireBall.name + '_dead', FireBall.dimensions)
        return FireBall

    def __init__(self, env, x, y, target):
        self.x = x
        self.y = y
        self.hitbox = set_hitbox_monster(env, self)
        self.target = target
        self.alive = True
        self.fire = True
        #self.weapon = weapon(env, self)

    def sniff_fresh_flesh(self):
        x_objective = (self.target.x + self.target.half) - (self.x + self.half)
        y_objective = (self.target.y + self.target.half) - (self.y + self.half)
        d_objective = int((x_objective ** 2 + y_objective ** 2) ** 0.5)
        if not y_objective or abs(x_objective / y_objective) > 0.66:
            if x_objective < 0:
                direction = 2
            else:
                direction = 6
        elif abs(x_objective / y_objective) < 0.33:
            if y_objective < 0:
                direction = 0
            else:
                direction = 4
        else:
            if x_objective < 0 and y_objective < 0:
                direction = 1
            elif x_objective < 0:
                direction = 3
            elif y_objective > 0:
                direction = 5
            else:
                direction = 7
        return direction, d_objective

    def target_hitted(self):
        for player in self.env.players:
            if player.lives and player.affected(self):
                player.hitted()
                self.fire = False

    def move(self):
        while self.fire:
            direction, _ = self.sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                tools.move(self, direction)
                self.hitbox.update_coords(self)
            self.target_hitted()
            time.sleep(0.01)
            while self.env.pause:
                time.sleep(0.01)
            self.ultimatum -= 1
            if not self.ultimatum or not self.target.lives:
                self.fire = False

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.fire:
            img = self.img_dead[self.direction]
        else:
            img = self.img[self.direction]
        tools.display(env, img, self.x, self.y, fitting)
        if env.debug and self.fire:
            pygame.draw.line(env.GameManager, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if not self.fire and self.degeneration:
            self.degeneration -= 1
        elif not self.fire and not self.degeneration:
            self.alive = False

class Daemon(Zombie):
    lives = 135
    name = "daemon"
    fury_1 = 90
    fury_2 = 45

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y
        self.img = tools.set_imgs(env.img_src + 'monsters/', self.name, self.dimensions)
        self.img_injured = tools.set_imgs(env.img_src + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = tools.set_imgs(env.img_src + 'monsters/', self.name + '_dead', self.dimensions)
        self.img_furious = tools.set_imgs(env.img_src + 'monsters/', self.name + '_furious', self.dimensions)
        self.img_spelling = tools.set_imgs(env.img_src + 'monsters/', self.name + '_spelling', self.dimensions)
        self.img_shooting = tools.set_imgs(env.img_src + 'monsters/', self.name + '_shooting', self.dimensions)

        self.rapidity = 3
        self.furious = 0
        #self.spell = randint(500, 1100)
        self.spell = randint(250, 400)
        self.spell_type = [self.fire_spell , self.star_spell]
        self.fire_ball = FireBall.build_class(env)
        self.hell_star = bullets.HellStar.build_class(env)
        self.shooting = -1
        self.fire_star = 0
        self.summoning = 4
        self.spelling = False
        self.hitbox = set_hitbox_monster(env, self, 0.7)
        self.target = env.players[0]

    def fury_mod(self, time):
        self.furious = time
        self.env.furious = 1
        self.spelling = False
        self.spell += 10
        self.shooting = -1

    def hitted(self, attack=1):
        if self.lives and not self.furious:
            self.injured += 12
            if self.lives > self.fury_2 and self.lives - attack <= self.fury_2:
                self.fury_mod(1444)
            elif self.lives > self.fury_1 and self.lives - attack <= self.fury_1:
                self.fury_mod(999)
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
        return attack

    def move(self):
        while self.lives:
            direction, _ = self.sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                if not self.spelling:
                    tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
            self.target_hitted()
            time.sleep(0.01)
            while self.env.pause:
                time.sleep(0.01)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.furious:
            img = self.img_furious[self.direction]
        elif self.spelling:
            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        tools.display(env, img, self.x, self.y, fitting)
        if self.spelling:
            tools.display(env, self.img_shooting[int(self.shooting) % 8], self.x, self.y, 0.23 * self.dimensions if int(self.shooting) % 2 else 0)
        if env.debug and self.lives:
            pygame.draw.line(env.GameManager, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def get_coords(self, i):
        x = self.x
        y = self.y
        if i == 1:
            y = self.y + self.half
        elif i == 2:
            y = self.y - self.half
        elif i == 3:
            x = self.x - self.half
        elif i == 4:
            x = self.x + self.half
        return x, y

    def fire_spell(self):
        self.shooting = 0.0

    def star_spell(self):
        self.fire_star = 1000
        if self.summoning:
            x, y = self.get_coords(self.summoning)
            hell_star = self.hell_star(self.env, x, y, self.env.players[randint(0, len(self.env.players))])
            t = Thread(target=hell_star.move, args=())
            t.daemon = True
            self.env.bullets.append(hell_star)
            t.start()
            self.summoning -= 1

    def update(self):
        if self.injured:
            self.injured -= 1
        if self.furious:
            self.furious -= 1
            if not self.furious:
                self.env.furious = 0
        elif int(self.shooting) != -1 and self.shooting < 16.:
            self.shooting += 0.12
        elif int(self.shooting) != -1:
            self.shooting = -1
            for i in range(1, 5):
                x, y = get_coords(i)
                fire_ball = self.fire_ball(self.env, x, y, self.env.players[randint(0, len(self.env.players))])
                t = Thread(target=fire_ball.move, args=())
                t.daemon = True
                self.env.bullets.append(fire_ball)
                t.start()
            self.spelling = False
        elif self.fire_star:
            self.fire_star -= 1
        elif self.spell:
            self.spell -= 1
        else:
            self.spell_type[randint(0, len(self.spell_type))]()
            self.spell = randint(500, 1100)
            self.spelling = True
        if not self.lives and self.degeneration:
            self.degeneration -= 1

class   Minion(Zombie):
    name = "minion"
    lives = 3
    def build_class(env):
        Minion.img = tools.set_imgs(env.img_src + 'monsters/', Minion.name, Minion.dimensions)
        Minion.img_injured = tools.set_imgs(env.img_src + 'monsters/', Minion.name + '_injured', Minion.dimensions)
        Minion.img_dead = tools.set_imgs(env.img_src + 'monsters/', Minion.name + '_dead', Minion.dimensions)
        return Minion

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y

        self.rapidity = randint(3, 7)
        self.rapidity = 4 if self.rapidity > 4 else self.rapidity
        self.hitbox = set_hitbox_monster(env, self, 0.26)
        self.target = env.players[0]


class   JackLantern(Zombie):
    name = "jack_lantern"
    lives = 3
    value = 3

    def build_class(env):
        JackLantern.img = tools.set_imgs(env.img_src + 'monsters/', JackLantern.name, JackLantern.dimensions)
        JackLantern.img_injured = tools.set_imgs(env.img_src + 'monsters/', JackLantern.name + '_injured', JackLantern.dimensions)
        JackLantern.img_dead = tools.set_imgs(env.img_src + 'monsters/', JackLantern.name + '_dead', JackLantern.dimensions)
        JackLantern.bullet = bullets.DoubleBullet.build_class(env)
        return JackLantern

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y

        self.rapidity = randint(2, 3)
        self.hitbox = set_hitbox_monster(env, self)
        self.target = env.players[0]

        self.next_shoot = randint(120, 300)

    def update(self):
        if self.injured:
            self.injured -= 1
        if self.next_shoot:
            self.next_shoot -= 1
        elif self.lives:
            bullet = self.bullet(self.x, self.y, self.direction, self)
            t = Thread(target=bullet.move, args=())
            t.daemon = True
            self.env.bullets.append(bullet)
            t.start()
            self.next_shoot = randint(120, 300)
        if not self.lives and self.degeneration:
            self.degeneration -= 1

class   Cyclops(Zombie):
    lives = 7
    eyeless = 3
    name = "cyclops"
    turn = 30
    hunt = True
    value = 5

    def build_class(env):
        Cyclops.sniff = int(Cyclops.dimensions * 1.5)
        Cyclops.img = tools.set_imgs(env.img_src + 'monsters/', Cyclops.name, Cyclops.dimensions)
        Cyclops.img_injured = tools.set_imgs(env.img_src + 'monsters/', Cyclops.name + '_injured', Cyclops.dimensions)
        Cyclops.img_eyeless = tools.set_imgs(env.img_src + 'monsters/', Cyclops.name + '_eyeless', Cyclops.dimensions)
        Cyclops.img_eyeless_injured = tools.set_imgs(env.img_src + 'monsters/', Cyclops.name + '_eyeless_injured', Cyclops.dimensions)
        Cyclops.img_dead = tools.set_imgs(env.img_src + 'monsters/', Cyclops.name + '_dead', Cyclops.dimensions)
        return Cyclops

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y
        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.rapidity = randint(2, 4)

        self.hitbox = set_hitbox_monster(env, self, 0.46)
        self.target = env.players[0]
        self.wait = self.turn
        #self.weapon = weapon(env, self)

    def move(self):
        while True:
            if not self.lives:
                return
            direction, distance = self.sniff_fresh_flesh()
            if direction is not None:
                self.hunt = distance < self.sniff
            if self.lives <= self.eyeless and not self.hunt:
                if not self.wait:
                    direction = randint(0, 12)
                    self.wait = self.turn
                else:
                    self.wait -= 1
                    direction = self.direction
            if direction is not None and direction < 8:
                self.direction = direction
                tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
            if self.lives <= self.eyeless:
                tools.limits(self, self.limitx, self.limity)
            self.target_hitted()
            time.sleep(0.01)
            while self.env.pause:
                time.sleep(0.01)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.lives > self.eyeless and self.injured:
            img = self.img_injured[self.direction]
        elif self.lives > self.eyeless:
            img = self.img[self.direction]
        elif self.injured:
            img = self.img_eyeless_injured[self.direction]
        else:
            img = self.img_eyeless[self.direction]
        tools.display(env, img, self.x, self.y, fitting)
        #if self.lives:
        #    self.weapon.display(env, self.direction, self.x, self.y, fitting)
        if env.debug and self.lives:
            if self.lives > self.eyeless or self.hunt:
                pygame.draw.line(env.GameManager, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        #self.weapon.update()
