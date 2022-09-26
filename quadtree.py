from tools import *
        
class QuadTree:
    
    def __init__(self, boundary: Rect, datapoints: Datapoint = None, max_points=4, depth=0):
       
        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.depth = depth
        
        self.divided = False

        if datapoints:
            for point in datapoints:
                self.insert(point)

    def divide(self):
        
        cx, cy = self.boundary.cx, self.boundary.cy
        w, h = self.boundary.w / 2, self.boundary.h / 2
        
        self.nw = QuadTree(Rect(cx - w/2, cy - h/2, w, h),
            max_points = self.max_points, depth = self.depth + 1)
        self.ne = QuadTree(Rect(cx + w/2, cy - h/2, w, h),
            max_points = self.max_points, depth = self.depth + 1)
        self.se = QuadTree(Rect(cx + w/2, cy + h/2, w, h),
            max_points = self.max_points, depth = self.depth + 1)
        self.sw = QuadTree(Rect(cx - w/2, cy + h/2, w, h),
            max_points = self.max_points, depth = self.depth + 1)
        self.divided = True

    def insert(self, point):
        
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.max_points:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        return (self.ne.insert(point) or
                self.nw.insert(point) or
                self.se.insert(point) or
                self.sw.insert(point))

    def range_search(self, boundary, found_points=None):

        if not found_points:
            found_points = []

        if not self.boundary.intersects(boundary): 
            return False

        for point in self.points:
            if boundary.contains(point):
                found_points.append(point)
        
        if self.divided:
            self.nw.range_search(boundary, found_points)
            self.ne.range_search(boundary, found_points)
            self.se.range_search(boundary, found_points)
            self.sw.range_search(boundary, found_points)
        return found_points
    
    def __str__(self):
       
        sp = ' ' * self.depth * 2
        s = str(self.boundary) + '\n'
        s += sp + ', '.join(str(point) for point in self.points)
        if not self.divided:
            return s
        return s + '\n' + '\n'.join([
                sp + 'nw: ' + str(self.nw), sp + 'ne: ' + str(self.ne),
                sp + 'se: ' + str(self.se), sp + 'sw: ' + str(self.sw)])

    def size(self):
        size = 0
        if not self.divided:
            return 1

        for child in [self.nw, self.ne, self.se, self.sw]:
            size += child.size()

        return size

if __name__ == "__main__":
    dictionary = {'a':[1,4],'b':[3,6],'c':[4,2],'d':[2,9],'e':[5,8],'f':[9,1],'g':[6,5],'h':[10,3],'i':[7,9],'j':[8,9]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    mbr = calc_mbr(datapoints)
    boundary = Rect(math.ceil(mbr[0][1]/2), math.ceil(mbr[1][1]/2), mbr[0][1]-mbr[0][0]+1, mbr[1][1]-mbr[1][0]+1)
    tree = QuadTree(boundary, datapoints)
    # f_points = []
    f_points = tree.range_search(boundary)
    for p in f_points:
        print(p)