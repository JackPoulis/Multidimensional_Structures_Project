from tools import Datapoint

class Node():
    def __init__(self, value, leftC = None, rightC = None, id = None, subtree = None):
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.subTree: RangeTree = subtree
        self.value = value
        self.id = id

    def isLeaf(self):
        if self.leftChild or self.rightChild:
            return False
        else:
            return True

    def __str__(self) -> str:
        string = str(self.value) + ": "
        if self.isLeaf():
            tail = "id: " + (str(self.id) if self.id else "-")
        else:
            tail = "Left: {leftvalue}, Right: {rightvalue}"
            leftstr = rightstr = "-"
            if self.leftChild:
                leftstr = str(self.leftChild.value)
            if self.rightChild:
                rightstr = str(self.rightChild.value)
            tail = tail.format(leftvalue = leftstr, rightvalue = rightstr)
        
        return string + tail

def extractLeafs(node: Node):
    leafs = []
    if node.isLeaf():
        leafs.append(node)
    else:
        for child in [node.leftChild, node.rightChild]:
            if child:
                [leafs.append(leaf) for leaf in extractLeafs(child)]
    return leafs

class RangeTree():
    def __init__(self, datapoints = None, axis=0):
        self.axis = axis
        self.dimensions = len(datapoints[0].vector) if datapoints else 1
        self.terminalTree = True if self.axis == self.dimensions-1 else False
        self.root = self.build(datapoints)

    def build(self, datapoints=None, node: Node = None):
        if datapoints == None or len(datapoints) == 0:
            return None

        values = list(set([datapoint.vector[self.axis] for datapoint in datapoints]))
        values = sorted(values)
        
        mid = (len(values)-1)//2
        nodevalue = values[mid]

        leftpoints = [datapoint for datapoint in datapoints if datapoint.vector[self.axis] <= nodevalue]
        rightpoints = [datapoint for datapoint in datapoints if datapoint not in leftpoints]

        nodeid = None
        if self.terminalTree:
            nodesubtree = None
            if len(values) == 1:
                nodeid = [datapoint.id for datapoint in datapoints]
                nodevalue = datapoints[0].vector[self.axis]
        else:
            newaxis = self.axis+1
            nodesubtree = RangeTree(datapoints, axis=newaxis)
            
        node = Node(value=nodevalue, subtree=nodesubtree, id=nodeid)

        if len(values) > 1:
            node.leftChild = self.build(leftpoints, node.leftChild)
            node.rightChild = self.build(rightpoints, node.rightChild)
            
        return node

    def split_search(self, start, end, node: Node, right_search=False):
        subroots = []

        right = node.rightChild
        left = node.leftChild
        if right_search==True:
            right = node.leftChild
            left = node.rightChild

        if right:
            if start <= node.value <= end:
                subroots.append(right)
                if left:
                    [subroots.append(subroot) for subroot in self.split_search(start, end, left, right_search=right_search)]
            else:
                [subroots.append(subroot) for subroot in self.split_search(start, end, right, right_search=right_search)]
        else:
            if start <= node.value <= end:
                if left:
                    [subroots.append(subroot) for subroot in self.split_search(start, end, left, right_search=right_search)]
                else:
                    subroots.append(node)

        return subroots

    def findSplitNode(self, start, end, node: Node=None) -> Node:
        if node is None:
            node = self.root
        
        splitnode = None

        if start <= node.value <= end:
            splitnode = node
        elif node.value < start:
            if node.rightChild:
                splitnode = self.findSplitNode(start, end, node.rightChild)
        else:
            if node.leftChild:
                splitnode = self.findSplitNode(start, end, node.leftChild)

        return splitnode

    def range_search(self, startVector: list, endVector: list, node=None):

        if self.root is None:
            return []

        if node is None:
            node = self.root

        start = startVector[self.axis] if isinstance(startVector, list) else startVector
        end = endVector[self.axis] if isinstance(endVector, list) else endVector

        if end < start:
            temp = end
            end = start
            start = temp
 
        splitnode = self.findSplitNode(start, end)
        if splitnode is None:
            return []
 
        subtrees = []
        if splitnode.isLeaf():
            subtrees = [splitnode]
        else:
            if splitnode.leftChild:
                left_subtrees_roots = self.split_search(start, end, splitnode.leftChild)
                subtrees = left_subtrees_roots
            if splitnode.rightChild:
                right_subtrees_roots = self.split_search(start, end, splitnode.rightChild, right_search=True)
                subtrees = subtrees + right_subtrees_roots

        results = []
        if self.terminalTree:
            for tree in subtrees:
                [results.append(node) for node in extractLeafs(tree)] 
        else:
            for tree in subtrees:
                for node in tree.subTree.range_search(startVector, endVector):
                    results.append(node)
        return results

    def __str__(self, node: Node = None) -> str:
        if self.root == None:
            return ''

        if node is None:
            node = self.root
        string = " axis: " + str(self.axis) + " | " + str(node) + "\n"

        for child in [node.leftChild, node.rightChild]:
            if child:
                string += self.__str__(child)
        
        if node.subTree:
            string += str(node.subTree)

        return string

if __name__ == "__main__":
    dictionary = {'a':[1,1],'b':[2,4],'c':[3,1],'d':[4,3],'e':[5,6],'f':[6,5]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    tree = RangeTree(datapoints)
    print(str(tree))
    # results = tree.range_search([1,1,2],[6,5,1])
    # for node in results:
    #     print(node.id[0],dictionary[node.id[0]])
