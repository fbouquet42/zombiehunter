import pygame

from .configuration import Configuration

class Game(object):
    def __init__(self):
        self.closed = False
        info = pygame.display.Info()
        config = Configuration(info)
        self.window = pygame.display.set_mode((config.width, config.height), pygame.FULLSCREEN)

    def display(self):
        self.window.fill((77,77,77))

    def run(self):
        clock = pygame.time.Clock()
        while not self.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.closed = True
            self.display()
            pygame.display.update()
            clock.tick(60)
