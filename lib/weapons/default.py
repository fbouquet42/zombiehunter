from threading import Thread

class   DefaultWeapon:

    xp = 0
    level_up = 800

    def build_class(env):
        env.mod.bullets.DefaultBullet.build_class(env)

    def update(self, **kwargs):
        if int(self.xp) > self.level_up:
            self.evolve()

    def not_pressed(self, **kwargs):
        pass

    def _shoot(self, env, player, bullet):
        obj = bullet(player.x, player.y, player.direction)
        t = Thread(target=obj.move, args=())
        t.daemon = True
        env.bullets.append(obj)
        t.start()

    def desequip(self):
        pass

    def evolve(self):
        pass
