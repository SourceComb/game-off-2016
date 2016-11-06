from cocos.layer import ColorLayer, Layer
from cocos.scene import Scene


class SpriteTestScene(Scene):
    def __init__(self, sprite, color):
        layer = None
        if color is None:
            layer = Layer()
        else:
            layer = ColorLayer(*map(int, color))

        self.sprite = sprite((100, 100))
        layer.add(self.sprite)

        super().__init__(layer)
