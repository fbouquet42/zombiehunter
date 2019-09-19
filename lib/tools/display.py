
def display(env, img, x, y, fitting=0):
    if env.jerk:
        fitting += env.jerk_fitting
    env.GameWindow.blit(img, (int(x - fitting), int(y - fitting)))
