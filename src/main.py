from textnode import TextNode


def main():

    node1 = TextNode("This is a dummy node", "bold", "htts://www.google.com")
    node2 = TextNode("This is a dummy node", "bold", "htts://www.google.com")
    print(node1)
    print(node1 == node2)




main()