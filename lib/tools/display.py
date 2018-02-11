
def display(env, img, x, y, fitting=0):
    if env.jerk:
        fitting += 23
    env.GameWindow.blit(img, (int(x - fitting), int(y - fitting)))
