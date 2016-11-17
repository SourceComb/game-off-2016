from cocos.layer import ScrollableLayer

from ..entity import Player
from ..unit import mtr


_hspeed = 3 * mtr
_vspeed = 4 * mtr


class PlayerLayer(ScrollableLayer):
    '''Layer containing an active player.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)

        self.player = Player(map, 0, 0)
        self.add(self.player)

    def setxvel(self, val, d=None):
        '''Utility for setting players X velocity from input'''
        vel = val * _hspeed
        if d is None:
            self.player.input_vel.x = vel
        else:
            self.player.input_vel.x += vel * d

    def setjump(self, d):
        '''Utility for setting players Y velocity from jump input'''
        if d > 0 and self.player.grounded:
            self.player.vel.y += _vspeed
