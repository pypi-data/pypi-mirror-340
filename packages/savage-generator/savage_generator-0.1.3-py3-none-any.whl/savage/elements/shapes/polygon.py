from .shape import Shape

class Polygon(Shape):
    def __init__(self, points:list[int], **kwargs):
        super().__init__(**kwargs)
        self.tag = "polygon"
        if len(points) % 2 != 0:
            raise ValueError("Points must contain an even number of elements (x, y pairs).")
        self.attributes['points'] = points
        
    def add_attribute_svg(self):
        points_svg = " ".join([f"{self.attributes['points'][i]},{self.attributes['points'][i+1]}" for i in range(0, len(self.attributes['points']), 2)])
        return f' points="{points_svg}"'