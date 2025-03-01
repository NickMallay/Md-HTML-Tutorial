from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for old_node in old_nodes:
        # If it's not a regular text node, add it as-is
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
    
        text = old_node.text
        first_delim_pos = text.find(delimiter)

        if first_delim_pos == -1:
            result.append(old_node)
            continue

        second_delim_pos = text.find(delimiter, first_delim_pos + len(delimiter))

        if second_delim_pos == -1:
            raise Exception(f"No closing delimiter found: {delimiter}")
        
        before_text = text[:first_delim_pos]
        delimited_text = text[first_delim_pos + len(delimiter):second_delim_pos]
        after_text = text[second_delim_pos + len(delimiter):]

        if before_text:
            result.append(TextNode(before_text, TextType.TEXT))
        
        result.append(TextNode(delimited_text, text_type))
        
        if after_text:
            result.extend(split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type))
    
    return result

def split_nodes_link(old_nodes):
    new_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        text = old_node.text

        links = extract_markdown_links(text)

        if not links:
            new_list.append(old_node)
            continue

        remaining_text = text

        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_list.append(TextNode(parts[0], TextType.TEXT))

            new_list.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
                new_list.append(TextNode(remaining_text, TextType.TEXT))
    return new_list

def split_nodes_image(old_nodes):
    new_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        text = old_node.text

        images = extract_markdown_images(text)

        if not images:
            new_list.append(old_node)
            continue

        remaining_text = text

        for alt_text, image_url in images:
            image_markdown = f"![{alt_text}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)

            if parts[0]:
                new_list.append(TextNode(parts[0], TextType.TEXT))

            new_list.append(TextNode(alt_text, TextType.IMAGE, image_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
                new_list.append(TextNode(remaining_text, TextType.TEXT))
    return new_list






def extract_markdown_images(text):
    regex_image_patern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(regex_image_patern, text)
    return images
def extract_markdown_links(text):
    regex_link_patern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(regex_link_patern, text)
    return links

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

