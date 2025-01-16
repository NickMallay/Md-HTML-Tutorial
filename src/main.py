from textnode import *

def main():
    test_node = TextNode("This is a text node", TextType.Bold, "https://www.url.com")
    print(test_node)

if __name__ == "__main__":
    main()