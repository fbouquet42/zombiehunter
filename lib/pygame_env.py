import pygame

class PyGameEnv(object):

    def __enter__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()
