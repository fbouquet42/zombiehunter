from threading import Thread

class   DefaultWeapon:

    def update(self, **kwargs):
        pass

    def not_pressed(self, **kwargs):
        pass

    def _shoot(self, env, player, bullet):
        obj = bullet(player.x, player.y, player.direction)
        t = Thread(target=obj.move, args=())
        t.daemon = True
        env.bullets.append(obj)
        t.start()
