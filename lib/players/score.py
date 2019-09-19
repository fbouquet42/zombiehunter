import pygame

class   Score:

    def __init__(self, env, player, x, y, dimensions):
        self.time = 60
        self.i = 0
        self.total = 0
        self.x = x
        self.y = y
        self.font = player.font
        self.half = player.half
        self.tools = player.tools
        self.img_total = player.img[0]
        self.list = ['zombie', 'cyclops', 'jack_lantern', 'daemon', 'minion', 'necromancer', 'harpy', 'ent', 'nyx', 'tentacle', 'piranha', 'kraken', 'dark_knight', 'villager', 'garou']
        self.kills = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.values = [1, 3.5, 2.5, 0.135, 2, 7, 3, 0.1, 0.12, 0.1, 3, 0.145, 11, 1, 4.5]
        self.img = []
        for name in self.list:
            self.load_img(env, name, dimensions)

    def load_img(self, env, name, dimensions):
        img = pygame.image.load(env.img_folder + 'monsters/' + name + '.png')
        self.img.append(pygame.transform.scale(img, (dimensions, dimensions)))

    def up(self):
        while self.i:
            self.i -= self.i % self.time
            self.i -= self.time
            if self.i < 0:
                self.i = 0
            if self.kills[self.i // self.time]:
                break
    def down(self):
        if not self.i // self.time < len(self.list):
            return
        while True:
            self.i += (self.time - self.i % self.time)
            if not self.i // self.time < len(self.list):
                break
            if self.kills[self.i // self.time]:
                break

    def calculate(self):
        for i in range(0, len(self.list)):
            self.total += int(self.values[i] * self.kills[i])

    def display(self, env, color):
        id_nb = self.i // self.time
        if id_nb < len(self.list):
            if not self.kills[id_nb]:
                self.i += self.time
                return self.display(env, color)
            score = self.font.render(str(int(self.values[id_nb] * self.kills[id_nb])), False, color)
            self.tools.display(env, self.img[id_nb], self.x, self.y)
            self.tools.display(env, score, self.x, self.y - self.half // 2)
            self.i += 1
        else:
            score = self.font.render(str(self.total), False, color)
            self.tools.display(env, self.img_total, self.x, self.y)
            self.tools.display(env, score, self.x, self.y - self.half // 2)
