
def update_tick(env):
    tick = env.mod.tools.Tick()
    while True:
        for player in env.players:
            player.update()

        for monster in env.monsters:
            monster.update()

        for obj in env.objects:
            obj.update()

        tick.sleep()
        while env.pause:
            tick.sleep()

