import pyglet.image


class SpritesheetBase:
    @classmethod
    def _parse(cls, src):
        lines = src.split('\n')
        # Ensure we have a valid source
        header = lines.pop(0)
        if not header.startswith('spritesheet;'):
            raise ValueError('Invalid spritesheet header: {!r}'
                    .format(header))
        # Get the cell width
        header = header.split(';')[1:]
        c = int(header[0])

        # Parse key/value section
        sprites = []
        for line in lines:
            if line:
                # Separate key and value
                key, value = line.split('=')
                key = key.strip()
                # Parse value section into parts
                pos, size, anim = value.strip().split(' ')
                y, x = map(int, pos.split(','))
                w, h = map(int, size.split('x'))
                nframes, rate = anim.split('@')
                nframes = int(nframes)
                rate = float(rate)
                # Generate frame info
                fdur = 1 / rate
                value = [(
                            ((x+i) * c, y * c,
                                # w/h -1 to avoid edges
                                w*c - 1, h*c - 1),
                            fdur
                        ) for i in range(nframes)]
                # Add this frameset to list of sprites
                sprites.append((key, value))
        return sprites

    def __init__(self, sprites, canvas):
        # Ensure any sprite sources are parsed
        if isinstance(sprites, str):
            sprites = SpritesheetBase._parse(sprites)
        # Convert list of sprites to dict
        if isinstance(sprites, list):
            sd = {}
            for sname, sinfo in sprites:
                skeys = sname.split('.')
                elem = sd
                for key in skeys[:-1]:
                    if key not in elem:
                        elem[key] = {}
                    elem = elem[key]
                elem[skeys[-1]] = sinfo
            sprites = sd
        # Set properties
        self.sprites = sprites
        self.canvas = canvas

    def __getitem__(self, key):
        # Get key from nested dict
        elem = self.sprites
        for k in key.split('.'):
            elem = elem[k]
        # Convert info to an Animation and return
        return pyglet.image.Animation(
            [pyglet.image.AnimationFrame(
                self.canvas.get_region(*frame[0]), frame[1]
            ) for frame in elem]
        )


class Spritesheet(SpritesheetBase):
    @classmethod
    def open(cls, name, canvas=None):
        if name.endswith('.spr'):
            # Using explicit file names
            srcf = name
            if canvas is None:
                canvas = name[:-4] + '.png'
        else:
            # Using template file names
            srcf = name + '.spr'
            canvas = name + '.png'
        # Read data from files
        with pyglet.resource.file(srcf) as srcf:
            src = srcf.read().decode('utf-8')
        canvas = pyglet.resource.image(canvas)
        # Return a Spritesheet instance
        return Spritesheet(src, canvas)

    def __init__(self, sprites, canvas):
        super().__init__(sprites, canvas)

    def __getattr__(self, key):
        # Check the cache
        if key in self._cache:
            return self._cache[key]
        # Nothing in cache
        if isinstance(self.sprites[key], dict):
            # Not a final key; create nested spritesheet
            val = Spritesheet(self.sprites[key], self.canvas)
        else:
            # This must be a final key
            val = self[key]
        # Set this value in cache
        self._cache[key] = val
        return val
