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
    def __init__(self, pos, size, scale=1, frames=1, rate=0):
        self.pos = pos
        self.size = size
        self.scale = scale
        self.frames = frames
        self.rate = rate

    def fill_defaults(self, defaults):
        if hasattr(defaults, 'scale') and defaults.scale is not None:
            self.scale *= defaults.scale
        if hasattr(defaults, 'rate') and defaults.rate is not None \
                and self.rate == 0:
            self.rate = defaults.rate

    def toimg(self, canvas, i):
        return canvas.get_region(
            self.pos[0] + self.size[0]*i, self.pos[1],
            # Fix an off-by-one issue
            self.size[0] - 1, self.size[1] - 1
        )

    def toanim(self, canvas):
        dur = 1.0/self.rate
        frames = [pyglet.image.AnimationFrame(self.toimg(canvas, i), dur)
                  for i in range(self.frames)]
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
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        info = _SheetInfo()
        for base in bases:
            if hasattr(base, 'info'):
                info.canvas = base.info.canvas
                info.defaults.update(base.info.defaults)
        return { 'info': info }

    def __init__(cls, name, bases, attrs, **kwargs):
        cls.info.canvas = _get_canvas(cls.info.canvas)
        for attr in attrs:
            value = getattr(cls, attr)
            if isinstance(value, Sprite):
                value.fill_defaults(cls.info.defaults)
                value.gensprite(cls.info.canvas)
        return super().__init__(name, bases, attrs, **kwargs)


class Spritesheet(metaclass=SpritesheetMeta):
    pass


if __name__ == '__main__':
    # By Riley
    print('Testing')
    print(hasattr(_SheetInfo, '__dict__'))
    a = _SheetDefaults()
    print(hasattr(a, '__dict__'))
    print(_SheetInfo.__bases__)
