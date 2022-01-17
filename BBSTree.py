import numpy as np

#TO DO:
#Build DONE
#Insert
#Delete
#Update?
#Search

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
        mid = (len(datapoints)-1)//2
        leftpoints = datapoints[:mid]
        rightpoints = datapoints[mid+1:]
        subroot = Node(datapoints[mid])
        subroot.leftChild = self.buildStructure(leftpoints, subroot.leftChild)
        subroot.rightChild = self.buildStructure(rightpoints, subroot.rightChild)
        return subroot

    def buildLeafs(self, datapoints):
        for point in datapoints:
            self.insert(Node(point), self.root)

    def build(self, datapoints):
        datapoints = sorted(datapoints)
        self.root = self.buildStructure(datapoints)
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
    datapoints = [6,7,8,9,10]
    tree = BBSTree()
    tree.build(datapoints)
    tree.printTree()