from threading import Thread
from random import randint

from . import DefaultMonster
from . import set_hitbox_monster
from . import Flower

class   Witch(DefaultMonster):
    name = "witch"
    lives = 160
    lives_dismount = 60
    id_nb = 17
    cloud_speed = 6

    @classmethod
    def build_class(cls):
        cls.ideal_distance = cls.env.height // 2
        cls.ideal_buffer = int(cls.ideal_distance * 0.2)
        cls.rushed_max = cls.ideal_distance - cls.ideal_buffer
        cls.fled_max = cls.ideal_distance + cls.ideal_buffer
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_spelling = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_spelling', cls.dimensions)
        cls.img_invisible = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_invisible', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_mounting = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_mounting', cls.dimensions)
        cls.img_mounting_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_mounting_injured', cls.dimensions)
        cls.img_mounting_spelling = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_mounting_spelling', cls.dimensions)
        cls.img_mounting_cloud = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_mounting_cloud', cls.dimensions)
        cls.dismount_effect = cls.env.mod.objects.DismountEffect.build_class(cls.env, cls.dimensions)
        cls.spore  = cls.env.mod.bullets.Spore.build_class(cls.env)
        cls.flower  = Flower.build_class(cls.env)
        return cls

    def _next_spell(self):
        self.will_spell = randint(220, 460)
        if self.sneaking:
            self.will_spell //= 3

    def throw_spore(self):
        spore = self.spore(self.x, self.y, self.direction if self.rushing else ((self.direction + 4) % 8))
        t = Thread(target=spore.move, args=())
        t.daemon = True
        self.env.bullets.append(spore)
        t.start()

    def to_sneak(self):
        self.sneaking = True

    def spawn_flower(self):
        if self.target is None:
            return
        flower = self.flower(self.target)
        t = Thread(target=flower.move, args=())
        t.daemon = True
        self.env.monsters.append(flower)
        t.start()

    def frogifying(self):
        if len(self.env.zombies):
            self.env.zombies[randint(0, len(self.env.zombies) - 1)].frogified()

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.46)
        self.hitbox_small = set_hitbox_monster(env, self)
        self.env = env

        self.rapidity = randint(6, 10)

        self.attack = 2
        self.mounting = True
        self.spelling = 0
        self.sneaking = False
        self.rushing = True
        self.clouding = 0
        self.spell_type = [self.frogifying, self.spawn_flower]
        #self.spell_type = [self.to_sneak]
        self._next_spell()
        self.walking_dead = False

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.sneaking:
            self.sneaking = False
            self.rushing = True
            self._next_spell()
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if self.mounting and self.lives <= self.lives_dismount:
                self.mounting = False
                self.attack = 1
                self.reset_bad_effect()
                self.invulnerable += 111
                self.clouding = 90
                self.rapidity += self.cloud_speed
                self.hitbox = self.hitbox_small
            return self.id_nb, attack
        return None, None

    def _action(self):
        if not self.stoned:
            direction, distance = self._sniff_fresh_flesh()
            if direction is not None:
                if self.sneaking:
                    if distance < self.rushed_max:
                        self.rushing = False
                    elif distance > self.fled_max:
                        self.rushing = True
                    if not self.rushing:
                        direction = (direction + 4) % 8
                self.direction = direction
                if self.sneaking:
                    rapidity = self.rapidity + 3
                else:
                    rapidity = self.rapidity
                self.tools.move(self, self.direction, rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def affected(self, bullet):
        if self.clouding:
            return False
        else:
            return super().affected(bullet)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.clouding:
            img = self.img_mounting_cloud[self.direction]
        elif self.sneaking:
            img = self.img_invisible[self.direction]
        elif self.spelling:
            if self.mounting:
                img = self.img_mounting_spelling[self.direction]
            else:
                img = self.img_spelling[self.direction]
        elif self.injured:
            if self.mounting:
                img = self.img_mounting_injured[self.direction]
            else:
                img = self.img_injured[self.direction]
        else:
            if self.mounting:
                img = self.img_mounting[self.direction]
            else:
                img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and not self.clouding and self.invulnerable:
            if self.mounting:
                self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
            else:
                self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            if self.mounting:
                self.tools.display(self.env, self.img_inflamed_large[self.direction], self.x, self.y, fitting)
            else:
                self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self._quit():
                return

        self.sneaking = False
        self.rushing = True

        if self.clouding:
            self.clouding = False
            self.rapidity -= self.cloud_speed

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        self._perform_fire()
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5

        if not self.lives:
            return
        if self.clouding:
            self.clouding -= 1
            if not self.clouding:
                self.rapidity -= self.cloud_speed
                self.env.objects.append(self.dismount_effect(self.x, self.y))
                self.spell_type.append(self.to_sneak)
            return

        if self.spelling:
            self.spelling -= 1
            if not self.spelling:
                if self.sneaking:
                    self.throw_spore()
                else:
                    self.spell_type[randint(0, len(self.spell_type) - 1)]()
                self._next_spell()
        if self.will_spell:
            self.will_spell -= 1
            if not self.will_spell:
                self.spelling = 6
