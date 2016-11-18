from cocos.euclid import Vector2
from cocos.layer.scrolling import ScrollingManager
from cocos.scene import Scene
from cocos.tiles import load_tmx
from pyglet.gl import GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    glBindTexture, glTexParameteri
import pyglet.resource

from ..input import InputHandler, J, K
from ..layer.player import PlayerLayer
from ..layer.enemy import EnemyLayer
from ..unit import mtr


def load_map(mapname):
    '''Hack to ensure maps with relative image paths get loaded correctly,
    by manipulating pyglet.resource.path.'''
    pyglet.resource.path.insert(0, 'asset/map/' + mapname)
    pyglet.resource.reindex()
    layer = load_tmx('map.tmx')
    pyglet.resource.path.pop(0)
    pyglet.resource.reindex()
    return layer


class LevelScene(Scene, InputHandler):
    '''Game level scene, implementing main level logic.'''

    is_event_handler = True

    def __init__(self, lvlname):
        mgr = ScrollingManager()
        Scene.__init__(self, mgr)
        InputHandler.__init__(self)

        # Load level and set scaling properties on tilesets
        level = load_map(lvlname)
        for tile in level['test_tiles'].values():
            tex = tile.image.get_texture()
            glBindTexture(tex.target, tex.id)
            glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Get map for displaying and use in collision checking
        lvlmap = level['tiles']

        # Set info for use in camera controls
        self.cam_pos = Vector2(0, 0)
        self.camvel = Vector2(0, 0)
        self.mgr = mgr
        # Set up scroll manager
        mgr.scale = 1.0
        mgr.add(lvlmap)
        mgr.set_focus(*self.cam_pos)

        # Add entity layers
        player_layer = PlayerLayer(lvlmap)
        self.player = player_layer.player
        mgr.add(player_layer)
        enemy_layer = EnemyLayer(lvlmap)
        mgr.add(enemy_layer)

        # Spawn entities based on locations set in map
        spawns = level['spawns']
        for obj in spawns.objects:
            if obj.usertype == 'enemy_spawn':
                enemy_layer.spawn(obj['entity_type'], (obj.x, obj.y))
            elif obj.usertype == 'player_spawn':
                self.player.center = obj.center
            else:
                print('[WARN]: Cannot spawn', obj.usertype,
                      '(entity_type == {!r})'.format(obj['entity_type']))

        # Set input bindings
        # Extra binding functions
        def updatecamx(value):
            self.camvel.x = value
        def updatecamy(value):
            self.camvel.y = -value
        # Keyboard bindings
        self.bindings['keyboard'] = keybinds = {}
        # Basic binds
        keybinds.update({
            K.UP: player_layer.setjump,
            K.LEFT: lambda d: player_layer.setxvel(-1, d),
            K.RIGHT: lambda d: player_layer.setxvel(1, d),
        })
        # Extra binds
        keybinds.update({
            K.SPACE: keybinds[K.UP],

            K.W: keybinds[K.UP],
            K.A: keybinds[K.LEFT],
            K.D: keybinds[K.RIGHT],

            K.H: keybinds[K.LEFT],
            K.K: keybinds[K.UP],
            K.L: keybinds[K.RIGHT],
        })
        # Joystick bindings
        self.bindings['joystick'] = {}
        self.bindings['joystick'].update({
            J.A: player_layer.setjump,
            J.LSX: player_layer.setxvel,

            J.RSX: updatecamx,
            J.RSY: updatecamy
        })

        # Set update loop
        self.schedule(self.tick)

    def tick(self, dt):
        '''Update camera'''
        self.cam_pos += self.camvel * dt * 8 * mtr
        player_pos = self.player.center
        self.mgr.force_focus(player_pos[0] + self.cam_pos.x,
                             player_pos[1] + self.cam_pos.y)

    def on_enter(self):
        Scene.on_enter(self)
        InputHandler.on_enter(self)

    def on_exit(self):
        Scene.on_exit(self)
        InputHandler.on_exit(self)
