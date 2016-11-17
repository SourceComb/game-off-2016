from .sheet import *

class CreatureSheet(Spritesheet):
    info.canvas = 'asset/sprite/creature.png'
    info.defaults.rate = 8


class PlayerSprite(CreatureSheet):
    idle_left =     Sprite(pos=(64, 64), size=(32, 32), scale=2,
                           frames=2, rate=1)
    idle_right =    Sprite(pos=(0, 64), size=(32, 32), scale=2,
                           frames=2, rate=1)

    run_left =      Sprite(pos=(0, 0), size=(32, 32), scale=2,
                           frames=8, rate=10)
    run_right =     Sprite(pos=(0, 32), size=(32, 32), scale=2,
                           frames=8, rate=10)

    jump_right =    Sprite(pos=(0, 96), size=(32, 32), scale=2,
                           frames=4, rate=10, repeat=False)
    jump_left =     Sprite(pos=(128, 96), size=(32, 32), scale=2,
                           frames=4, rate=10, repeat=False)
