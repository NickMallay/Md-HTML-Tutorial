from textnode import *
from htmlnode import *
from text_capture import *
from block_type import *
import shutil
import os
import re
import sys
def text_to_children(text):
    # Clean up spacing between lines
    cleaned_text = " ".join(text.splitlines()).strip()
    
    text_nodes = text_to_textnodes(cleaned_text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes
def markdown_to_html_node(markdown):
    print(f"Processing markdown: {markdown}")
    parent_node = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    print(f"Found blocks: {blocks}")
    

    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block: '{block}' has type: {block_type}")
        if block_type == BlockType.PARAGRAPH:
            # Get children from inline text
            children = text_to_children(block) ## Need to create    
            #Make parent node with children
            paragraph_node = ParentNode("p", children)
            #add to parent div
            parent_node.children.append(paragraph_node)

        elif block_type == BlockType.HEADING:
            #Determin heading level
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else: 
                    break
            #remove heading tag and get children
            heading_text = block.lstrip("#").strip()
            children = text_to_children(heading_text)

            #make node with correct heading tag
            heading_node = ParentNode(f"h{level}", children)

            #add to parent div
            parent_node.children.append(heading_node)
        
        elif block_type == BlockType.CODE:
            # Remove leading/trailing backticks and extra newlines
            code_text = block.strip("`").strip("\n").strip()

            # 🚨 Fix: If empty, do not process
            if not code_text.strip():
                print("⚠️ Skipping empty code block to prevent crash")
                continue

            # ✅ Create a LeafNode with the "code" tag (NO extra ParentNode for <code>)
            html_node = LeafNode("code", code_text)

            # ✅ Wrap it directly inside <pre> (this is correct HTML structure)
            pre_node = ParentNode("pre", [html_node])

            # Append to parent node
            parent_node.children.append(pre_node)

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                if not line.strip():
                    continue
                item_text = line.strip()
                if item_text.startswith ("- "):
                    item_text = item_text[2:]
                item_children = text_to_children(item_text)

                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ul_node = ParentNode("ul", list_items)

            parent_node.children.append(ul_node)



        
        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                if not line.strip():
                    continue
                item_text = line.strip()
                prefix_end = 0
                for i, char in enumerate(item_text):
                    if char == "." and i + 1 < len(item_text) and item_text[i + 1] == " ":
                        prefix_end = i +2
                        break
                if prefix_end > 0:
                    item_text = item_text[prefix_end:]
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ol_node = ParentNode("ol", list_items)
            parent_node.children.append(ol_node)
        
        elif block_type == BlockType.QUOTE:
            quote_lines = []
            for line in block.split("\n"):
                line = line.strip()  # Strip spaces
                if line.startswith(">"):  # Check if it's a blockquote line
                    if len(line) > 1 and line[1] == " ":
                        line = line[2:].strip()  # Remove '> ' and trim
                    else:
                        line = line[1:].strip()  # Remove '>' and trim
                # Skip empty lines after processing
                if not line:  
                    continue
                quote_lines.append(line)
            
            # Join remaining lines with a single space
            quote_text = " ".join(quote_lines)
            print(f"DEBUG: Quote text: '{quote_text}'")  # Display cleaned and joined text for verification
            
            quote_children = text_to_children(quote_text)
            blockquote_node = ParentNode("blockquote", quote_children)
            parent_node.children.append(blockquote_node)

    return parent_node
def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)  

def copy_directory(src, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(src):
        src_path = os.path.join(src,item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, destination_path)
            print(f"Copied file: {src_path} > {destination_path}")
        elif os.path.isdir(src_path):
            # Special case: If copying "static/index/", flatten its contents
            if item == "index":
                for file in os.listdir(src_path):
                    file_src_path = os.path.join(src_path, file)
                    file_dest_path = os.path.join(destination, file)
                    shutil.copy(file_src_path, file_dest_path)
                    print(f"Flattened file: {file_src_path} → {file_dest_path}")
            else:
                os.makedirs(destination_path, exist_ok=True)
                print(f"Created directory: {destination_path}")
                copy_directory(src_path, destination_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "): 
            return line[2:].strip()
        
    raise ValueError("No H1 title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Replace absolute paths in href/src with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')


    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Page generated: {dest_path}")



def main():
    # Get base path from command line, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

        # Ensure it ends with "/"
    if not basepath.endswith("/"):
        basepath += "/"
    print(f"Using base path: {basepath}")
    
    clear_directory("docs")
    copy_directory("static", "docs")
    
    content_path = "content"
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file.endswith(".md"):
                # Get the full path to the markdown file
                md_path = os.path.join(root, file)
                
                # Calculate the relative path from content directory
                rel_path = os.path.relpath(md_path, content_path)
                
                # Convert the output path: change .md to .html and put in docs directory
                output_rel_path = os.path.splitext(rel_path)[0] + ".html"
                output_path = os.path.join("docs", output_rel_path)
                
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Generate the page
                generate_page(md_path, "template.html", output_path, basepath)
    
    print("Site generation complete!")

if __name__ == "__main__":
    main()