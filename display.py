import pygame

def set_imgs(env, player):
    player.img = []
    player.img.append(pygame.image.load(env.img_src + player.name + '.png'))
    player.img[0] = pygame.transform.scale(player.img[0], (player.dimensions, player.dimensions))
    player.img.append(pygame.transform.rotate(player.img[0], 45))
    player.img.append(pygame.transform.rotate(player.img[0], 90))
    player.img.append(pygame.transform.rotate(player.img[0], 135))
    player.img.append(pygame.transform.rotate(player.img[0], 180))
    player.img.append(pygame.transform.rotate(player.img[0], 225))
    player.img.append(pygame.transform.rotate(player.img[0], 270))
    player.img.append(pygame.transform.rotate(player.img[0], 315))

    player.curr_img = player.img[0]
    env.to_display.append(player)
