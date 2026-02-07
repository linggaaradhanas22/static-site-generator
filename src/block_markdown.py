from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # Split by double newlines to separate blocks
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        # Strip leading/trailing whitespace
        block = block.strip()
        # Skip empty strings (this handles cases with 3+ newlines)
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading check: 1-6 '#' followed by a space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code block check: starts and ends with ```
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote check: every line starts with >
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # Unordered list check: every line starts with "- "
    if block.startswith("- ") or block.startswith("* "):
        for line in lines:
            if not (line.startswith("- ") or line.startswith("* ")):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # Ordered list check: every line starts with "1. ", "2. ", etc.
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    # Default case
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return create_ulist_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return create_olist_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    """Helper to convert inline markdown text into HTMLNode children"""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_code_node(block):
    # Strip the backticks and handle the nested <code> structure
    text = block[4:-3] # Removes the ```\n and the ```
    if not text.endswith("\n"):
        text += "\n"
    raw_text_node = LeafNode(None, text)
    code_node = ParentNode("code", [raw_text_node])
    return ParentNode("pre", [code_node])

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_ulist_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:] # Remove the "- "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def create_olist_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        # Find the space after the dot, e.g., "1. text"
        pos = item.find(". ")
        text = item[pos + 2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)