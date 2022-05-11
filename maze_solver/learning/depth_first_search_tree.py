# tree = {
#     "A": ["B","C"],
#     "B": ["D","E"],
#     "C": ["I","J"],
#     'D': ['F'],
#     'E' : ['G','H'],
#     'I' : [],
#     'J' : ['K','L'],
#     'F' : [],
#     'G' : [],
#     'H' : ['M'],
#     'L' : [],
#     'K' : []
# }


# print(tree)

class Node:
    def __init__(self,val):
        self.left = None
        self.right = None
        self.val = val

def DFSIO(root):
    if root:
        DFSIO(root.left)
        print(root.val),
        DFSIO(root.right)

def DFSpre(root):
    if root:
        print(root.val),
        DFSpre(root.left)
        DFSpre(root.right)


def DFSpost(root):
    if root:
        DFSpost(root.left)
        DFSpost(root.right)
        print(root.val),

root = Node(1)
root.right = Node(3)
root.left = Node(2)
root.left.left = Node(4)
root.left.right = Node(5)


print('''
1. inorder
2. preorder
3. postorder
''')
x = int(input('Enter option: '))

match x:
    case 1:
        DFSIO(root)
    case 2:
        DFSpre(root)
    case 3:
        DFSpost(root)