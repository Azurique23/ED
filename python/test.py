from .bin_tree import Node

print(1_000)


def in_order(node: Node):
    right = []
    left = []
    if node.right:
        right += in_order(node.right)
    if(node.left):
        left += in_order(node.left)

    return right + [node.value] + left

def insert(node:Node, value):
    if node.value > value:
        if node.right:
            insert(node.right, value)
        else:
            node.right = Node(value)
    else:
        if node.left:
            insert(node.left, value)
        else:
            node.left = Node(value)

def in_order(node: Node):
    right = []
    left = []
    if node.right:
        right += in_order(node.right)
    if(node.left):
        left += in_order(node.left)

    return right + [node.value] + left


def pre_order(node: Node) -> list:
    right = [node.value]
    left = []
    if node.right:
        right += pre_order(node.right)
    if node.left:
        left += pre_order(node.left)
    return right + left


def pos_order(node: Node) -> list:
    right = []
    left = []
    if node.right:
        right = pos_order(node.right)
    if node.left:
        left = pos_order(node.left)
    return right + left + [node.value]

def travel(node:Node)-> list:
    rightpr = righti = rightpo  = ""
    leftpr = lefti = leftpo =  ""
    if node.right:
        rightpr, righti , rightpo = search(node.right)
    if node.left:
        leftpr, lefti, leftpo = search(node.left)
    value = str(node.value)
    return [value+" "+rightpr+ leftpr, righti +value+" "+lefti, rightpo + leftpo + value + " "]
    return [[node.value] + rightpr + leftpr, righti + [node.value] + lefti, rightpo + leftpo + [node.value]]

def insertInter(node:Node, value):
    while node:
        if node.value > value:
            if node.right:
                node = node.right
            else:
                node.right = Node(value)
                break
        else:
            if node.left:
                node = node.left
            else:
                node.left = Node(value)
                break