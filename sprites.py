import io
import pyglet.image
import pyglet.resource


class FrameData:
    @classmethod
    def parse(cls, src, c):
        pos, size, anim = src.split(' ')
        posy, posx = tuple(map(int, pos.split(',')))
        w, h = tuple(map(int, size.split('x')))
        nf, rate = tuple(map(int, anim.split('@')))

        framelen = 1.0 / rate
        return [FrameData(
                ((posx+i) * c, posy * c,
                    w*c - 1, h*c - 1),
                framelen
            ) for i in range(nf)]

    def __init__(self, bounds, length):
        self.bounds = bounds
        self.length = length


class Layout:
    def __init__(self, toparse, *, _cellsize=None, _sprites=None):
        if toparse is None:
            self._cellsize = _cellsize
            self.sprites = _sprites
        elif isinstance(toparse, str):
            self._parse_str(toparse)
        elif isinstance(toparse, io.IOBase):
            self._parse_str(toparse.read().decode('utf-8'))
        else:
            raise TypeError('invalid layout type: ' + repr(toparse))

    def _parse_str(self, src):
        lines = src.split('\n')
        header = lines.pop(0)
        if not header.startswith('spritesheet;'):
            raise ValueError('invalid layout header: {!r}'.format(header))
        header = header.split(';')[1:]
        self._cellsize = int(header[0])

        sprites = {}
        for line in lines:
            if not line:
                continue
            key, value = line.split('=')
            key = key.strip()
            value = value.strip()

            ks = key.split('.')
            elem = sprites
            for k in ks[:-1]:
                if k.isnumeric():
                    k = int(k)
                if k not in elem:
                    elem[k] = {}
                elem = elem[k]

            elem[ks[-1]] = FrameData.parse(value, self._cellsize)
        self.sprites = sprites

    def __getitem__(self, key):
        ks = key.split('.', 1)
        info = self.sprites[ks[0]]
        if isinstance(info, dict):
            info = Layout(
                    None, _cellsize=self._cellsize, _sprites=info
            )
            self.sprites[ks[0]] = info
        if isinstance(info, Layout) and len(ks) > 1:
            return info[ks[1]]
        else:
            return info


class SpriteSheet:
    def __init__(self, layout, canvas):
        if not isinstance(layout, Layout):
            layout = Layout(layout)
        self.layout = layout
        self.canvas = canvas
        self._cache = {}

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        if key in self._cache:
            return self._cache[key]

        info = self.layout[key]
        if isinstance(info, Layout):
            val = SpriteSheet(info, self.canvas)
        else:
            frames = [
                    pyglet.image.AnimationFrame(
                        self.canvas.get_region(*framedata.bounds),
                        framedata.length
                    ) for framedata in info
            ]
            val = pyglet.image.Animation(frames)

        self._cache[key] = val
        return val


def load(name, canvas=None):
    if canvas is not None:
        src = name
    else:
        src = pyglet.resource.file(name + '.spr')
        canvas = pyglet.resource.image(name + '.png')
    return SpriteSheet(src, canvas)
