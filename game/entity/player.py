from .component import Entity, Spritable
from ..sprite.test import StickSprite


class Player(Entity, Spritable):
    def __init__(self, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, StickSprite.idle)
