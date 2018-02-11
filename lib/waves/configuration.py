from random import randint

class   DefaultWave:
    def random(self, i):
        return randint(self.times[i], self.times[i]*2)
    
    def spawn(self, env, i):
        spawned = randint(1, self.nb[i])
        env.mod.tools.spawn(env.mod.monsters.tab[i], spawned)
        self.next[i] = self.random(i)
        return spawned

class   Wave1(DefaultWave):
    def __init__(self, env):
        title = env.mod.tools.load_img(env, 'waves/wave_1', env.height, env.height)
        self.objective = 65
        self.times = [14, 65]
        self.nb = [3, 1]
        self.next = [0, self.random(1)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 0:
                    self.objective -= spawned
        if self.objective > 0:
            return False
        return True

class   Wave2(DefaultWave):
    def __init__(self, env):
        title = env.mod.tools.load_img(env, 'waves/wave_2', env.height, env.height)
        self.objective = 25
        self.times = [17, 70, 65]
        self.nb = [3, 1, 2]
        self.next = [0, self.random(1), self.random(2)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 2:
                    self.objective -= spawned
        if self.objective > 0:
            return False
        return True

class   Wave3(DefaultWave):
    def __init__(self, env):
        title = env.mod.tools.load_img(env, 'waves/wave_3', env.height, env.height)
        self.times = [20, 80, 95]
        self.nb = [2, 1, 1]
        self.next = [0, self.random(1), self.random(2)]
        env.background = env.background_hell
        self.objective = env.mod.tools.spawn_boss(env, env.mod.monsters.Daemon)

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                self.spawn(env, i)
        if not self.objective.lives :
            env.background = env.background_basic
            return False
        return True

class   Wave4(DefaultWave):
    def __init__(self, env):
        title = env.mod.tools.load_img(env, 'waves/wave_4', env.height, env.height)
        self.objective = 7
        self.times = [18, 72, 80, 130]
        self.nb = [3, 1, 1, 1]
        self.next = [0, self.random(1), self.random(2), self.random(3)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 3:
                    self.objective -= spawned
        if self.objective > 0:
            return False
        return True

class   Wave5(DefaultWave):
    def __init__(self, env):
        title = env.mod.tools.load_img(env, 'waves/wave_5', env.height, env.height)
        self.objective = 48
        self.times = [18, 70, 82, 210, 32]
        self.nb = [3, 1, 1, 1, 2]
        self.next = [0, self.random(1), self.random(2), self.random(3), self.random(4)]

    def process(self, env):
        for i, value in enumerate(self.next):
            if not value:
                spawned = self.spawn(env, i)
                if i == 4:
                    self.objective -= spawned
        if self.objective > 0:
            return False
        return True
