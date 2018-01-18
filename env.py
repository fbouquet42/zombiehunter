from threading import Thread
import events

class Env:
    def __init__(self, width, height, img_src, player_dimensions, debug=False):
        self.debug = debug
        self.width = width
        self.height = height
        self.player_dimensions = player_dimensions
        self.pause = False
        self.img_src = img_src
        self.jerk = False
        self.players =[]
        self.monsters = []
        self.bullets = []

    def start(self):
        t = Thread(target=events.auto, args=(self, ))
        t.daemon = True
        t.start()
