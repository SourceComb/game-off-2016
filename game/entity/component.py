'''Module containing the Entity type, and mixins useful for defining
entity behaviour using the Component model.'''

from cocos.cocosnode import CocosNode
from cocos.draw import Canvas
from cocos.euclid import Vector2
from cocos.mapcolliders import RectMapWithPropsCollider
from cocos.rect import Rect
from pyglet.event import EventDispatcher

from ..sprite import sheet
from ..unit import mtr


def getvec2(x, y=None):
    if isinstance(x, int):
        x = float(x)
    if isinstance(y, int):
        y = float(y)
    if isinstance(x, float):
        assert isinstance(y, float)
        x = x, y

    if isinstance(x, tuple):
        x = Vector2(x[0], x[1])

    if isinstance(x, Vector2):
        return x
    else:
        raise ValueError('Could not convert ({!r}, {!r}) to Vector2'.format(
            x, y
        ))


def _sendonmove(e):
    e.dispatch_event('on_move', e, e.rect.position)


class EntityMeta(type):
    '''Metaclass for entities.

    Allows components to use an `EVENTS` property to declare the events they may
    emit.'''
    def __init__(cls, name, bases, attrs, **kwargs):
        if 'EVENTS' in attrs:
            for event in cls.EVENTS:
                cls.register_event_type(event)

        for base in bases:
            events = base.EVENTS if hasattr(base, 'EVENTS') \
                    else base._EVENTS if hasattr(base, '_EVENTS') \
                    else tuple()
            for event in events:
                cls.register_event_type(event)

        super().__init__(name, bases, attrs)


class Entity(CocosNode, EventDispatcher, metaclass=EntityMeta):
    '''Entity super-type.

    All entities have a position and size (under the `rect` property), and a
    velocity. When active, the position is automatically updated based on
    velocity. They emit the `on_move` event when their position changes.'''

    EVENTS = 'on_move', 'on_accelerate'

    def __init__(self, pos, size=(0, 0)):
        CocosNode.__init__(self)

        self._rect = Rect(*pos, *size)
        self._vel = Vector2(0.0, 0.0)

        self.push_handlers(self)

    def on_enter(self):
        self.schedule(self.tick)
        super().on_enter()

    def on_exit(self):
        self.unschedule(self.tick)
        super().on_exit()

    def tick(self, dt):
        '''Perform necessary update operations.'''
        self._apply_velocity(dt)

    def _apply_velocity(self, dt):
        '''Naïve velocity calculation implementation. Does not account for any
        collisions; use *Collidable components to make these considerations.'''
        self.pos += self._vel * dt

    @property
    def rect(self):
        return self._rect.copy()

    @rect.setter
    def rect(self, newrect):
        self._rect = newrect.copy()
        _sendonmove(self)

    @property
    def pos(self):
        return Vector2(*self._rect.position)

    @pos.setter
    def pos(self, value):
        self._rect.position = value
        _sendonmove(self)

    @property
    def center(self):
        return Vector2(*self._rect.center)

    @center.setter
    def center(self, value):
        self._rect.center = value
        _sendonmove(self)

    @property
    def size(self):
        return Vector2(*self._rect.size)

    @size.setter
    def size(self, value):
        self._rect.size = value

    @property
    def vel(self):
        return self._vel.copy()

    @vel.setter
    def vel(self, value):
        oldvel = self.vel
        newvel = getvec2(value)
        self._vel = newvel
        # Emit event
        if oldvel != newvel:
            self.dispatch_event('on_accelerate', self, newvel - oldvel)


class Spritable:
    '''The Spritable component indicates that an entity has a sprite.

    This sprite is passed to the constructor. It is automatically added as a
    child node. Its position is kept in sync with the entity's.'''

    def __init__(self, sprite):
        self._Spritable_sprite = None
        self.sprite = sprite
        # Update sprite position when the entity moves
        def setpos(_, pos):
            self._Spritable_sprite.position = self.center
        self.push_handlers(on_move=setpos)

    @property
    def sprite(self):
        return self._Spritable_sprite

    @sprite.setter
    def sprite(self, new):
        if isinstance(new, sheet.Sprite):
            new = new(self.pos)
        else:
            new.position = self.center
        # Ensure rect size matches sprite
        self.size = new.width, new.height
        # Set sprite on self
        old = self._Spritable_sprite
        self._Spritable_sprite = new
        # Set sprite as child node
        if old is not None:
            self.remove(old)
        self.add(new)


