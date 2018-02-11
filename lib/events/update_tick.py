import time

class   _Tick:
    def __init__(self):
        self.time = time.time()

def update_tick(env):
    tick = _Tick()
    while True:
        for player in env.players:
            player.update()
        for monster in env.monsters:
            monster.update()
        time.sleep(env.mod.tools.clock(tick))
        while env.pause:
            time.sleep(env.mod.tools.clock(tick))

