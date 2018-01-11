from threading import Thread
import events

class Env:
    def __init__(self, width, heigth, img_src, debug=False):
        self.debug = debug
        self.width = width
        self.heigth = heigth
        self.pause = False
        self.img_src = img_src
        self.id = 0
        self.players = {}
        self.hitboxes = []
        self.to_display = []
        self.bullets = []

    def start(self):
        t = Thread(target=events.auto, args=(self, ))
        t.daemon = True
        t.start()
