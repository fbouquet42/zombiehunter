from random import randint

class   DefaultWave:
    def random(self, i):
        return randint(self.times[i], self.times[i]*2)
    
    def spawn(self, env, i):
        spawned = randint(1, self.nb[i])
        env.mod.tools.spawn(env, env.mod.monsters.tab[i], spawned)
        self.next[i] = self.random(i)
        return spawned

class   Wave1(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_1', env.height, env.height)
        self.objective = 70
        self.times = [45, 178]
        self.nb = [3, 1]
        self.next = [0, self.random(1)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 0:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False

class   Wave2(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_2', env.height, env.height)
        self.objective = 25
        self.times = [58, 180, 105]
        self.nb = [3, 1, 2]
        self.next = [0, self.random(1), self.random(2)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 2:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False

class   Wave3(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_3', env.height, env.height)
        self.times = [80, 230, 185]
        self.nb = [2, 1, 1]
        self.next = [0, self.random(1), self.random(2)]
        env.background = env.background_hell
        self.objective = env.mod.tools.spawn_boss(env, env.mod.monsters.Daemon)

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                self.spawn(env, i)
            else:
                self.next[i] -= 1
        if not self.objective.lives:
            env.background = env.background_basic
            return False
        return True

class   Wave4(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_4', env.height, env.height)
        self.objective = 5
        self.times = [69, 180, 220, 850]
        self.nb = [3, 1, 1, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 3:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False

class   Wave5(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_5', env.height, env.height)
        self.objective = 27
        self.times = [69, 180, 215, 1380, 102]
        self.nb = [3, 1, 1, 1, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 4:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False
"""
class   Wave6(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_6', env.height, env.height)
        self.objective = 4
        self.times = [71, 185, 220, 1380, 263, 1050]
        self.nb = [3, 1, 1, 1, 2, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4), self.random(5) // 2]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 5:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False
"""
class   Wave6(DefaultWave):
    def __init__(self, env):
        self.title = env.mod.tools.load_img(env, 'waves/wave_6', env.height, env.height)
        self.objective = 4
        self.times = [10000, 185, 220, 1380, 263, 1050]
        self.nb = [3, 1, 1, 1, 2, 1]
        self.next = [self.random(0), self.random(0), self.random(0), self.random(0), self.random(0), 0]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 5:
                    self.objective -= spawned
            else:
                self.next[i] -= 1
        if self.objective > 0:
            return True
        return False
