from .elements import Element, Shape

class Graphic:
    def __init__(self, width=None, height=None, background=None, **kwargs):
        self.width = width
        self.height = height
        self.background = background
        self.elements: list[Element] = []
        self.tags_used = []
        self.text_used = False
        self.default_styles = {}
        self.default_styles['fill'] = kwargs.get('fill', '#EBF3F7')
        self.default_styles['stroke'] = kwargs.get('stroke', '#9CA7AD')
        self.default_styles['stroke-width'] = kwargs.get('strokewidth', 2)
        
    def add(self, element:Element):
        self.elements.append(element)
        tag = element.tag
        # if isinstance(element, Shape) and element.tag not in self.tags_used:
        ignored_elements = ['g', 'text']
        if element.tag not in self.tags_used and element.tag not in ignored_elements:
            self.tags_used.append(element.tag)
            self.tags_used.sort()
        if element.tag == 'text':
            self.text_used = True

    def to_svg(self):
        # TODO: allow default styles to be specified for shapes
        svg_string = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n"""
        width_svg = f' width="{self.width}"' if self.width is not None else ""
        height_svg = f' height="{self.height}"' if self.height is not None else ""
        svg_string += f"""<svg xmlns="http://www.w3.org/2000/svg"{width_svg}{height_svg}>\n"""
        if self.tags_used or self.text_used:
            svg_string += "  <style>\n"
        if self.tags_used:
            svg_string += f'''    {", ".join(self.tags_used)} {{\n'''
            svg_string += f'''      fill: {self.default_styles['fill']};\n'''
            svg_string += f'''      stroke: {self.default_styles['stroke']};\n'''
            svg_string += f'''      stroke-width: {self.default_styles['stroke-width']};\n'''
            svg_string += '    }\n'
        if self.text_used:
            svg_string += "    text { font-family: sans-serif; text-anchor: middle; dominant-baseline: middle; fill: #40484D; }\n"
        if self.tags_used or self.text_used:
            svg_string += "  </style>\n"
        if self.background:
            svg_string += f'  <rect width="100%" height="100%" style="fill: {self.background}; stroke: none" />\n'
        for element in self.elements:
            # svg_string += "  " + element.to_svg() + "\n"
            svg_string += element.to_svg() + "\n"
        svg_string += """</svg>"""
        return svg_string
    
    def save(self, filepath):
        svg_string = self.to_svg()
        with open(filepath, 'w') as output:
            output.write(svg_string)