from .shape import Shape

class Ellipse(Shape):
    def __init__(self, cx, cy, rx, ry, **kwargs):
        super().__init__(**kwargs)
        self.tag = "ellipse"
        self.attributes['cx'] = cx
        self.attributes['cy'] = cy
        self.attributes['rx'] = rx
        self.attributes['ry'] = ry