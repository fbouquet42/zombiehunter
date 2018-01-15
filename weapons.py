import tools
import pygame

class HitboxBullet:
    def update_coords(self, player):
        self.x = int(player.x + player.dimensions * 0.44)
        self.y = int(player.y + player.dimensions * 0.44)

    def __init__(self, player, dimensions):
        self.update_coords(player)
        self.dimensions = dimensions

def set_hitbox_bullet(env, bullet):
    hitbox = HitboxBullet(bullet, int(bullet.dimensions * 0.12))
    img = pygame.image.load(env.img_src + "hitbox.png")
    img = pygame.transform.scale(img, (hitbox.dimensions, hitbox.dimensions))
    hitbox.img = img
    return hitbox

class   BulletType:
    def __init__(self, env, player, name, rapidity):
        self.dimensions = player.dimensions
        self.name = name
        self.img = []
        tools.set_imgs(env, self.dimensions, self.name, self.img, 'bullets/')
        self.rapidity = rapidity

def set_bullet(env, player, weapon):
    bullet_type = None
    if weapon.name == "crossbow_unloaded":
        bullet_type = BulletType(env=env, player=player, name="arrow", rapidity=22)
    elif weapon.name == "submachine_gun_3":
        bullet_type = BulletType(env=env, player=player, name="bullet", rapidity=28)
    return bullet_type

class   Weapon:
    def __init__(self, env, player):
        self.dimensions = player.dimensions
        #self.img = []
        #tools.set_imgs(env, self.dimensions, self.name, self.img, 'weapons/')
        #self.bullet_type = set_bullet(env, player, self)
        self.cooldown = 0
        #self.cadence = cadence

class   Crossbow(Weapon):
    def __init__(self, env, player):
        super().__init__(self, player.dimensions)
        self.cadence = 45
        ##here

weapons = {'jack' : Crossbow, 'baltazar' : SubmachineGun}

def set_weapon(env, player):
    weapon = weapons[player.name](env=env, player=player)
    return weapon

    weapon = None
    if player.name == "jack":
        weapon = Weapon(env=env, player=player, name="crossbow_unloaded", cadence=45)
    elif player.name == "baltazar":
        weapon = Weapon(env=env, player=player, name="submachine_gun_3", cadence=20)
    return weapon
