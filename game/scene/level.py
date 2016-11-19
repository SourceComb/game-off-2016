from cocos.euclid import Vector2
from cocos.layer.scrolling import ScrollingManager
from cocos.scene import Scene
from cocos.tiles import TileSet, load_tmx
from pyglet.gl import GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    glBindTexture, glTexParameteri
import pyglet.resource

from ..input import InputHandler, J, K, M
from ..layer.player import PlayerLayer
from ..layer.enemy import EnemyLayer
from ..tiles import load_map
from ..unit import mtr


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
        for name, tileset in level.find(TileSet):
            for tile in tileset.values():
                tex = tile.image.get_texture()
                glBindTexture(tex.target, tex.id)
                glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Set info for use in camera controls
        self.cam_pos = Vector2(0, 0)
        self.cam_vel = Vector2(0, 0)

        # Get map for displaying and use in collision checking
        lvlmap = level['tiles']

        # Create and populate entity layers with spawns
        self.player = None  # Will hold player entity for camera to center on
        player_layer, enemy_layer = self._create_entity_layers(level, lvlmap)

        # Set up scroll manager
        self.mgr = mgr
        # Add layers to scrolling manager
        if 'backdrop' in level:
            mgr.add(level['backdrop'])
        mgr.add(lvlmap)
        mgr.add(enemy_layer)
        mgr.add(player_layer)   # Player should probably always be on top

        # Set input bindings
        self.bindings = {}
        self._bind_events(player_layer)

        # Set update loop
        self.schedule(self.tick)

    # __init__ helper functions
    def _create_entity_layers(self, level, level_map):
        player_layer = PlayerLayer(level_map)
        enemy_layer = EnemyLayer(level_map)

        # Store reference to player entity
        self.player = player_layer.player

        # Spawn entities based on locations set in map
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

        # Mouse bindings
        self.bindings['mouse'] = {}
        self.bindings['mouse'].update({
            M.LEFT: player_layer.attack
        })

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
