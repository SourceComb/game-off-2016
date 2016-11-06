import argparse
from cocos.director import director


parser = argparse.ArgumentParser()
parser.add_argument('--sprite', nargs=1)
parser.add_argument('--bg', nargs=1)
args = parser.parse_args()

director.init()
scene = None

if args.sprite is not None:
    # To run this test:
    # $ python . --sprite game.sprite.test.StickSprite.run --bg 255,255,255,255
    from importlib import import_module
    from game.scene.tests import SpriteTestScene

    module, sheet, sprite = args.sprite[0].rsplit('.', 2)
    module = import_module(module)
    sheet = getattr(module, sheet)
    sprite = getattr(sheet, sprite)
    bg = args.bg[0].split(',') if args.bg else None

    scene = SpriteTestScene(sprite, bg)

else:
    from game.scene import first_scene
    scene = first_scene()

director.run(scene)
