from cocos.layer import Layer

from .traits import XInputHandler


class PlayerLayer(Layer, XInputHandler):
    def __init__(self):
        Layer.__init__(self)
        XInputHandler.__init__(self)

    def on_enter(self):
        Layer.on_enter(self)
        XInputHandler.on_enter(self)

    def on_exit(self):
        Layer.on_exit(self)
        XInputHandler.on_exit(self)
