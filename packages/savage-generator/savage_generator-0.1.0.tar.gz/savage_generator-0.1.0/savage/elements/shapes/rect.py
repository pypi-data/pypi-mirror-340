from .shape import Shape

class Rect(Shape):
    def __init__(self, width, height, x, y, rx=None, ry=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = "rect"
        self.attributes['width'] = width
        self.attributes['height'] = height
        self.attributes['x'] = x
        self.attributes['y'] = y
        if rx:
            self.attributes['rx'] = rx
        if ry:
            self.attributes['ry'] = ry