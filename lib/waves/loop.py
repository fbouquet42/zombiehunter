#Python Lib
import time

#Current Module
from . import _waves
from . import wave

def _init(env):
    title = env.mod.tools.load_img(env, 'waves/loading_0', env.height, env.height)
    env.titles.append(title)
    env.mod.monsters.DefaultMonster.build_class(env)
    env.mod.monsters.Zombie.build_class()
    env.mod.monsters.Cyclops.build_class()
    env.titles.remove(title)
    title = env.mod.tools.load_img(env, 'waves/loading_1', env.height, env.height)
    env.titles.append(title)
    env.mod.monsters.Devourer.build_class()
    env.mod.monsters.DarkKnight.build_class()
    env.mod.monsters.Fly.build_class()
    env.mod.monsters.JackLantern.build_class()
    env.mod.monsters.Ent.build_class()
    env.titles.remove(title)
    title = env.mod.tools.load_img(env, 'waves/loading_2', env.height, env.height)
    env.titles.append(title)
    env.mod.weapons.MagicWand.build_class(env)
    env.mod.weapons.DragonHead.build_class(env)
    env.mod.weapons.DevilBlade.build_class(env)
    env.mod.monsters.Necromancer.build_class()
    env.mod.monsters.Harpy.build_class()
    env.mod.monsters.MotherOfTheVermine.build_class()
    env.titles.remove(title)
    title = env.mod.tools.load_img(env, 'waves/loading_3', env.height, env.height)
    env.titles.append(title)
    env.mod.weapons.ShadowDaggers.build_class(env)
    env.mod.monsters.Villager.build_class()
    env.mod.monsters.Witch.build_class()
    env.mod.monsters.Alchemist.build_class(env)
    env.mod.monsters.Piranha.build_class()
    env.titles.remove(title)
    title = env.mod.tools.load_img(env, 'waves/loading_4', env.height, env.height)
    env.titles.append(title)
    env.mod.monsters.AbstractGargamel.build_class()
    env.titles.remove(title)

def loop(env):
    buff = 0
    _init(env)
    while True:
        if env.retry:
            i = buff
            env.retry = False
        elif env.debug:
            i = env.debug_wave - 1
        else:
            i = 0
        while i < len(_waves):
            obj = _waves[i](env)
            env.titles.append(obj.title)
            time.sleep(5)
            env.titles.remove(obj.title)
            if not wave(env, obj):
                buff = i
                break
            else:
                i += 1
        if i == len(_waves):
            env.quit = True
            env.credits = True
        while env.quit:
            time.sleep(0.2)
