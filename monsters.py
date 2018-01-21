import tools
import pygame
import weapons
import time

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
    rapidity = 4
    lives = 2
    injured = 0
    direction = 0
    name = "zombie"
    degeneration = 400

    def build_class(env):
        Zombie.env = env
        Zombie.dimensions = env.player_dimensions
        Zombie.half = Zombie.dimensions // 2
        Zombie.img = tools.set_imgs(env.img_src + 'monsters/', Zombie.name, Zombie.dimensions)
        Zombie.img_injured = tools.set_imgs(env.img_src + 'monsters/', Zombie.name + '_injured', Zombie.dimensions)
        Zombie.img_dead = tools.set_imgs(env.img_src + 'monsters/', Zombie.name + '_dead', Zombie.dimensions)
        Zombie.value = 1
        return Zombie

    def __init__(self, env, x, y):
        self.x = x + env.width + 200 if x > -100 else x
        self.y = y + env.height + 200 if y > -100 else y

        self.hitbox = set_hitbox_monster(env, self)
        self.target = env.players[0]
        #self.weapon = weapon(env, self)

    def affected(self, bullet):
        if self.x <= (bullet.x + bullet.hitbox.dimensions) and bullet.x <= (self.x + self.hitbox.dimensions) and self.y <= (bullet.y + bullet.hitbox.dimensions) and bullet.y <= (self.y + self.hitbox.dimensions):
            return True
        return False

    def hitted(self):
        if self.lives and not self.injured:
            self.injured += 10
            self.lives -= 1
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
                    return None
                d_objective = distance
                x_objective = x
                y_objective = y
                target = player
        if target is None:
            return None
        self.target = target
        if not y_objective or abs(x_objective / y_objective) > 0.66:
            if x < 0:
                direction = 2
            else:
                direction = 6
        elif abs(x_objective / y_objective) < 0.33:
            if y < 0:
                direction = 0
            else:
                direction = 4
        else:
            if x < 0 and y < 0:
                direction = 1
            elif x < 0:
                direction = 3
            elif y > 0:
                direction = 5
            else:
                direction = 7
        return direction

    def target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()

    def move(self):
        while True:
            if not self.lives:
                return
            direction = self.sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                tools.move(self, direction)
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
        if env.debug:
            if self.lives:
                pygame.draw.line(env.GameManager, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        #self.weapon.update()
