import pyglet.input


class XInputHandler:
    def __init__(self, *joysticks):
        if len(joysticks) == 0:
            joysticks = list(pyglet.input.get_joysticks())
        self.joysticks = joysticks

    def on_enter(self):
        for joy in self.joysticks:
            joy.open()
            joy.push_handlers(self)

    def on_exit(self):
        for joy in self.joysticks:
            joy.remove_handlers(self)
