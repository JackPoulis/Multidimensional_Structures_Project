import numpy as np

class Node():
    def __init__(self, value, leftC = None, rightC = None):
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.value = value
        self.height = 0

    def isLeaf(self):
        if self.leftChild or self.rightChild:
            return False
        else:
            return True

    def printNode(self):
        print('Data:\t',self.value)
        if self.leftChild:
            print('Left:\t', self.leftChild.value)
        if self.rightChild:
            print('Right:\t', self.rightChild.value)
        print('Balance:\t', self.height)
        if self.isLeaf():
            print('Leaf')
        else:
            print('Internal')
        print('-----------------------------')

class BBSTree():
    def __init__(self, datapoints = None):
        if datapoints:
            self.build(datapoints)
        else:
            self.root = None

    def buildStructure(self, datapoints, subroot: Node = None):
        if len(datapoints) == 0:
            return subroot
        mid = len(datapoints)//2 - (len(datapoints)+1)%2
        leftpoints = datapoints[:mid]
        rightpoints = datapoints[mid+1:]
        if self.root is None:
            self.root = Node(datapoints[mid])
            if subroot is None:
                subroot = self.root
            subroot.leftChild = self.buildStructure(leftpoints, subroot.leftChild)
            subroot.rightChild = self.buildStructure(rightpoints, subroot.rightChild)
        else:
            if subroot is None:
                subroot = self.root
            subroot = Node(datapoints[mid])
            subroot.leftChild = self.buildStructure(leftpoints, subroot.leftChild)
            subroot.rightChild = self.buildStructure(rightpoints, subroot.rightChild)
        return subroot

    def buildLeafs(self, datapoints):
        for leaf in datapoints:
            self.insert(Node(leaf), self.root)

    def build(self, datapoints):
        datapoints = sorted(datapoints)
        self.buildStructure(datapoints)
        self.buildLeafs(datapoints)

    def insert(self, newNode: Node, subroot: Node = None):
        if self.root is None:
            self.root = newNode
            return

        if subroot is None:
            subroot = self.root
        if newNode.value > subroot.value:
            if subroot.rightChild:
                self.insert(newNode, subroot.rightChild)
            else:
                subroot.rightChild = newNode
        else:
            if subroot.leftChild:
                self.insert(newNode, subroot.leftChild)
            else:
                subroot.leftChild = newNode
        
    def delete(self):
        return 0

    def search(self, startValues, endValues=None):
        node = self.root
        if node.isLeaf() and not (node is self.root):
            return node
        # if startValues<node.value

    # def rotateLeft(self, node: Node):
    #     replaceNode = node.rightChild
    #     if node is self.root:
    #         self.root = replaceNode
    #     t = replaceNode.leftChild
    #     replaceNode.leftChild = node
    #     node.rightChild = t
    #     return replaceNode

    # def rotateRight(self, node: Node):
    #     replaceNode = node.leftChild
    #     if node is self.root:
    #         self.root = replaceNode
    #     t = replaceNode.rightChild
    #     replaceNode.rightChild = node
    #     node.leftChild = t
    #     return replaceNode

    def printTree(self, node: Node = None):
        if node is None:
            node = self.root
        node.printNode()
        for child in [node.leftChild, node.rightChild]:
            if child:
                self.printTree(child)

if __name__ == "__main__":
    datapoints = [1,3,2,4,5,6,7,8,9,10]
    tree = BBSTree()
    tree.build(datapoints)
    tree.printTree()