from threading import Thread
import events

class Env:
    def __init__(self, width, height, img_src, debug=False):
        self.debug = debug
        self.width = width
        self.height = height
        self.pause = False
        self.img_src = img_src
        self.id = 0
        self.players =[]
        self.monsters = []
        self.bullets = []

    def start(self):
        t = Thread(target=events.auto, args=(self, ))
        t.daemon = True
        t.start()
