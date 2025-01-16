from htmlnode import HTMLNode

def test_htmlnode_1():
    node = HTMLNode(None, None, None, None)
    assert node.props_to_html() == ""
def test_htmlnode_2():
    node = HTMLNode(None, None, None, {"bear": "grizzly"})
    assert node.props_to_html() == ' bear="grizzly"'
def test_htmlnode_3():
    node = HTMLNode(None, None, None, {"wizard": "magical", "honey": "sweet"})
    assert node.props_to_html() == ' wizard="magical" honey="sweet"'