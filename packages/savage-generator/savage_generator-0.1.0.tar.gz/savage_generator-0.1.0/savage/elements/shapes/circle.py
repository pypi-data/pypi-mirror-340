from .shape import Shape

class Circle(Shape):
    def __init__(self, cx, cy, r, **kwargs):
        super().__init__(**kwargs)
        self.tag = "circle"
        self.attributes['cx'] = cx
        self.attributes['cy'] = cy
        self.attributes['r'] = r