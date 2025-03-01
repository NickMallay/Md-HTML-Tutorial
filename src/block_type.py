from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_list = markdown.strip().split("\n\n")
    stripped_block_list = [
        "\n".join(line.strip() for line in block.split("\n")).strip()
        for block in block_list if block.strip()
    ]
    return stripped_block_list

def is_ordered_list(block):
    lines = block.split('\n')
    if not lines:
        return False
    for i, line in enumerate(lines, 1):
        if not re.match(rf'^{i}\.\s+', line):  # Ensures "X. " with possible extra spaces
            return False
    return True

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH