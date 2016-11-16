from cocos.euclid import Vector2
from cocos.layer.scrolling import ScrollingManager
from cocos.scene import Scene
from cocos.tiles import load_tmx
from pyglet.gl import GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    glBindTexture, glTexParameteri
import pyglet.resource

from ..input import InputHandler, J, K
from ..layer.player import PlayerLayer


def load_map(mapname):
    pyglet.resource.path.insert(0, 'asset/map/' + mapname)
    pyglet.resource.reindex()
    layer = load_tmx('map.tmx')
    pyglet.resource.path.pop(0)
    pyglet.resource.reindex()
    return layer


class LevelScene(Scene, InputHandler):
    is_event_handler = True

    def __init__(self, lvlname):
        player = PlayerLayer()
        mgr = ScrollingManager()
        Scene.__init__(self, player, mgr)
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
            J.LSY: lambda val: player.setyvel(-val),

            J.RSX: self.updatecamx,
            J.RSY: self.updatecamy
        })

        level = load_map(lvlname)
        for tile in level['test_tiles'].values():
            tex = tile.image.get_texture()
            glBindTexture(tex.target, tex.id)
            glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.campos = Vector2(330, 380)
        self.camvel = Vector2(0, 0)
        self.mgr = mgr

        mgr.scale = 1.0
        mgr.add(level['topology'])
        mgr.set_focus(0, 0)

        self.schedule(self.tick)

    def updatecamx(self, value):
        self.camvel.x = value

    def updatecamy(self, value):
        self.camvel.y = -value

    def tick(self, dt):
        self.campos += self.camvel * dt * 60
        self.mgr.force_focus(self.campos.x, self.campos.y)

    def on_enter(self):
        Scene.on_enter(self)
        InputHandler.on_enter(self)

    def on_exit(self):
        Scene.on_exit(self)
        InputHandler.on_exit(self)
