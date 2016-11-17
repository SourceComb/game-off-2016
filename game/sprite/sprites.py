from .sheet import *

class PlayerSheet(Spritesheet):
    info.canvas = 'asset/sprite/test.png'
    info.defaults.rate = 8


class PlayerSprite(PlayerSheet):
    idle = Sprite(pos=(256, 480), size=(32, 32), frames=2, scale=2, rate=1)
    run = Sprite(pos=(256, 448), size=(32, 32), frames=8, scale=4, rate=10)




