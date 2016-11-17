from .sheet import *

class PlayerSheet(Spritesheet):
    info.canvas = 'asset/sprite/test.png'
    info.defaults.rate = 8


class PlayerSprite(PlayerSheet):
    right_idle = Sprite(
        pos=(256, 480), size=(32, 32), frames=2, scale=2, rate=1
    )
    left_idle = Sprite(
        pos=(320, 480), size=(32, 32), frames=2, scale=2, rate=1
    )

    right_run = Sprite(
        pos=(256, 448), size=(32, 32), frames=8, scale=2, rate=10
    )
    left_run = Sprite(
        pos=(256, 416), size=(32, 32), frames=8, scale=2, rate=10
    )




