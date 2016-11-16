from cocos.euclid import Vector2
from .component import Entity, MapCollidable, Spritable
from ..sprite.test import StickSprite


class Player(Entity, Spritable, MapCollidable):
    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y), (32, 32))
        Spritable.__init__(self, StickSprite.idle)
        MapCollidable.__init__(self, map, 'slide')

        self.input_vel = Vector2(0, 0)

    def _apply_velocity(self, dt):
        self.vel = self.input_vel
        MapCollidable._apply_velocity(self, dt)
