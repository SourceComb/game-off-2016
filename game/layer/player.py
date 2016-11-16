from cocos.euclid import Vector2
from cocos.layer import ScrollableLayer
import pyglet.window.key as K

from ..entity import Player


class PlayerLayer(ScrollableLayer):
    '''Layer containing an active player.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)

        self.speed = 120

        self.player = Player(map, 100, 100)
        self.add(self.player)

    def setxvel(self, val, d=None):
        '''Utility for setting players X velocity from input'''
        vel = val * self.speed
        if d is None or d > 0:
            self.player.vel.x = vel
        else:
            self.player.vel.x = 0

    def setyvel(self, val, d=None):
        '''Utility for setting players Y velocity from input'''
        vel = val * self.speed
        if d is None or d > 0:
            self.player.vel.y = vel
        else:
            self.player.vel.y = 0
