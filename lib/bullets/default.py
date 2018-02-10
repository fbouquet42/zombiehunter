
class   DefaultBullet:
    attack=1
    def build_class(env):
        DefaultBullet.env = env
        DefaultBullet.dimensions = env.player_dimensions
        DefaultBullet.limitx = env.width + 100
        DefaultBullet.limity = env.height + 100
        DefaultBullet.tools = env.mod.tools
        return DefaultBullet

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        self.fitting = 0.23 * self.dimensions if self.direction % 2 else 0

    def display(self, env):
        self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def _limits_reached(self):
        if self.x < -100 or self.y < -100 or self.y > self.limity or self.x > self.limitx:
            return True
        return False
    
    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        for monster in self.env.monsters:
            if monster.affected(self):
                self.player.score += monster.hitted(attack=self.attack)
                ret = True
        return ret

    def _dead(self):
        self.alive = False

    def _quit():
        time.sleep(self.tools.clock(self))
        while self.env.pause:
            if self.env.quit:
                return True
            time.sleep(self.tools.clock(self))
        return self.env.quit

    def move(self):
        self.time = time.time()
        while True:
            self.tools.move(self, self.direction)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            if self._quit():
                return
