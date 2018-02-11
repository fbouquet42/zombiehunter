import pygame

def     load_img(env, path, width, height):
    loaded = pygame.image.load(env.img_folder + path + '.png')
    loaded = pygame.transform.scale(loaded, (width, height))
    return loaded
