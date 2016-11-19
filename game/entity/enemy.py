from cocos.euclid import Vector2
from .component import (Entity, Droppable, Killable, MapCollidable, Spritable,
                        State, Stateable)
from ..sprite.creature import ZombieSpriteSheet
from ..unit import mtr


class Zombie(Entity, Spritable, MapCollidable, Droppable, Stateable):
    SPEED = 1 * mtr
    def __init__(self, map, x, y):
        Entity.__init__(self, (x, y))
        Spritable.__init__(self, ZombieSpriteSheet.idle_right)
        Killable.__init__(self, 40)
        MapCollidable.__init__(self, map, 'slide')
        Droppable.__init__(self)
        Stateable.__init__(self)

        self.running = False
        self.facing = 'right'
        self.was_grounded = False

        def tick(dt, self):
            self.state_update(dt)
            if self.cur_state.name.startswith('idle'):
                # Idle at the moment, continue patrolling
                if self.facing == 'right':
                    self.push_state(State('run_left', active_duration=4))
                    self.hvel = -Zombie.SPEED
                    self.facing = 'left'
                    self.change_sprite()
                else:
                    self.push_state(State('run_right', active_duration=4))
                    self.hvel = Zombie.SPEED
                    self.facing = 'right'
                    self.change_sprite()

        self.schedule(tick, self)

    @property
    def hvel(self):
        return None

    @hvel.setter
    def hvel(self, val):
        # Need to start running
        self.running = True
        self.vel = Vector2(val, 0.0)


    def _apply_velocity(self, dt):
        MapCollidable._apply_velocity(self, dt)

    def change_sprite(self):
        self.sprite.remove_handlers(on_animation_end=self.on_animation_end)

        type = 'run_' if self.vel.x else 'idle_'
        self.sprite = getattr(ZombieSpriteSheet, type + self.facing)
        self.sprite.push_handlers(on_animation_end=self.on_animation_end)

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
            self.change_sprite()

    def on_map_disconnect(self, _, direction):
        if direction == 'down' and self.was_grounded:
            self.was_grounded = False
            self.change_sprite()

    def on_accelerate(self, _, change):
        if change.x:
            if self.vel.x < 0:
                self.facing = 'left'
            elif self.vel.x > 0:
                self.facing = 'right'
            self.change_sprite()

    def on_animation_end(self):
        pass