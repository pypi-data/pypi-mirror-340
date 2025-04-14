from savage import Graphic, Circle, Rect

def test_graphic_creation():
    graphic = Graphic(width=500, height=400)

    assert graphic.width == 500
    assert graphic.height == 400
    assert graphic.elements == []

def test_graphic_add_elements():
    graphic = Graphic(width=500, height=400)
    circle = Circle(cx=50, cy=50, r=20)
    rect = Rect(width=100, height=50, x=150, y=150)

    graphic.add(circle)
    graphic.add(rect)

    assert len(graphic.elements) == 2
    assert graphic.elements[0] is circle
    assert graphic.elements[1] is rect

def test_graphic_to_svg():
    graphic = Graphic(width=500, height=400)
    circle = Circle(cx=50, cy=50, r=20, fill="red")
    rect = Rect(width=100, height=50, x=150, y=150, fill="blue")

    graphic.add(circle)
    graphic.add(rect)

    svg_output = graphic.to_svg()

    # Check that the SVG output contains the correct XML structure
    assert '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' in svg_output
    assert '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="400">' in svg_output
    assert '<circle' in svg_output  # Verify Circle element is included
    assert 'fill: red;' in svg_output  # Verify the fill of the circle
    assert '<rect' in svg_output  # Verify Rect element is included
    assert 'fill: blue;' in svg_output  # Verify the fill of the rect
    assert svg_output.endswith('</svg>')  # Ensure the SVG tag closes correctly

def test_graphic_save(mocker):
    # Mock the open function to avoid actually writing to the file system
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    
    graphic = Graphic(width=500, height=400)
    circle = Circle(cx=50, cy=50, r=20)
    graphic.add(circle)

    graphic.save("test_output.svg")

    # Check if open was called with the correct filepath
    mock_open.assert_called_once_with("test_output.svg", 'w')
    
    # Check that the file contents match the expected SVG output
    svg_output = graphic.to_svg()
    mock_open.return_value.write.assert_called_once_with(svg_output)

def test_svg_element_order_preserved():
    graphic = Graphic(width=500, height=400)
    rect = Rect(width=100, height=50, x=10, y=10)
    circle = Circle(cx=20, cy=20, r=10)

    graphic.add(rect)
    graphic.add(circle)

    svg_output = graphic.to_svg()

    # rect should appear before circle
    rect_index = svg_output.index("<rect")
    circle_index = svg_output.index("<circle")
    assert rect_index < circle_index
