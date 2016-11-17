from cocos.layer import ScrollableLayer

from ..entity import Player
from ..unit import mtr


_hspeed = 3 * mtr
_vspeed = 4 * mtr

class PlayerLayer(ScrollableLayer):
    '''Layer containing an active player.'''

    def __init__(self, map):
        ScrollableLayer.__init__(self)

        self.player = Player(map, 0, 0)
        self.add(self.player)

    def setxvel(self, val, d=None):
        """
        Utility for setting players X velocity from input

        :param val: -1 for left, 1 for right
        :param d: d is only equal to None when a joystick axis is involved.  Is
            -1 when the key is released.
        :return: None
        """
        vel = val * _hspeed
        if d is None:
            # Joystick handler
            self.player.input_vel.x = vel
        else:
            # Keyboard handler
            self.player.input_vel.x += vel * d
            if d == 1:
                if val == 1:
                    # Running right
                    self.player.change_state('right_run')
                else:
                    # Running left
                    self.player.change_state('left_run')
            else:
                # Key has been released.  Idle now.
                if val == 1:
                    # Was running right
                    self.player.change_state('right_idle')
                else:
                    # Was running left
                    self.player.change_state('left_idle')


    def setjump(self, d):
        '''Utility for setting players Y velocity from jump input'''
        if d > 0 and self.player.grounded:
            self.player.vel.y += _vspeed
