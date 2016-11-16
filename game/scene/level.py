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
        mgr = ScrollingManager()
        Scene.__init__(self, mgr)
        InputHandler.__init__(self)

        level = load_map(lvlname)
        for tile in level['test_tiles'].values():
            tex = tile.image.get_texture()
            glBindTexture(tex.target, tex.id)
            glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        lvlmap = level['tiles']

        self.campos = Vector2(0, 0)
        self.camvel = Vector2(0, 0)
        self.mgr = mgr

        mgr.scale = 1.0
        mgr.add(lvlmap)
        mgr.set_focus(*self.campos)

        spawns = level['spawns']

        player = PlayerLayer(lvlmap)
        self.player = player.player
        mgr.add(player)
        playerspawn = spawns.match(spawn_type='player')[0]
        self.player.center = playerspawn.center

        self.schedule(self.tick)

        self.bindings['keyboard'] = keybinds = {}
        keybinds.update({
            K.UP: player.setjump,
            K.LEFT: lambda d: player.setxvel(-1, d),
            K.RIGHT: lambda d: player.setxvel(1, d),
        })
        keybinds.update({
            K.SPACE: keybinds[K.UP],

            K.W: keybinds[K.UP],
            K.A: keybinds[K.LEFT],
            K.D: keybinds[K.RIGHT],

            K.H: keybinds[K.LEFT],
            K.K: keybinds[K.UP],
            K.L: keybinds[K.RIGHT],
        })

        self.bindings['joystick'] = {}
        self.bindings['joystick'].update({
            J.A: player.setjump,
            J.LSX: player.setxvel,

            J.RSX: self.updatecamx,
            J.RSY: self.updatecamy
        })

    def updatecamx(self, value):
        self.camvel.x = value

    def updatecamy(self, value):
        self.camvel.y = -value

    def tick(self, dt):
        self.campos += self.camvel * dt * 60
        playerpos = self.player.center
        self.mgr.force_focus(playerpos[0] + self.campos.x,
                             playerpos[1] + self.campos.y)

    def on_enter(self):
        Scene.on_enter(self)
        InputHandler.on_enter(self)

    def on_exit(self):
        Scene.on_exit(self)
        InputHandler.on_exit(self)
