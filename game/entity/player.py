from cocos.euclid import Vector2
from .component import Entity, Droppable, MapCollidable, Spritable
from ..sprite.creature import PlayerSprite


class Player(Entity, Spritable, MapCollidable, Droppable):
    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, PlayerSprite.idle_right)
        MapCollidable.__init__(self, map, 'slide')
        Droppable.__init__(self)

        self.running = False
        self.facing = 'right'

    @property
    def hvel(self):
        return None

    @hvel.setter
    def hvel(self, val):
        if val and not self.running:
            # Need to start running
            self.running = True
            self.vel += Vector2(val, 0.0)
        elif val == 0 and self.running:
            # Need to stop running
            self.running = False
            self.vel -= Vector2(self.vel.x, 0.0)

    def _apply_velocity(self, dt):
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
