from cocos.euclid import Vector2
from cocos.layer import ColorLayer
import pyglet.window.key as K

from ..entity import Player


class PlayerLayer(ColorLayer):
    def __init__(self):
        ColorLayer.__init__(self, 255, 255, 255, 255)

        self.speed = 120

        self.player = Player(100, 100)
        self.add(self.player)

    def setxvel(self, val, d=None):
        vel = val * self.speed
        if d is None:
            self.player.vel.x = vel
        else:
            self.player.vel.x += vel * d

    def setyvel(self, val, d=None):
        vel = val * self.speed
        if d is None:
            self.player.vel.y = vel
        else:
            self.player.vel.y += vel * d
