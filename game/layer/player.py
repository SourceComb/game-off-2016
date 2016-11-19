from cocos.euclid import Vector2
from cocos.layer import ScrollableLayer

from ..entity import Player
from ..unit import mtr


_hspeed = 4 * mtr
_vspeed = 10 * mtr


class PlayerLayer(ScrollableLayer):
    '''Layer containing an active player.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)

        self.player = Player(map, 0, 0)
        self.add(self.player)

    def set_xvel(self, dir, is_key_press=None):
        """
        Utility for setting players X velocity from input
        :param dir: (int)  Direction multiplier.  1 for right, -1 for left.
        :param is_key_press: Holds if called by key press.  False if called by
            key release.  None only if joystick input.
        :return:  None.
        """
        if is_key_press is None:
            # Joystick control, normalise controller input
            is_key_press = 1 if round(dir) else -1
            dir = 1 if dir > 0 else -1

        if is_key_press < 0:
            # Releasing a key; set velocity to 0
            if (dir < 0) != (self.player.vel.x < 0):
                # Don't do anything if the direction is not the same
                return
            dir = 0
        # Set velocity
        self.player.hvel = dir * _hspeed

    def set_jump(self, is_key_press):
        '''Utility for setting players Y velocity from jump input'''
        if is_key_press > 0 and self.player.grounded:
            # Jump button pressed, and the player can actually jump so set
            # upwards velocity to jump velocity
            self.player.vel += Vector2(0.0, _vspeed)
