from .sheet import *

class TestSheet(Spritesheet):
    info.canvas = 'asset/sprite/test.png'
    info.defaults.rate = 8


class StickSprite(TestSheet):
    idle = Sprite(pos=(256, 448), size=(64, 64), frames=1)
    run = Sprite(pos=(0, 256), size=(64, 128), frames=4)
