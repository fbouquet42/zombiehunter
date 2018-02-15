
def display(env):
    for player in env.players:
        player.display(env)
    i = 0
    while i != len(env.monsters):
        if not env.monsters[i].degeneration:
            del env.monsters[i]
        else:
            env.monsters[i].display(env)
            i += 1
    i = 0
    while i != len(env.bullets):
        if not env.bullets[i].alive:
            del env.bullets[i]
        else:
            env.bullets[i].display(env)
            i += 1
    for title in env.titles:
        env.mod.tools.display(env, title, env.title_position, 0)

