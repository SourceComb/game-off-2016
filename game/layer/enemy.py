from cocos.euclid import Vector2
from cocos.layer import ScrollableLayer

from ..entity import enemy


class EnemyLayer(ScrollableLayer):
    '''Layer containing active enemies.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)
        self.map = map

    def spawn(self, etype, pos):
        if isinstance(etype, str):
            if hasattr(enemy, etype):
                etype = getattr(enemy, etype)
            else:
                print('[WARN]: No such enemy type ', repr(etype))
                return
        enemy = etype(pos, self.map)
        self.add(enemy)
