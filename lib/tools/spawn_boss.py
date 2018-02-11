from threading import Thread
from random import randint

def spawn_boss(env, boss):
    x = randint(-200, 0)
    y = randint(-200, 0)
    obj = boss(env, x, y)
    t = Thread(target=obj.move, args=())
    t.daemon = True
    self.monsters.append(obj)
    t.start()
    return obj
