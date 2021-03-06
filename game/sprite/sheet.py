import cocos.sprite
import pyglet.image
from pyglet.gl import GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    glBindTexture, glTexParameteri
import pyglet.resource


def _get_canvas(arg):
    if arg is None: return arg
    canvas = arg
    if isinstance(canvas, str):
        canvas = pyglet.resource.image(canvas)
    if isinstance(canvas, pyglet.image.AbstractImage):
        # Set nearest scaling, so that up-scaled sprites look nice.
        tex = canvas.get_texture()
        glBindTexture(tex.target, tex.id)
        glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return canvas
    else:
        raise ValueError('Could not create canvas from ' + repr(arg))


class _SheetInfo:
    __slots__ = 'canvas', 'defaults'

    def __init__(self):
        self.canvas = None
        self.defaults = _SheetDefaults()


class _SheetDefaults:
    __slots__ = 'scale', 'rate'
    def update(self, other):
        if hasattr(other, 'scale'):
            self.scale = other.scale
        if hasattr(other, 'rate'):
            self.rate = other.rate


class Sprite:
    def __init__(self, pos, size, scale=1, frames=1, rate=0, repeat=True):
        self.pos = pos
        self.size = size
        self.scale = scale
        self.frames = frames
        self.rate = rate
        self.repeat = repeat

    def fill_defaults(self, defaults):
        if hasattr(defaults, 'scale') and defaults.scale is not None:
            self.scale *= defaults.scale
        if hasattr(defaults, 'rate') and defaults.rate is not None \
                and self.rate == 0:
            self.rate = defaults.rate

    def toimg(self, canvas, i):
        return canvas.get_region(
            self.pos[0] + self.size[0]*i, self.pos[1],
            self.size[0], self.size[1]
        )

    def toanim(self, canvas):
        dur = 1.0/self.rate
        frames = [pyglet.image.AnimationFrame(self.toimg(canvas, i), dur)
                  for i in range(self.frames)]
        if not self.repeat:
            frames[-1].duration = None
        return pyglet.image.Animation(frames)

    def gensprite(self, canvas):
        if self.frames == 1:
            self._spr = self.toimg(canvas, 0)
        else:
            self._spr = self.toanim(canvas)

    def __call__(self, *args, **kwargs):
        # Set correct scale argument
        scale = 1
        if len(args) >= 3:
            scale = args[2]
        elif 'scale' in kwargs:
            scale = kwargs['scale']
        # Use any passed scale as a multiplier
        scale *= self.scale
        if len(args) >= 3:
            args[2] = scale
        else:
            kwargs['scale'] = scale

        return cocos.sprite.Sprite(self._spr, *args, **kwargs)


class SpritesheetMeta(type):
    '''Metaclass for all spritesheets. You'll probably want to use `Spritesheet`
    as an intermediate superclass, rather that directly setting
    `metaclass=SpritesheetMeta`.

    This allows subclassing effectively, so that subclasses don't clobber the
    parents `info` when they change theirs. It also allows calculating image
    information up-front, when the class is created.'''
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        # Create new info object to prevent clobbering parents.
        info = _SheetInfo()
        # Extend info from bases
        for base in bases:
            if hasattr(base, 'info'):
                info.canvas = base.info.canvas
                info.defaults.update(base.info.defaults)
        return { 'info': info }

    def __init__(cls, name, bases, attrs, **kwargs):
        # Calculate images for each sprite up-front.
        cls.info.canvas = _get_canvas(cls.info.canvas)
        for attr in attrs:
            value = getattr(cls, attr)
            if isinstance(value, Sprite):
                value.fill_defaults(cls.info.defaults)
                value.gensprite(cls.info.canvas)
        return super().__init__(name, bases, attrs, **kwargs)


class Spritesheet(metaclass=SpritesheetMeta):
    '''Super-class for spritesheet definitions. Sets the metaclass to
    `SpritesheetMeta`.'''
    pass
