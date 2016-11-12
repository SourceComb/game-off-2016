from cocos.euclid import Vector2
from cocos.layer import ColorLayer
import pyglet.window.key as K

from .traits import XInputHandler
from ..entity import Player


class PlayerLayer(ColorLayer, XInputHandler):
    is_event_handler = True

    def __init__(self):
        ColorLayer.__init__(self, 255, 255, 255, 255)
        XInputHandler.__init__(self)

        self.player = Player(100, 100)
        self.add(self.player)

        self.keybinds = {
            K.W: lambda s: self.setmove(0, 1, s),
            K.A: lambda s: self.setmove(-1, 0, s),
            K.S: lambda s: self.setmove(0, -1, s),
            K.D: lambda s: self.setmove(1, 0, s),
        }

        self.jabinds = {
            'x': lambda val: self.setvel(val, 0),
            'y': lambda val: self.setvel(0, -val),
        }

    def setvel(self, x, y):
        vec = Vector2(x, y) * 120
        if vec.y == 0:
            self.player.vel.x = vec.x
        elif vec.x == 0:
            self.player.vel.y = vec.y
        else:
            self.player.vel = vec

    def setmove(self, x, y, state):
        vec = Vector2(x, y) * 60
        if not state:
            vec = -vec
        self.player.vel += vec

    def on_enter(self):
        ColorLayer.on_enter(self)
        XInputHandler.on_enter(self)

    def on_exit(self):
        ColorLayer.on_exit(self)
        XInputHandler.on_exit(self)

    def on_key_press(self, key, mod):
        if key in self.keybinds:
            self.keybinds[key](True)
            return True

    def on_key_release(self, key, mod):
        if key in self.keybinds:
            self.keybinds[key](False)
            return True

    def on_joyaxis_motion(self, joy, axis, value):
        if axis in self.jabinds:
            self.jabinds[axis](value)
            return True
