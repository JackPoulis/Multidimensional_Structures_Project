from tools import *

class Node():
    def __init__(self, value, axis, leftC = None, rightC = None, datapoint: Datapoint = None):
        self.value = value
        self.axis = axis
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.datapoint: Datapoint = datapoint
        
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
        string = "Axis: {axis}, Value: {value} -> "
        tail = "Left: {leftvalue}, Right: {rightvalue}"
        leftstr = rightstr = "-"
        if self.leftChild:
            leftstr = str(self.leftChild.value)
        if self.rightChild:
            rightstr = str(self.rightChild.value)
        tail = tail.format(leftvalue = leftstr, rightvalue = rightstr)
        if self.isLeaf():
            tail = str(self.datapoint)
        return string.format(axis = self.axis, value = self.value) + tail

class KDTree():
    """N-Dimensional k-d tree data structure

    :param datapoints: The datapoints to generate the tree. 
    If None creates an empty tree, defaults to None
    :type datapoints: Datapoint, optional
    """
    def __init__(self, datapoints = None):
        self.dimensions = len(datapoints[0].vector) if datapoints else 1
        self.root = self.build(datapoints)

    def build(self, datapoints: Datapoint = None, depth = 0) -> Node:
        # We assumed all datapoints have diferent positions 
        if datapoints == None or len(datapoints) == 0:
            return None

        axis = depth%self.dimensions

        values = list(set([datapoint.vector[axis] for datapoint in datapoints]))
        values = sorted(values)
        
        mid = (len(values)-1)//2
        nodevalue = values[mid]

        leftpoints = [datapoint for datapoint in datapoints if datapoint.vector[axis] <= nodevalue]
        rightpoints = [datapoint for datapoint in datapoints if datapoint not in leftpoints]

        node = Node(nodevalue, axis)
        if len(datapoints) == 1:
            node.datapoint=datapoints[0]
        else:
            node.leftChild = self.build(leftpoints, depth = depth + 1)
            node.rightChild = self.build(rightpoints, depth = depth + 1)
            
        return node

    # def range_search(self, startVector: list, endVector: list, node: Node = None):
    #     if self.root is None:
    #         return []
        
    #     if node is None:
    #         node = self.root

    #     s_range = (startVector, endVector)
    #     results = []
    #     if node.isLeaf():
    #         # if node.in_range(startVector, endVector):
    #         #   results.append(node)
    #     else:
    #         if contained(node.region(), s_range):
    #             [results.append(l) for l in extractLeafs(node)]
    #         else:
    #             if intersects(node.leftChild.region(), s_range):
    #                 self.range_search(startVector, endVector, node.leftChild)
    #             if intersects(node.rightChild.region(), s_range):
    #                 self.range_search(startVector, endVector, node.rightChild)

    def __str__(self, node: Node = None) -> str:
        string = ''
        if self.root == None:
            return string

        if node is None:
            node = self.root

        string = str(node) + "\n"

        for child in [node.leftChild, node.rightChild]:
            if child:
                string += self.__str__(child)

        return string

if __name__ == "__main__":
    dictionary = {'p1':[1,4],'p2':[3,6],'p3':[4,2],'p4':[2,9],'p5':[5,8],'p6':[9,1],'p7':[6,5],'p8':[10,3],'p9':[7,9],'p10':[8,7]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    tree = KDTree(datapoints)
    print(tree)