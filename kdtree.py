from tools import *

class KDTree():
    """N-Dimensional k-d tree data structure

    :param datapoints: The datapoints to generate the tree. 
    If None creates an empty tree, defaults to None
    :type datapoints: Datapoint, optional
    """
    def __init__(self, datapoints = None):
        self.dimensions = len(datapoints[0].vector) if datapoints else 1
        self.total_region = calc_mbr(datapoints) if datapoints else None
        self.root = self.build(datapoints)

    def build(self, datapoints: Datapoint = None, depth = 0) -> Node:
        # We assume all datapoints have different positions 
        if datapoints == None or len(datapoints) == 0:
            return None

        axis = depth%self.dimensions

        values = list(set([datapoint.vector[axis] for datapoint in datapoints]))
        values = sorted(values)
        
        mid = (len(values)-1)//2
        nodevalue = values[mid]

        leftpoints = [dp for dp in datapoints if dp.vector[axis] <= nodevalue]
        rightpoints = [dp for dp in datapoints if dp not in leftpoints]

        node = Node(nodevalue, axis)
        if len(datapoints) == 1:
            node.datapoint=datapoints[0]
        else:
            node.left_child = self.build(leftpoints, depth = depth + 1)
            node.right_child = self.build(rightpoints, depth = depth + 1)
            
        return node

    def search(self, point, node: Node = None):
        if self.root is None:
            return None

        if node is None:
            node = self.root

        value = point[node.axis]

        result = None
        if value <= node.value:
            if node.left_child:
                result = self.search(point, node.left_child)
            elif node.is_leaf():
                if node.datapoint.vector == point:
                    result = node
        else:
            if node.right_child:
                result = self.search(point, node.right_child)

        return result

    def range_search(self, s_region: list, node: Node = None, region = None):
        if self.root is None:
            return []
        
        if node is None:
            node = self.root

        if region is None:
            region = self.total_region
        
        results = []

        if node.is_leaf():
            if node.datapoint.in_range(s_region):
                results.append(node)
        else:
            if contained(region, s_region):
                [results.append(l) for l in extract_leafs(node)]
            else:
                lc_region, rc_region = KDTree.bisect(region, node.axis, node.value)
                if intersects(lc_region, s_region):
                    results += self.range_search(s_region, node.left_child, lc_region)
                if intersects(rc_region, s_region):
                    results += self.range_search(s_region, node.right_child, rc_region)

        return results
    
    def bisect(region, axis, value):
        region[axis].sort()
        if value > region[axis][1] or value < region[axis][0]:
            return None
        lefthalf = [[v for v in ax] for ax in region]
        righthalf = [[v for v in ax] for ax in region]
        lefthalf[axis][1] = value
        righthalf[axis][0] = value
        return lefthalf, righthalf

    def __str__(self, node: Node = None) -> str:
        string = ''
        if self.root == None:
            return string

        if node is None:
            node = self.root

        string = str(node) + "\n"

        for child in [node.left_child, node.right_child]:
            if child:
                string += self.__str__(child)

        return string

    def size(self, node: Node = None) -> int:
        if self.root == None:
            return 0

        size = 1
        if node is None:
            node = self.root

        for child in [node.left_child, node.right_child]:
            if child:
                size += self.size(child)

        return size

if __name__ == "__main__":
    dictionary = {'a':[1,4],'b':[3,6],'c':[4,2],'d':[2,9],'e':[5,8],'f':[9,1],'g':[6,5],'h':[10,3],'i':[7,9],'j':[8,9]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    tree = KDTree(datapoints)

    print("Tree: KD tree")
    print("Input Datapoints: ")
    [print(p) for p in datapoints]

    print("The constructed tree: ")
    print(tree)
    print("Tree size:" , tree.size())

    search_area = [[3,7],[2,9]]
    print("The result when searching in area: " + str(search_area))
    found_points = tree.range_search(search_area)
    for p in found_points:
        print(p)