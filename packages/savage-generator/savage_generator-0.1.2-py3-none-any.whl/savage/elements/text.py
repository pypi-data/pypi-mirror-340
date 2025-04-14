from .element import Element

class Text(Element):
    def __init__(self, x, y, content, **kwargs):
        super().__init__(**kwargs)
        self.tag = "text"
        self.attributes['x'] = x
        self.attributes['y'] = y
        self.content = content
        self.styles['font-family'] = kwargs.get('font', None)
        self.styles['font-size'] = kwargs.get('size', None)
        self.styles['text-anchor'] = kwargs.get('anchor', None)
        self.styles['dominant-baseline'] = kwargs.get('baseline', None)