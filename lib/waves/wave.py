
class   _Tick:
    def __init__(self):
        self.time = time.time()

def wave(env, obj):
    tick = _Tick()
    while True:
        if not obj.process(env):
            break
        time.sleep(env.mod.tools.clock(tick), wait=0.1)
        while env.pause:
            time.sleep(0.3)
        if env.quit:
            return False
    while len(env.monsters):
        time.sleep(0.2)
    return True
