#Python Lib
import time

#Current Module
from . import _waves
from . import wave

def _init(env):
    env.mod.monsters.DefaultMonster.build_class(env)
    env.mod.monsters.Zombie.build_class(env)
    env.mod.monsters.Cyclops.build_class(env)
    env.mod.monsters.JackLantern.build_class(env)
    env.mod.monsters.Minion.build_class(env)
    env.mod.monsters.Necromancer.build_class(env)
    env.mod.monsters.Harpy.build_class(env)

def loop(env):
    _init(env)
    while True:
        if env.debug:
            i = env.debug_wave
        else:
            i = 0
        while i < len(_waves):
            obj = _waves[i](env)
            env.titles.append(obj.title)
            time.sleep(5)
            env.titles.remove(obj.title)
            if not wave(env, _waves[i]):
                i = 0
            else:
                i += 1
        env.menus.credits(env)
