#Python Lib
#import sys

#Local Lib
from lib import Game, PyGameEnv

"""
while not env.closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.closed = True

    env.display()
    pygame.display.update()

    if env.pause:
        env.mod.menus.pause(env)
    if env.closed:
        pass
    elif not env.players_alive:
        env.mod.menus.game_over(env)
    elif env.credits:
        env.mod.menus.credits(env)
    clock.tick(30)
"""
def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    with PyGameEnv():
        main()
