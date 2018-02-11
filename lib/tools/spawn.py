from threading import Thread
from random import randint

def spawn(env, monster, nb=1):
    while nb:
        x = randint(-200, 0)
        y = randint(-200, 0)
        obj = monster(env, x, y)
        t = Thread(target=obj.move, args=())
        t.daemon = True
        env.monsters.append(obj)
        t.start()
        nb -= 1
