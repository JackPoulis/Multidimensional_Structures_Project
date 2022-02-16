from tools import Datapoint

class Node():
    def __init__(self, value, leftC = None, rightC = None, id = None, subtree = None):
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.subTree: RangeTree = subtree
        self.value = value
        self.id = id

    def isLeaf(self):
        """Checks if the node is a leaf. A leaf node has no child nodes

        :return: True if the node is leaf else False
        :rtype: bool
        """
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
    """Takes a node of a tree/subtree and returns all the leaf nodes below that node

    :param node: The root/subroot node of the tree/subtree to extract leafs
    :type node: Node
    :return: A list of all leaf nodes found below the node
    including the node if it is a leaf node
    :rtype: list
    """

    leafs = []
    if node.isLeaf():
        leafs.append(node)
    else:
        for child in [node.leftChild, node.rightChild]:
            if child:
                [leafs.append(leaf) for leaf in extractLeafs(child)]
    return leafs

class RangeTree():
    """N-Dimensional range tree data structure

    :param datapoints: The datapoints to generate the tree. 
    If None creates an empty tree, defaults to None
    :type datapoints: Datapoint, optional
    :param axis: The dimension of the current tree. 
    It is used internally for recursion, defaults to 0
    :type axis: int, optional
    """

    def __init__(self, datapoints: Datapoint = None, axis = 0):
        self.axis = axis
        self.dimensions = len(datapoints[0].vector) if datapoints else 1
        self.terminalTree = True if self.axis == self.dimensions-1 else False
        self.root = self.build(datapoints)

    def build(self, datapoints: Datapoint=None, node: Node = None) -> Node:
        """The build method of the range tree

        :param datapoints: The datapoints if provided become 
        the nodes of the tree, defaults to None
        :type datapoints: Datapoint, optional
        :param node: This parameter is used internally for
        the recursion of this method, defaults to None
        :type node: Node, optional
        :return: Returns the root/subroot node of the new tree/subtree
        :rtype: Node
        """

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

    def split_search(self, start, end, node: Node, right_search = False):
        """Called internally by range_search() after the split node is found

        :param start: The lower bound of the search
        :type start: Any
        :param end: The upper bound of the search
        :type end: Any
        :param node: The root/subroot of the tree to search
        :type node: Node
        :param right_search: Specifies if this search 
        is right or left search, defaults to False
        :type right_search: bool, optional
        :return: all the trees/subtrees that have points
        in the range of search
        :rtype: list
        """

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

    def findSplitNode(self, start, end, node: Node = None) -> Node:
        """Finds the node where the range search splits to left and right search

        :param start: The lower bound of the search
        :type start: Any
        :param end: The upper bound of the search
        :type end: Any
        :param node: The root/subroot of the tree to search. If None provided
        the search starts from the root of the tree, defaults to None
        :type node: Node, optional
        :return: Returns the split node of the range search
        :rtype: Node
        """

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

    def range_search(self, startVector: list, endVector: list, node: Node = None):
        """Searches for the leaf nodes that are in the hyperrectangle [startVector, endVector]
        If tree is 1D it searches for 1D points in the range [startVector, endVector]

        :param startVector: The "corner" of the hyperrectangle
        :type startVector: list
        :param endVector: The hyperrectangle's antidiamentric "corner" of startVector
        :type endVector: list
        :param node: The root/subroot from where to start the search. If None provided
        it starts from the tree's root, defaults to None
        :type node: Node, optional
        :return: Returns the resulting nodes of the range search
        :rtype: list
        """

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
