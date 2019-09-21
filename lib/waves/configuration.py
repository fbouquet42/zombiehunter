from random import randint
import time
#
#

class   AdditionalSpawn:
    def random(self, nb):
        return randint(nb, nb * 3)

    def __init__(self, dark_knight):
        self.dark_min, self.dark_max, self.dark_time = dark_knight

        self.next = self.random(self.dark_time)

    def process(self, env):
        if not self.next:
            env.mod.tools.spawn(env, env.mod.monsters.DarkKnight, randint(self.dark_min, self.dark_max))
            self.next = self.random(self.dark_time)
        else:
            self.next -= 1

class   DefaultWave:
    def random(self, i):
        return randint(self.times[i], self.times[i]*2)
    
    def spawn(self, env, i):
        if not self.nb[i]:
            return 0
        spawned = randint(1, self.nb[i])
        env.mod.tools.spawn(env, env.mod.monsters.tab[i], spawned)
        self.next[i] = self.random(i)
        return spawned

    def loot(self, env):
        pass

class   Wave1(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_1', env.height, env.height)
        self.objective = 70
        self.times = [45, 178]
        self.nb = [3, 1]
        self.next = [0, self.random(1)]
        self.add = AdditionalSpawn((0, 1, 799))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 0:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave2(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_2', env.height, env.height)
        self.objective = 25
        self.times = [58, 180, 120]
        self.nb = [3, 1, 2]
        self.next = [0, self.random(1), self.random(2)]
        self.add = AdditionalSpawn((0, 1, 888))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 2:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False


class   Wave3(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_3', env.height, env.height)
        self.looting_title = env.mod.tools.load_img(env, 'waves/looting_wave_3', env.height, env.height)
        self.cross = env.mod.objects.Cross.build_class(env, 'waves/cross_wave_3')
        self.weapons = [env.mod.weapons.Abaddon, env.mod.weapons.Aguni]
        self.times = [80, 230, 185]
        self.nb = [2, 1, 1]
        self.next = [0, self.random(1), self.random(2)]
        self.add = AdditionalSpawn((0, 1, 1222))
        env.background = env.background_hell
        self.objective = env.mod.tools.spawn_boss(env, env.mod.monsters.Daemon)
#        self.objective.lives = 0

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                self.spawn(env, i)
            else:
                self.next[i] -= 1
        self.add.process(env)
        if not self.objective.lives:
            env.background = env.background_basic
            return False
        return True

    def loot(self, env):
        env.titles.append(self.looting_title)
        env.objects.append(self.cross(x=int(0.2* env.width), y=int(0.5 *env.height)))
        if len(env.players) > 1:
            env.objects.append(self.cross(x=int(0.7* env.width), y=int(0.5 *env.height)))
        while len(env.objects):
            time.sleep(0.3)

        rand = randint(0, 1)
        env.objects.append(env.mod.objects.Weapon(env, x=int(0.2* env.width), y=int(0.5 *env.height), builder=self.weapons[rand]))
        if len(env.players) > 1:
            env.objects.append(env.mod.objects.Weapon(env, x=int(0.7* env.width), y=int(0.5 *env.height), builder=self.weapons[(rand + 1) % 2]))
        while len(env.objects):
            time.sleep(0.3)
        env.titles.remove(self.looting_title)

class   Wave4(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_4', env.height, env.height)
        self.objective = 5
        self.times = [69, 180, 220, 820]
        self.nb = [3, 1, 1, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3)]
        self.add = AdditionalSpawn((0, 2, 799))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 3:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave5(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_5', env.height, env.height)
        self.objective = 27
        self.times = [69, 180, 215, 1280, 102]
        self.nb = [3, 1, 1, 1, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4)]
        self.add = AdditionalSpawn((0, 2, 888))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 4:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave6(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_6', env.height, env.height)
        self.objective = 4
        self.times = [71, 185, 220, 1280, 263, 900]
        self.nb = [3, 1, 1, 1, 2, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2]
        self.add = AdditionalSpawn((0, 2, 799))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 5:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave7(DefaultWave):
    def _more_monsters(self):
        self.more = True
        self.times = [90, 290, 245, 1480, 350, 2300]
        self.nb = [2, 1, 1, 1, 2, 1]
        self.next = [self.next[0], self.next[1], self.next[2], self.random(3), self.random(4) // 2, self.random(5) // 2]
        self.add = AdditionalSpawn((0, 1, 1222))

    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_7', env.height, env.height)
        self.looting_title = env.mod.tools.load_img(env, 'waves/looting_wave_7', env.height, env.height)
        self.cross = env.mod.objects.Cross.build_class(env, 'waves/cross_wave_7')
        self.weapons = [env.mod.weapons.MagicWand, env.mod.weapons.ShadowDaggers]
        self.more = False
        self.times = [58, 220, 155]
        self.nb = [2, 1, 1]
        self.next = [0, 0, self.random(2)]
        env.background = env.background_shadows
        self.objective = env.mod.tools.spawn_boss(env, env.mod.monsters.Kraken)

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                self.spawn(env, i)
            else:
                self.next[i] -= 1
        if self.more:
            self.add.process(env)
        elif not self.objective.lives_nyx:
            self._more_monsters()
        if not self.objective.lives:
            env.background = env.background_basic
            return False
        return True

    def loot(self, env):
        env.titles.append(self.looting_title)
        env.objects.append(self.cross(x=int(0.2* env.width), y=int(0.5 *env.height)))
        if len(env.players) > 1:
            env.objects.append(self.cross(x=int(0.7* env.width), y=int(0.5 *env.height)))
        while len(env.objects):
            time.sleep(0.3)

        rand = randint(0, 1)
        env.objects.append(env.mod.objects.Weapon(env, x=int(0.2* env.width), y=int(0.5 *env.height), builder=self.weapons[rand]))
        if len(env.players) > 1:
            env.objects.append(env.mod.objects.Weapon(env, x=int(0.7* env.width), y=int(0.5 *env.height), builder=self.weapons[(rand + 1) % 2]))
        while len(env.objects):
            time.sleep(0.3)
        env.titles.remove(self.looting_title)

class   Wave8(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_8', env.height, env.height)
        self.objective = 42
        self.times = [79, 177, 212, 1180, 255, 1320, 88]
        self.nb = [3, 1, 1, 1, 2, 1, 3]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5), 0]
        self.add = AdditionalSpawn((0, 2, 788))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 6:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave9(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_9', env.height, env.height)
        self.objective = 13
        self.times = [79, 177, 212, 1180, 255, 1320, 90, 144]
        self.nb = [3, 1, 1, 1, 2, 1, 2, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5), self.random(6) // 2, 0]
        self.add = AdditionalSpawn((0, 2, 788))

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 7:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False
