from .shape import Shape

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(**kwargs)
        self.tag = "line"
        self.attributes['x1'] = x1
        self.attributes['y1'] = y1
        self.attributes['x2'] = x2
        self.attributes['y2'] = y2