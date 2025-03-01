from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        prop_list = [f" {key}=\"{value}\"" for key, value in self.props.items()]
        return "".join(prop_list)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})" 

    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None or self.value == "":
            print(f"🚨 ERROR: LeafNode with tag <{self.tag}> has no value!")
            raise ValueError

        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def to_html(self):
        if self.tag == "img":
            # Self-closing <img> tag (no value, just props)
            return f"<img{self.props_to_html()} />"
        
        if self.value is None or self.value == "":
            print(f"🚨 ERROR: LeafNode with tag <{self.tag}> has no value!")
            raise ValueError

        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
     def __init__(self, tag, children, props=None):
          super().__init__(tag, None, children, props)

     def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError
        if self.children == None or self.children == []:
            raise ValueError("No Children found")
        html =  f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html


def text_node_to_html_node(text_node):
    print(f"🔍 Converting TextNode: {text_node.text_type}, Value: {repr(text_node.text)}")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        print(f"🖼 Processing image: alt={repr(text_node.text)}, src={repr(text_node.url)}")

        # 🚨 Prevent crash if the image URL is missing
        if not text_node.url:
            raise ValueError(f"🚨 Image missing URL! Alt text: {repr(text_node.text)}")

        # Ensure alt text is at least an empty string
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text or ""})

    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")
    