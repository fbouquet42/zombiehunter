import time

class   _Tick:
    def __init__(self):
        self.time = time.time()

def wave(env, obj):
    tick = _Tick()
    while True:
        if not obj.process(env):
            break
        time.sleep(env.mod.tools.clock(tick, wait=0.1))
        while env.pause:
            time.sleep(0.3)
        if env.quit:
            while env.quit:
                time.sleep(0.1)
            return False
    while len(env.monsters):
        time.sleep(0.3)
    for player in env.players:
        player.lives = player.max_lives
    return not env.quit
