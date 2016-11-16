from .sheet import *

class TestSheet(Spritesheet):
    info.canvas = 'asset/sprite/test.png'
    info.defaults.rate = 8


class StickSprite(TestSheet):
    idle = Sprite(pos=(256, 480), size=(32, 32), frames=2, scale=2, rate=2)
    run = Sprite(pos=(0, 256), size=(64, 128), frames=4)
