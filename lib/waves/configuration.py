from random import randint
import time
#
#

class   AdditionalSpawn:
    def random(self, nb):
        return randint(nb, nb * 3)

    def __init__(self, dark_knight, fly=None):
        self.dark_min, self.dark_max, self.dark_time = dark_knight
        self.dark_next = self.random(self.dark_time)
        if fly is not None:
            self.fly_min, self.fly_max, self.fly_time = fly
            self.fly_next = self.random(self.fly_time)
        else:
            self.fly_next = -1

    def process(self, env):
        if not self.dark_next:
            env.mod.tools.spawn(env, env.mod.monsters.DarkKnight, randint(self.dark_min, self.dark_max))
            self.dark_next = self.random(self.dark_time)
        else:
            self.dark_next -= 1

        if self.fly_next >= 0:
            if not self.fly_next:
                env.mod.tools.spawn(env, env.mod.monsters.Fly, randint(self.fly_min, self.fly_max))
                self.fly_next = self.random(self.fly_time)
            else:
                self.fly_next -= 1

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
        self.title = env.mod.tools.load_img(env, 'waves/gargamel', env.height, env.height)
        self.objective = 70
        self.times = [45, 178]
        self.nb = [3, 1]
        self.next = [0, self.random(1)]
        #self.add = AdditionalSpawn((0, 1, 799), (0, 1, 899))
        self.add = AdditionalSpawn((0, 1, 110), (0, 1, 899))
        #gargamel test
        env.mod.tools.spawn_boss(env, env.mod.monsters.Gargamel)

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
        self.add = AdditionalSpawn((0, 1, 888), (0, 1, 999))

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
        self.weapons = [env.mod.weapons.DragonHead, env.mod.weapons.DevilBlade]
        self.times = [80, 230, 185]
        self.nb = [2, 1, 1]
        self.next = [0, self.random(1), self.random(2)]
        self.add = AdditionalSpawn((0, 1, 1222), (0, 1, 1444))
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
        self.add = AdditionalSpawn((0, 2, 799), (0, 2, 811))

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
        self.objective = 28
        self.times = [69, 180, 215, 1280, 102]
        self.nb = [3, 1, 1, 1, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4)]
        self.add = AdditionalSpawn((0, 2, 888), (0, 2, 888))

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
        self.times = [71, 185, 220, 1280, 220, 900]
        self.nb = [3, 1, 1, 1, 2, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2]
        self.add = AdditionalSpawn((0, 2, 799), (0, 2, 666))

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
        self.times = [88, 260, 235, 1460, 290, 1750]
        self.nb = [3, 1, 1, 1, 2, 1]
        self.next = [self.next[0], self.next[1], self.next[2], self.random(3), self.random(4) // 2, self.random(5) // 2]
        self.add = AdditionalSpawn((0, 1, 999), (0, 2, 777))

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
        self.objective = 41
        self.times = [72, 177, 212, 1180, 235, 1320, 88]
        self.nb = [3, 1, 1, 1, 2, 1, 3]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5), 0]
        self.add = AdditionalSpawn((0, 2, 788), (1, 4, 599))

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
        self.objective = 19
        self.times = [84, 187, 212, 1180, 235, 1320, 144, 301]
        self.nb = [3, 1, 1, 1, 2, 1, 1, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5), self.random(6), 0]
        self.add = AdditionalSpawn((0, 2, 833), (0, 3, 822))

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


#self.times = [144, 187, 212, 1280, 166, 1520, 144, 401]
#self.nb = [3, 1, 1, 1, 2, 1, 1, 1]

class   Wave10(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_10', env.height, env.height)
        self.objective = 28
        self.times = [144, 97, 212, 1280, 166, 1520, 144, 401, 199]
        self.nb = [3, 1, 1, 1, 2, 1, 1, 1, 3]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2, self.random(6), self.random(7), 0]
        self.add = AdditionalSpawn((0, 2, 833))

    def process(self, env):
        for i, value in enumerate(self.next):
            if self.nb[i]:
                if not value:
                    spawned = self.spawn(env, i)
                    if i == 8:
                        self.objective -= spawned
                else:
                    self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave11(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_11', env.height, env.height)
        self.objective = 18
        self.times = [144, 187, 212, 1280, 166, 1520, 144, 401, 222, 299]
        self.nb = [2, 1, 1, 1, 2, 1, 1, 1, 2, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2, self.random(6), self.random(7), 0, 0]
        self.add = AdditionalSpawn((0, 2, 833))

    def process(self, env):
        for i, value in enumerate(self.next):
            if self.nb[i]:
                if not value:
                    spawned = self.spawn(env, i)
                    if i == 9:
                        self.objective -= spawned
                else:
                    self.next[i] -= 1
        self.add.process(env)
        if self.objective > 0:
            return True
        return False

class   Wave12(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_12', env.height, env.height)
        self.times = [102, 277, 212, 1480, 277, 1920, 122, 433]
        self.nb = [2, 1, 1, 1, 2, 1, 1, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2, self.random(6), self.random(7)]
        self.add = AdditionalSpawn((0, 1, 1222), (0, 1, 1444))
        env.background = env.background_swamp
        self.objective = env.mod.tools.spawn_boss(env, env.mod.monsters.Graeae)
#        self.objective.lives = 0

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                self.spawn(env, i)
            else:
                self.next[i] -= 1
        self.add.process(env)
        if not self.objective.splited_lives:
            env.background = env.background_basic
            return False
        return True
