from cocos.cocosnode import CocosNode
from cocos.euclid import Vector2
from pyglet.event import EventDispatcher

from ..sprite import sheet


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


class EntityMeta(type):
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
    EVENTS = ('on_move',)

    def __init__(self, pos):
        CocosNode.__init__(self)

        self._pos = Vector2(pos[0], pos[1])
        self._vel = Vector2(0.0, 0.0)

    def on_enter(self):
        self.schedule(self.tick)
        super().on_enter()

    def on_exit(self):
        self.unschedule(self.tick)
        super().on_exit()

    def tick(self, dt):
        self.move(self._vel * dt)

    def move(self, relx, rely=None):
        self.pos += getvec2(relx, rely)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, newpos):
        self._pos = newpos
        self.dispatch_event('on_move', self, newpos)

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel = getvec2(value)


class Spritable:
    def __init__(self, sprite):
        if isinstance(sprite, sheet.Sprite):
            sprite = sprite(self.pos)
        else:
            sprite.position = self.pos

        self._Spritable_sprite = sprite
        self.add(sprite)

        self.push_handlers(on_move=self._Spritable_setpos)

    def _Spritable_setpos(self, _, pos):
        self._Spritable_sprite.position = pos


class Killable:
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

            if self.dead():
                self.dispatch_event('on_death', self)

    @property
    def dead(self):
        return self._Killable_health <= 0
