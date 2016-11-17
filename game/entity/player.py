from cocos.euclid import Vector2
from .component import Entity, Droppable, MapCollidable, Spritable
from ..sprite.sprites import PlayerSprite


class Player(Entity, Spritable, MapCollidable, Droppable):
    STATES = ('right_idle', 'left_idle', 'right_run', 'left_run')

    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, PlayerSprite.right_idle)
        MapCollidable.__init__(self, map, 'slide')
        Droppable.__init__(self)

        self.input_vel = Vector2(0, 0)

    def _apply_velocity(self, dt):
        self.vel.x = self.input_vel.x
        MapCollidable._apply_velocity(self, dt)

    def map_state_sprites(self):
        self.state_sprite_map = {
            'right_idle': PlayerSprite.right_idle,
            'left_idle': PlayerSprite.left_idle,
            'right_run': PlayerSprite.right_run,
            'left_run': PlayerSprite.left_run,

        }

    def handler_state_change(self, state):
        self.state = state
        self.change_sprite(self.state_sprite_map[state])