class Killable:
    '''The Killable component indicates that an entity has health.

    The starting health is passed as an argument to the constructor. The
    `health` property allows manipulating this entity's health. Events are
    emitted when the health changes, and when the health decreases to zero
    ("death"). The `dead` property returns true when this is the case.'''

    EVENTS = 'on_heal', 'on_damage', 'on_death'

    def __init__(self, start_health, enable_events=True):
        self._Killable_health = start_health
        self._Killable_enable_events = enable_events

    @property
    def health(self):
        return self._Killable_health

    @health.setter
    def health(self, value):
        oldvalue = self._Killable_health
        self._Killable_health = value

        if self._Killable_enable_events:
            if value < oldvalue:    # Taking damage
                self.dispatch_event('on_damage', self, oldvalue - value)
            elif value > oldvalue:  # Restoring health
                self.dispatch_event('on_heal', self, value - oldvalue)

            if self.dead:
                self.dispatch_event('on_death', self)

    @property
    def dead(self):
        return self._Killable_health <= 0


class MapCollidable:
    '''The MapCollidable component indicates that an entity can collide with
    the map.

    It stores the map collider and the map to collide with, and accounts for the
    map by overriding the per-tick movement code. The `grounded` property is
    made available for checking whether or not this entity is touching the
    ground.'''

    EVENTS = ('on_map_connect',)

    def __init__(self, map, collide_strategy):
        self._MapCollidable_collider = \
            _CustomMapCollider(self, collide_strategy)
        self._MapCollidable_map = map
        self._MapCollidable_connected = {
            'up': False, 'down': False,
            'left': False, 'right': False
        }

        def on_connect(self, direction, obj):
            self._MapCollidable_connected[direction] = True
        self.push_handlers(on_map_connect=on_connect)

    @property
    def grounded(self):
        return self._MapCollidable_connected['down']

    def _apply_velocity(self, dt):
        '''Account for map when applying velocity'''
        old = self.rect
        vel = self.vel
        # Calculate main changes
        disp = vel * dt
        new = old.copy()
        new.x += disp.x
        new.y += disp.y
        # Account for collisions
        # Modifies `new` and returns an updated velocity
        # that takes collisions into account
        newvel = self._MapCollidable_collider.collide_map(
            self._MapCollidable_map,
            old, new, vel.x, vel.y
        )
        self.vel = newvel
        # Update self with new position
        self.rect = new

        # Unset any connections that no longer apply
        connected = self._MapCollidable_connected
        if connected['up'] and self.vel.y:
            # Moved down so no longer connected
            connected['up'] = False
        if connected['down'] and self.vel.y:
            # Moved up so no longer connected
            connected['down'] = False
        if connected['left'] and self.vel.x:
            # Moved right so no longer connected
            connected['left'] = False
        if connected['right'] and self.vel.x:
            # Moved left so no longer connected
            connected['right'] = False


class _CustomMapCollider(RectMapWithPropsCollider):
    '''Custom MapCollider to dispatch events to a MapCollidable entity.'''

    def __init__(self, entity, *args):
        super().__init__(*args)
        self.entity = entity

    def collide_bottom(self, obj):
        '''Bottom of entity collided with top of obj'''
        self.entity.dispatch_event('on_map_connect', self.entity, 'down', obj)

    def collide_left(self, obj):
        '''Left of entity collided with right of obj'''
        self.entity.dispatch_event('on_map_connect', self.entity, 'left', obj)

    def collide_right(self, obj):
        '''Right of entity collided with left of obj'''
        self.entity.dispatch_event('on_map_connect', self.entity, 'right', obj)

    def collide_top(self, obj):
        '''Top of entity collided with bottom of obj'''
        self.entity.dispatch_event('on_map_connect', self.entity, 'up', obj)


# Accel due to grav, in px/s/s
_a_g = Vector2(0.0, -9.8) * mtr
class Droppable:
    '''The Droppable component indicates that an entity should be affected by
    gravity.

    If `self.grounded` exists, it will be checked and gravity disabled when it
    is true. This allows seamless cooperation with MapCollidable.'''
    def __init__(self):
        self.schedule(self._Droppable_apply_gravity)

    def _Droppable_apply_gravity(self, dt):
        self.vel += _a_g * dt
