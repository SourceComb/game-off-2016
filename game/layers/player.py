from cocos.actions import *
from cocos.layer import Layer
from cocos.text import Label

import pyglet.window.key as K

from .traits import XInputHandler


KEYS_UP = K.UP, K.W, K.K
KEYS_DOWN = K.DOWN, K.S, K.J
KEYS_LEFT = K.LEFT, K.A, K.H
KEYS_RIGHT = K.RIGHT, K.D, K.L


class PlayerLayer(Layer, XInputHandler):
    is_event_handler = True
    def __init__(self):
        Layer.__init__(self)
        XInputHandler.__init__(self)

        self.player_sprite = Label('\n',
                font_name='Liberation Mono',
                font_size=32)
        self.player_sprite.position = 100, 100
        self.add(self.player_sprite)
        self.movement = [None, None]

    def _stop(self, action):
        if action is not None:
            self.player_sprite.remove_action(action)

    def on_key_press(self, key, mod):
        duration = 1.0/60
        movement = self.movement
        if key in KEYS_UP:
            self._stop(movement[1])
            action = Repeat(MoveBy((0, 1), duration))
            movement[1] = self.player_sprite.do(action)
        elif key in KEYS_DOWN:
            self._stop(movement[1])
            action = Repeat(MoveBy((0, -1), duration))
            movement[1] = self.player_sprite.do(action)
        elif key in KEYS_LEFT:
            self._stop(movement[0])
            action = Repeat(MoveBy((-1, 0), duration))
            movement[0] = self.player_sprite.do(action)
        elif key in KEYS_RIGHT:
            self._stop(movement[0])
            action = Repeat(MoveBy((1, 0), duration))
            movement[0] = self.player_sprite.do(action)

    def on_key_release(self, key, mod):
        if key in KEYS_UP or key in KEYS_DOWN:
            self._stop(self.movement[1])
            self.movement[1] = None
        elif key in KEYS_LEFT or key in KEYS_RIGHT:
            self._stop(self.movement[0])
            self.movement[0] = None

    def on_enter(self):
        Layer.on_enter(self)
        XInputHandler.on_enter(self)

    def on_exit(self):
        Layer.on_exit(self)
        XInputHandler.on_exit(self)
