import pygame


pygame.init()


background = pygame.image.load('background.png')
display_width = 1366
display_height = 768

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Zombie Hunters')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
JackImg = pygame.image.load('jack.png')
img_width1, img_heigth1 = JackImg.get_rect().size
JackImg = pygame.transform.scale(JackImg, (img_width1 // 5, img_heigth1 // 5))
BaltImg = pygame.image.load('baltazar.png')
img_width2, img_heigth2 = BaltImg.get_rect().size
BaltImg = pygame.transform.scale(BaltImg, (img_width2 // 5, img_heigth2 // 5))
Hitbox = pygame.image.load('hitbox.png')
Hitbox1 = pygame.transform.scale(Hitbox, (img_width1 // 5, img_heigth1 // 5))
Hitbox2 = pygame.transform.scale(Hitbox, (img_width2 // 5, img_heigth2 // 5))
curr1 = JackImg
curr2 = BaltImg

fittingx1, fittingy1 = 0, 0
def jack(x,y, curr, key):
    global fittingx1
    global fittingy1

    if key > 1:
        fittingx1, fittingy1 = img_width1 // 20, img_heigth1 // 20
    elif key:
        fittingx1, fittingy1 = 0, 0
    gameDisplay.blit(curr, (x - fittingx1,y - fittingy1))
    gameDisplay.blit(Hitbox1, (x,y))

fittingx2, fittingy2 = 0, 0
def baltazar(x,y, curr, key):
    global fittingx2
    global fittingy2

    if key > 1:
        fittingx2, fittingy2 = img_width2 // 20, img_heigth2 // 20
    elif key:
        fittingx2, fittingy2 = 0, 0
    gameDisplay.blit(curr, (x - fittingx2,y - fittingy2))
    gameDisplay.blit(Hitbox2, (x,y))

x1 =  (display_width * 0.25)
y1 = (display_height * 0.5)
x2 =  (display_width * 0.75)
y2 = (display_height * 0.5)
#x, y = 0, 0

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.blit(background, (0, 0))

    newx1, newy1, rot1, key1 = 0, 0, 0, 0
    newx2, newy2, rot2, key2 = 0, 0, 0, 0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        newx1 -= 14
        rot1 += 90
        key1 += 1
    if pressed[pygame.K_UP]:
        newy1 -= 14
        if not key1:
            rot1 += 360
        key1 += 1
    if pressed[pygame.K_RIGHT]:
        newx1 += 14
        rot1 += 270
        key1 += 1
    if pressed[pygame.K_DOWN]:
        newy1 += 14
        rot1 += 180
        key1 += 1
    if newx1 and newy1:
        x1, y1 = x1 + newx1 / (2 ** 0.5), y1 + newy1 / (2 ** 0.5)
    else:
        x1, y1 = x1 + newx1, y1 + newy1
    if key1:
        curr1 = pygame.transform.rotate(JackImg, rot1 // key1)

    if pressed[pygame.K_a]:
        newx2 -= 14
        rot2 += 90
        key2 += 1
    if pressed[pygame.K_w]:
        newy2 -= 14
        if not key2:
            rot2 += 360
        key2 += 1
    if pressed[pygame.K_d]:
        newx2 += 14
        rot2 += 270
        key2 += 1
    if pressed[pygame.K_s]:
        newy2 += 14
        rot2 += 180
        key2 += 1
    if newx2 and newy2:
        x2, y2 = x2 + newx2 / (2 ** 0.5), y2 + newy2 / (2 ** 0.5)
    else:
        x2, y2 = x2 + newx2, y2 + newy2
    if key2:
        curr2 = pygame.transform.rotate(BaltImg, rot2 // key2)
        
    jack(x1,y1, curr1, key1)
    baltazar(x2,y2, curr2, key2)
    pygame.display.update()
    clock.tick(40)

pygame.quit()
quit()
