from cocos.euclid import Vector2
from cocos.layer import ScrollableLayer
import pyglet.window.key as K

from ..entity import Player


class PlayerLayer(ScrollableLayer):
    '''Layer containing an active player.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)

        self.speed = 120

        self.player = Player(map, 0, 0)
        self.add(self.player)

    def setxvel(self, val, d=None):
        '''Utility for setting players X velocity from input'''
        vel = val * self.speed
        if d is None:
            self.player.input_vel.x = vel
        else:
            self.player.input_vel.x += vel * d

    def setjump(self, d):
        if d > 0 and self.player.grounded:
            self.player.vel.y += 64
