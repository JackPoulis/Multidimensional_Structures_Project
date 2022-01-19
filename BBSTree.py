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
        print('Data:\t', self.value)
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
            self.insertLeaf(Node(point), self.root)

    def build(self, datapoints):
        datapoints = sorted(datapoints)
        self.root = self.buildStructure(datapoints)
        self.buildLeafs(datapoints)

    def insertLeaf(self, newNode: Node, subroot: Node = None):

        if self.root is None:
            self.root = newNode
            return

        if subroot is None:
            subroot = self.root
        if newNode.value > subroot.value:
            if subroot.rightChild:
                self.insertLeaf(newNode, subroot.rightChild)
            else:
                subroot.rightChild = newNode
        else:
            if subroot.leftChild:
                self.insertLeaf(newNode, subroot.leftChild)
            else:
                subroot.leftChild = newNode

    def search(self, value, node=None):
        if node is None:
            node = self.root

        if value == node.value and node.isLeaf():
            return node
        elif value <= node.value and node.leftChild:
            return self.search(value, node.leftChild)
        elif node.rightChild:
            return self.search(value, node.rightChild)
        else:
            return None

    def left_search(self, start, node: Node):
        subtrees_roots = []
        if node.value >= start:
            if node.isLeaf():
                subtrees_roots.append(node)
            else:
                if node.rightChild:
                    subtrees_roots.append(node.rightChild)
                if node.leftChild:
                    for subtree_root in self.left_search(start, node.leftChild):
                        subtrees_roots.append(subtree_root)
        else:
            if node.rightChild:
                for subtree_root in self.left_search(start, node.rightChild):
                        subtrees_roots.append(subtree_root)

        return subtrees_roots
            
    def right_search(self, end, node: Node):
        subtrees_roots = []
        if node.value <= end:
            if node.isLeaf():
                subtrees_roots.append(node)
            else:
                if node.rightChild:
                    for subtree_root in self.right_search(end, node.rightChild):
                        subtrees_roots.append(subtree_root)
                if node.leftChild:
                    subtrees_roots.append(node.leftChild)
        else:
            if node.leftChild:
                for subtree_root in self.right_search(end, node.leftChild):
                    subtrees_roots.append(subtree_root)

        return subtrees_roots

    def range_search(self, start, end, node=None):
        if end < start:
            temp = end
            end = start
            start = temp
        if node is None:
            node = self.root
        results = []
        if node.value < start and node.rightChild:
            results = self.range_search(start, end, node.rightChild)
        elif node.value > end and node.leftChild:
            results = self.range_search(start, end, node.leftChild)
        else:
            # print('Split node:')
            # node.printNode()
            if node.leftChild:
                left_subtrees_roots = self.left_search(start, node.leftChild)
                results = left_subtrees_roots
            if node.rightChild:
                right_subtrees_roots = self.right_search(end, node.rightChild)
                results = results + right_subtrees_roots

        return results

    def printLeafs(self, subroots):
        for subroot in subroots:
            if subroot.isLeaf():
                subroot.printNode()
            else:
                if subroot.leftChild:
                    self.printLeafs([subroot.leftChild])
                if subroot.rightChild:
                    self.printLeafs([subroot.rightChild])

    def printTree(self, node: Node = None):
        if node is None:
            node = self.root
        node.printNode()
        for child in [node.leftChild, node.rightChild]:
            if child:
                self.printTree(child)

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

if __name__ == "__main__":
    datapoints = [1,2,3,4,5,6,7,8,9,10]
    tree = BBSTree()
    tree.build(datapoints)
    # tree.printTree()
    print('=================================')
    # tree.search(11).printNode()
    mylist = tree.range_search(1, 2)
    tree.printLeafs(mylist)
    # for node in mylist:
    #     node.printNode()