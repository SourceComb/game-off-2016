from cocos.euclid import Vector2
from .component import Entity, Droppable, MapCollidable, Spritable
from ..sprite.creature import PlayerSprite


class Player(Entity, Spritable, MapCollidable, Droppable):
    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, PlayerSprite.idle_right)
        MapCollidable.__init__(self, map, 'slide')
        Droppable.__init__(self)

        self.input_vel = Vector2(0, 0)
        self.facing = 'right'

    def _apply_velocity(self, dt):
        vel = self.vel
        vel.x = self.input_vel.x
        self.vel = vel
        MapCollidable._apply_velocity(self, dt)

    def on_accelerate(self, _, change):
        if change.x:
            if self.vel.x > 0:
                self.facing = 'right'
                self.sprite = PlayerSprite.run_right
            elif self.vel.x < 0:
                self.facing = 'left'
                self.sprite = PlayerSprite.run_left
            else:
                self.sprite = getattr(PlayerSprite, 'idle_' + self.facing)
