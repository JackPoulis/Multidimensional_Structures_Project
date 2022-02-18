from tools import *

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

    def build(self, datapoints: Datapoint=None) -> Node:
        """The build method of the range tree.
        This code assumes that all datapoints are different

        :param datapoints: The datapoints if provided become 
        the nodes of the tree, defaults to None
        :type datapoints: Datapoint, optional
        :return: Returns the root/subroot node of the new tree/subtree
        :rtype: Node
        """

        if datapoints == None or len(datapoints) == 0:
            return None

        values = list(set([dp.vector[self.axis] for dp in datapoints]))
        values = sorted(values)
        
        mid = (len(values)-1)//2
        nodevalue = values[mid]

        leftpoints = [dp for dp in datapoints if dp.vector[self.axis] <= nodevalue]
        rightpoints = [dp for dp in datapoints if dp not in leftpoints]

        nodepoint = None
        if self.terminalTree:
            nodesubtree = None
            if len(values) == 1:
                nodepoint = datapoints[0]
                nodevalue = datapoints[0].vector[self.axis]
        else:
            newaxis = self.axis+1
            nodesubtree = RangeTree(datapoints, axis=newaxis)
            
        node = Node(nodevalue, self.axis, subtree = nodesubtree, datapoint = nodepoint)

        if len(values) > 1:
            node.left_child = self.build(leftpoints)
            node.right_child = self.build(rightpoints)
            
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

        right = node.right_child
        left = node.left_child
        if right_search==True:
            right = node.left_child
            left = node.right_child

        if right:
            if start <= node.value <= end:
                subroots.append(right)
                if left:
                    subroots += self.split_search(start, end, left, right_search)
            else:
                subroots += self.split_search(start, end, right, right_search)
        else:
            if start <= node.value <= end:
                if left:
                    subroots += self.split_search(start, end, left, right_search)
                else:
                    subroots.append(node)

        return subroots

    def find_split_node(self, start, end, node: Node = None) -> Node:
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
            if node.right_child:
                splitnode = self.find_split_node(start, end, node.right_child)
        else:
            if node.left_child:
                splitnode = self.find_split_node(start, end, node.left_child)

        return splitnode

    def range_search(self, s_region: list, node: Node = None):
        """Searches for the leaf nodes that are 
        in the hyperrectangle s_region

        :param s_region: The region to search for the datapoints
        :type s_region: list
        :param node: The root/subroot from where to start the search.
        If None provided it starts from the tree's root, defaults to None
        :type node: Node, optional
        :return: Returns the resulting nodes of the range search
        :rtype: list
        """

        if self.root is None:
            return []

        if node is None:
            node = self.root

        start = s_region[self.axis][0]
        end = s_region[self.axis][1]

        if end < start:
            temp = end
            end = start
            start = temp
 
        splitnode = self.find_split_node(start, end)
        if splitnode is None:
            return []
 
        subtrees = []
        if splitnode.is_leaf():
            subtrees = [splitnode]
        else:
            if splitnode.left_child:
                l_roots = self.split_search(start, end, splitnode.left_child)
                subtrees = l_roots
            if splitnode.right_child:
                r_roots = self.split_search(start, end, splitnode.right_child, right_search=True)
                subtrees = subtrees + r_roots

        results = []
        if self.terminalTree:
            for tree in subtrees:
                [results.append(node) for node in extract_leafs(tree)] 
        else:
            for tree in subtrees:
                for node in tree.subtree.range_search(s_region):
                    results.append(node)
        return results

    def __str__(self, node: Node = None) -> str:
        if self.root == None:
            return ''

        if node is None:
            node = self.root
        string = str(node) + "\n"

        for child in [node.left_child, node.right_child]:
            if child:
                string += self.__str__(child)
        
        if node.subtree:
            string += str(node.subtree)

        return string

if __name__ == "__main__":
    dictionary = {'a':[1,1],'b':[2,4],'c':[3,1],'d':[4,3],'e':[5,6],'f':[6,5]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    tree = RangeTree(datapoints)
    print(str(tree))
    results = tree.range_search([[1,5],[1,5]])
    for node in results:
        print(node.datapoint)
