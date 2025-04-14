from .element import Element

class Group(Element):
    def __init__(self, content=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = "g"
        self.content: list[Element] = content if content is not None else []
        
    def add(self, element:Element):
        self.content.append(element)
        
    def add_open_tag_svg(self):
        return super().add_open_tag_svg() +"\n"
    
    def add_content_svg(self, indentation=2):
        content_svg = ""
        for element in self.content:
            content_svg += element.to_svg(indentation+2) + "\n"
        return content_svg