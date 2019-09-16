import time

def wave(env, obj):
    tick = env.mod.tools.Tick()
    while True:
        if not obj.process(env):
            break
        tick.sleep(0.047)
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
    obj.loot(env)
    return not env.quit
