from cocos.euclid import Vector2
from .component import Entity, Droppable, Killable, MapCollidable, Spritable
from ..sprite.creature import PlayerSprite
from ..unit import mtr


class Player(Entity, Spritable, Killable, MapCollidable, Droppable):
    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, PlayerSprite.idle_right)
        Killable.__init__(self, 40)
        MapCollidable.__init__(self, map, 'slide')
        Droppable.__init__(self)

        self.running = False
        self.facing = 'right'
        self.was_grounded = False

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

    def select_sprite(self):
        if self.grounded:
            type = 'run_' if self.vel.x else 'idle_'
        else:
            type = 'jump_'
        self.sprite = getattr(PlayerSprite, type + self.facing)

    def on_map_connect(self, _, direction, obj):
        # Stop moving if not running
        if direction == 'down' and not self.running:
            def stop(dt):
                if not self.running:
                    self.vel = Vector2(0.0, self.vel.y)
                self.unschedule(stop)
            self.schedule(stop)

        # Fix sprite if landing
        if direction == 'down' and not self.was_grounded:
            self.was_grounded = True
            self.select_sprite()

        # Check for spikes
        dmg = obj.get('damage')
        if dmg:
            # Apply damage
            self.health -= dmg
            # Calculate knockback
            knockback = dmg * mtr
            if direction == 'right':
                knockback = -knockback
            knockback = Vector2(
                knockback if direction in ('left', 'right') else 0.0,
                abs(knockback)
            )
            # Apply knockback on next tick
            def apply_knockback(dt):
                self.hvel = 0
                self.vel = knockback
                self.unschedule(apply_knockback)
            self.schedule(apply_knockback)

    def on_damage(self, _, dmg):
        print('took', dmg, 'damge (', self.health, ')')

    def on_map_disconnect(self, _, direction):
        if direction == 'down' and self.was_grounded:
            self.was_grounded = False
            self.select_sprite()

    def on_accelerate(self, _, change):
        if change.x:
            if self.vel.x < 0:
                self.facing = 'left'
            elif self.vel.x > 0:
                self.facing = 'right'
            self.select_sprite()
