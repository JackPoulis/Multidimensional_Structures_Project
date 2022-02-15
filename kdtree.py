from tools import Datapoint

class Node():
    def __init__(self, datapoint: Datapoint, leftC = None, rightC = None, id = None, depth = 0):
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.datapoint:Datapoint = datapoint
        self.depth = depth
        self.axis = depth%len(datapoint.vector)

    def isLeaf(self):
        if self.leftChild or self.rightChild:
            return False
        else:
            return True

    def __str__(self) -> str:
        string = str(self.datapoint.id) + ": "
        tail = "Left: {leftvalue}, Right: {rightvalue}"
        leftstr = rightstr = "-"
        if self.leftChild:
            leftstr = str(self.leftChild.datapoint.id)
        if self.rightChild:
            rightstr = str(self.rightChild.datapoint.id)
        tail = tail.format(leftvalue = leftstr, rightvalue = rightstr)
        
        return string + tail

class KDTree():
    def __init__(self, datapoints = None):
        self.dimensions = len(datapoints[0].vector) if datapoints else 1
        self.root = self.build(datapoints)

    def build(self, datapoints, depth = 0):
        if datapoints == None or len(datapoints) == 0:
            return None

        axis = depth%self.dimensions
        datapoints.sort(key=lambda x: x.vector[axis])

        mid = (len(datapoints)-1)//2
        nodepoint: Datapoint = datapoints[mid]

        node = Node(nodepoint, depth = depth)

        leftpoints = [datapoint for datapoint in datapoints if datapoint.vector[axis] < node.datapoint.vector[axis]]
        rightpoints = [datapoint for datapoint in datapoints if datapoint.vector[axis] > node.datapoint.vector[axis]]

        node.leftChild = self.build(leftpoints, depth = depth + 1)
        node.rightChild = self.build(rightpoints, depth = depth + 1)
            
        return node

    def range_search(self, startVector: list, endVector: list, node=None):
        pass

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
    dictionary = {'a':[1,1],'b':[2,4],'c':[3,1],'d':[4,3],'e':[5,6],'f':[6,5]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    tree = KDTree(datapoints)
    print(tree)