from cocos.director import director
from cocos.euclid import Vector2
from cocos.layer.base_layers import Layer
import pyglet.input

import pyglet.window.key as K

class J:
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    BACK = 6
    START = 7
    LSPUSH = 9
    RSPUSH = 10

    LSX = 'x'
    LSY = 'y'
    RSX = 'rx'
    RSY = 'ry'
    LT = 'z'
    RT = 'rz'
    HATX = 'hat_x'
    HATY = 'hat_y'


class XInputHandler:
    def __init__(self, *joysticks):
        if len(joysticks) == 0:
            joysticks = list(pyglet.input.get_joysticks())
        self.joysticks = joysticks

    def on_enter(self):
        for joy in self.joysticks:
            joy.open()
            joy.push_handlers(self)

    def on_exit(self):
        for joy in self.joysticks:
            joy.remove_handlers(self)


def _getaction(bindings, device1, device2, key=None):
    if key is None:
        key = device2
        device2 = None

    if device1 in bindings:
        bindings = bindings[device1]
    elif device2 in bindings:
        bindings = bindings[device2]
    else:
        return None

    return bindings[key] if key in bindings else None


class InputHandler(XInputHandler):
    def __init__(self):
        XInputHandler.__init__(self)
        self.bindings = {}

    def on_enter(self):
        if not isinstance(self, Layer):
            director.window.push_handlers(self)
        XInputHandler.on_enter(self)

    def on_exit(self):
        if not isinstance(self, Layer):
            director.window.remove_handlers(self)
        XInputHandler.on_exit(self)

    def on_key_press(self, key, mod):
        action = _getaction(self.bindings, 'keyboard', key)
        if action is not None:
            action(1)
            return True

    def on_key_release(self, key, mod):
        action = _getaction(self.bindings, 'keyboard', key)
        if action is not None:
            action(-1)
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        action = _getaction(self.bindings, 'mouse', 'move')
        if action is not None:
            action(Vector2(x, y), Vector2(dx, dy))
            return True

    def on_mouse_press(self, x, y, btn, mod):
        action = _getaction(self.bindings, 'mouse', btn)
        if action is not None:
            action(1, Vector2(x, y))
            return True

    def on_mouse_release(self, x, y, btn, mod):
        action = _getaction(self.bindings, 'mouse', btn)
        if action is not None:
            action(-1, Vector2(x, y))
            return True

    def on_joybutton_press(self, joy, button):
        action = _getaction(self.bindings, joy, 'joystick', button)
        if action is not None:
            action(1)
            return True

    def on_joybutton_press(self, joy, button):
        action = _getaction(self.bindings, joy, 'joystick', button)
        if action is not None:
            action(-1)
            return True

    def on_joyaxis_motion(self, joy, axis, value):
        action = _getaction(self.bindings, joy, 'joystick', axis)
        if action is not None:
            action(value)
            return True
