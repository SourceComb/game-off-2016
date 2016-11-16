from sheet import *


class MainSheet(Spritesheet):
    info.canvas = 'assets/player.png'
    info.defaults.scale = 2
    info.defaults.rate = 8


class PlayerSprite(MainSheet):
    idle = Sprite(pos=(0, 0), size=(28, 32))
    run = Sprite(pos=(0, 32), size=(28, 32), frames=8)


class WeaponSprite(MainSheet):
    info.defaults.scale = 1
    axe_static = Sprite(pos=(28, 0), size=(84, 32))
    axe_swing = Sprite(pos=(0, 64), size=(84, 32), frames=4)


################################################################################
from sprite import PlayerSprite
from cocos.sprite import Sprite


PlayerSprite.load()

# ...
sprite = Sprite(PlayerSprite.idle, ...)
# ...
