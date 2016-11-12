from cocos.scene import Scene

from ..input import InputHandler, J, K
from ..layer.player import PlayerLayer


class LevelScene(Scene, InputHandler):
    is_event_handler = True

    def __init__(self):
        player = PlayerLayer()
        Scene.__init__(self, player)
        InputHandler.__init__(self)

        self.bindings['keyboard'] = keybinds = {}
        keybinds.update({
            K.UP: lambda d: player.setyvel(1, d),
            K.DOWN: lambda d: player.setyvel(-1, d),
            K.LEFT: lambda d: player.setxvel(-1, d),
            K.RIGHT: lambda d: player.setxvel(1, d),
        })
        keybinds.update({
            K.W: keybinds[K.UP],
            K.A: keybinds[K.LEFT],
            K.S: keybinds[K.DOWN],
            K.D: keybinds[K.RIGHT],

            K.H: keybinds[K.LEFT],
            K.J: keybinds[K.DOWN],
            K.K: keybinds[K.UP],
            K.L: keybinds[K.RIGHT],
        })

        self.bindings['joystick'] = {}
        self.bindings['joystick'].update({
            J.LSX: player.setxvel,
            J.LSY: lambda val: player.setyvel(-val)
        })

    def on_enter(self):
        Scene.on_enter(self)
        InputHandler.on_enter(self)

    def on_exit(self):
        Scene.on_exit(self)
        InputHandler.on_exit(self)
