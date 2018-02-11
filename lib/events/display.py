from threading import Thread

def _keys_manager(env):
    players_alive = 0
    for player in env.players:
        if not player.lives:
            if env.walking_dead and not player.possessed:
                player.undead(env)
            continue
        direction = env.mod.tools.set_direction(env.pressed, player)
        if direction >= 0:
            player.move(direction)
        if env.pressed[player.shoot]:
            player.weapon.pressed(env, player)
        else:
            player.weapon.not_pressed(env=env, player=player)
        players_alive += 1
    env.players_alive = players_alive

def display(env):
    _keys_manager(env)
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

