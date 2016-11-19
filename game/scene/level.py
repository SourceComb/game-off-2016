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
    pyglet.resource.path.insert(0, 'asset/map')
    pyglet.resource.reindex()
    layer = load_tmx('level_{}.tmx'.format(mapname))
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
        # For each tile in the map, set scaling behaviour to no interpolation.
        # This means that we don't get blurring on our scaled sprites.
        for tile in level['test_tiles'].values():
            tex = tile.image.get_texture()
            glBindTexture(tex.target, tex.id)
            glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Get map for displaying and use in collision checking
        lvlmap = level['tiles']

        # Set info for use in camera controls
        self.cam_pos = Vector2(0, 0)
        self.cam_vel = Vector2(0, 0)
        self.mgr = mgr
        # Set up scroll manager
        mgr.scale = 1.0
        mgr.add(lvlmap)
        mgr.set_focus(*self.cam_pos)

        # Spawn entities based on locations set in map
        self.player = None  # Holds player entity
        player_layer, enemy_layer = self._create_entity_layers(level, lvlmap)

        # Set input bindings
        self.bindings = {}
        self._bind_events(player_layer)

        # Set update loop
        self.schedule(self.tick)

    # __init__ helper functions
    def _bind_events(self, player_layer):
        """
        Binds all events for which the Scene should listen and delegate, if
        necessary.  Also binds all inputs.
        :param player_layer:  Layer which player is on, for input binding.
        :return: None
        """
        # Extra binding functions
        def update_cam_x(value):
            self.cam_vel.x = value
        def update_cam_y(value):
            self.cam_vel.y = -value

        # Keyboard bindings
        self.bindings['keyboard'] = keybinds = {}
        # Basic binds
        keybinds.update({
            K.UP: player_layer.set_jump,
            K.LEFT: lambda d: player_layer.set_xvel(-1, d),
            K.RIGHT: lambda d: player_layer.set_xvel(1, d),
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
            J.A: player_layer.set_jump,
            J.LSX: player_layer.set_xvel,

            J.RSX: update_cam_x,
            J.RSY: update_cam_y
        })
    def _create_entity_layers(self, level, level_map):
        """
        Create Layers for the player and for enemies and adds them to the
        ScrollingManager.  Populates the layers with all spawns dictated to by
        the level map.
        :param level: The map, read in directly from the .TMX
        :param level_map: The tiles which make up level, retrieved from
            levels['tiles']
        :return: Layers for the player, enemies
        """
        # Add entity layers
        player_layer = PlayerLayer(level_map)
        self.player = player_layer.player
        self.mgr.add(player_layer)
        enemy_layer = EnemyLayer(level_map)
        self.mgr.add(enemy_layer)

        spawns = level['spawns']
        for obj in spawns.objects:
            if obj.usertype == 'spawn.enemy':
                enemy_layer.spawn(obj['entity_type'], (obj.x, obj.y))
            elif obj.usertype == 'spawn.player':
                self.player.center = obj.center
            else:
                print('[WARN]: Cannot spawn', obj.usertype,
                      '(entity_type == {!r})'.format(obj['entity_type']))

        return player_layer, enemy_layer

    # Actual methods
    def tick(self, dt):
        '''Update camera'''
        self.cam_pos += self.cam_vel * dt * 8 * mtr
        player_pos = self.player.center
        self.mgr.force_focus(player_pos[0] + self.cam_pos.x,
                             player_pos[1] + self.cam_pos.y)

    def on_enter(self):
        Scene.on_enter(self)
        InputHandler.on_enter(self)

    def on_exit(self):
        Scene.on_exit(self)
        InputHandler.on_exit(self)
