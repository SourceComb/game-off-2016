from cocos.director import director
from cocos.euclid import Vector2
from cocos.layer.base_layers import Layer
import pyglet.input

import pyglet.window.key as K

class J:
    '''Joystick constants'''

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
    '''Mixin enabling use of joysticks the same way as key and mouse events are
    produced by default.

    Note that it does not automatically detect new controllers.'''

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
    '''Utility to find an action. `device2` is optional.

    If `device1` doesn't exist, `device2` will be tried instead. If there is no
    available binding for this device and action, None will be returned.'''
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
    '''Mixin providing an input binding system.

    Bindings are defined in the `self.bindings` dict. Keys of this dict are
    "devices". Individual joystick devices are recognised, as well as the
    strings `"keyboard"` (for any keyboard input), `"mouse"` (for any mouse
    input), and `"joystick"` (for any joystick input). Each device's value is
    another dict, with keys as the input control and values as functions to
    call.

    Keyboard bindings react to input on all connected keyboards. The keys in
    these bindings must be constants from `pyglet.window.key` (exported from
    this module as `K` for convenience). The only parameter passed to these
    functions is an integer indicating whether or not the key was pressed or
    released (1 or -1 respectively). Example keyboard bindings:

        self.bindings['keyboard'] = {
            K.SPACE: lambda s: s > 0 and player.jump()
        }

    Joystick bindings react to input on one joystick (where a specific joystick
    reference was given as the device), or on all joysticks (where the string
    `"joystick"` was given as the device). The keys in these bindings must be
    constants from the `J` namespace exported from this module. For button
    bindings, the parameters are the same as for keyboard bindings. For axis
    bindings, the only parameter passed is the current "value" of this axis -
    some value between -1 and 1 inclusive (0 is the neutral position for most
    axes, -1 is neutral for trigger axes). Note that Y axes use -1 for "up",
    contradicting the convention for the entity and display system. Example
    joystick bindings:

        self.bindings['joystick'] = {
            J.A: lambda s: s > 0 and player.jump()
            J.RSY: lambda val: camera.vel.y = -val
        }

    TODO: Document mouse bindings

    Note that for reliable operation, ensure you call on_enter and on_exit from
    your own enter and exit methods. If you are subclassing, remember to call
    `InputHandler.__init__(self)` from the subclass constructor.
    '''

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
