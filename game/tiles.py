from cocos.layer.scrolling import ScrollableLayer
from cocos.sprite import Sprite
from cocos.tiles import *
import pyglet.image
import pyglet.resource
from xml.etree import ElementTree


class TmxImageLayer(ScrollableLayer):
    def __init__(self, image, offset, maph):
        super(TmxImageLayer, self).__init__()
        self.image = image
        self._sprite = Sprite(
            image,
            (offset[0] + (image.width / 2),
             (maph - offset[1]) - (image.height / 2))
        )
        self.add(self._sprite)


def load_map(mapname):
    '''Hack to ensure maps with relative image paths get loaded correctly,
    by manipulating pyglet.resource.path.'''
    pyglet.resource.path.insert(0, 'asset/map')
    pyglet.resource.reindex()
    layer = load_tmx('level_{}.tmx'.format(mapname))
    pyglet.resource.path.pop(0)
    pyglet.resource.reindex()
    return layer


def load_tmx(filename):
    """Load some tile mapping resources from a TMX file.

    Modified from cocos.tiles.load_tmx
    """
    resource = Resource(filename)

    tree = ElementTree.parse(resource.path)
    map = tree.getroot()
    if map.tag != 'map':
        raise ResourceError('document is <%s> instead of <map>' % map.name)

    width = int(map.attrib['width'])
    height = int(map.attrib['height'])

    # XXX this is ASSUMED to be consistent
    tile_width = int(map.attrib['tilewidth'])
    tile_height = int(map.attrib['tileheight'])

    tiling_style = map.attrib['orientation']

    if tiling_style == "hexagonal":
        hex_sidelenght = int(map.attrib["hexsidelength"])
        # 'x' meant hexagons with top and bottom sides parallel to x axis,
        # 'y' meant hexagons with left and right sides paralel to y axis
        s = map.attrib["staggeraxis"]
        hex_orientation = {'x': 'pointy_left', 'y': 'pointy_up'}
        # 'even' or 'odd', currently cocos only displays correctly 'even'
        lowest_columns = map.attrib["staggerindex"] == "even"
        cell_cls = HexCell
        layer_cls = HexMapLayer
        map_height_pixels = height * tile_height + tile_height // 2

    elif tiling_style == "orthogonal":
        cell_cls = RectCell
        layer_cls = RectMapLayer
        map_height_pixels = height * tile_height

    else:
        raise ValueError("Unsuported tiling style, must be 'orthogonal' or 'hexagonal'")

    # load all the tilesets
    tilesets = []
    for tag in map.findall('tileset'):
        if 'source' in tag.attrib:
            firstgid = int(tag.attrib['firstgid'])
            path = resource.find_file(tag.attrib['source'])
            with open(path) as f:
                tag = ElementTree.fromstring(f.read())
        else:
            firstgid = int(tag.attrib['firstgid'])

        name = tag.attrib['name']

        spacing = int(tag.attrib.get('spacing', 0))
        for c in tag.getchildren():
            if c.tag == "image":
                # create a tileset from the image atlas
                path = resource.find_file(c.attrib['source'])
                tileset = TileSet.from_atlas(name, firstgid, path, tile_width,
                                             tile_height, row_padding=spacing,
                                             column_padding=spacing)
                # TODO consider adding the individual tiles to the resource?
                tilesets.append(tileset)
                resource.add_resource(name, tileset)
            elif c.tag == 'tile':
                # add properties to tiles in the tileset
                gid = tileset.firstgid + int(c.attrib['id'])
                tile = tileset[gid]
                props = c.find('properties')
                if props is None:
                    continue
                for p in props.findall('property'):
                    # store additional properties.
                    name = p.attrib['name']
                    value = p.attrib['value']
                    # TODO consider more type conversions?
                    if value.isdigit():
                        value = int(value)
                    tile.properties[name] = value

    # now load all the layers
    for layer in map.findall('layer'):
        data = layer.find('data')
        if data is None:
            raise ValueError('layer %s does not contain <data>' % layer.name)

        encoding = data.attrib.get('encoding')
        compression = data.attrib.get('compression')
        if encoding is None:
            # tiles data as xml
            data = [int(tile.attrib.get('gid')) for tile in data.findall('tile')]
        else:
            data = data.text.strip()
            if encoding == 'csv':
                data.replace('\n', '')
                data = [int(s) for s in data.split(',')]
            elif encoding == 'base64':
                data = decode_base64(data)
                if compression == 'zlib':
                    data = decompress_zlib(data)
                elif compression == 'gzip':
                    data = decompress_gzip(data)
                elif compression is None:
                    pass
                else:
                    raise ResourceError('Unknown compression method: %r' % compression)
                data = struct.unpack(str('<%di' % (len(data) // 4)), data)
            else:
                raise TmxUnsupportedVariant("Unsupported tiles layer format " +
                                            "use 'csv', 'xml' or one of " +
                                            "the 'base64'")

        assert len(data) == width * height

        cells = [[None] * height for x in range(width)]
        for n, gid in enumerate(data):
            if gid < 1:
                tile = None
            else:
                # UGH
                for ts in tilesets:
                    if gid in ts:
                        tile = ts[gid]
                        break
            i = n % width
            j = height - (n // width + 1)
            cells[i][j] = cell_cls(i, j, tile_width, tile_height, {}, tile)

        id = layer.attrib['name']

        m = layer_cls(id, tile_width, tile_height, cells, None, {})
        m.visible = int(layer.attrib.get('visible', 1))

        resource.add_resource(id, m)

    # Load object groups
    for tag in map.findall('objectgroup'):
        layer = TmxObjectLayer.fromxml(tag, tilesets, map_height_pixels)
        resource.add_resource(layer.name, layer)

    # Load image layers
    for tag in map.findall('imagelayer'):
        imgtag = tag.getchildren()[0]
        path = resource.find_file(imgtag.attrib['source'])
        image = pyglet.image.load(path)
        layer = TmxImageLayer(
            image, (int(tag.attrib['offsetx']), int(tag.attrib['offsety'])),
            height * tile_height
        )
        resource.add_resource(tag.attrib['name'], layer)

    return resource
