from cocos.scene import Scene

from ..layer.player import PlayerLayer


class LevelScene(Scene):
    def __init__(self):
        Scene.__init__(self, PlayerLayer())
