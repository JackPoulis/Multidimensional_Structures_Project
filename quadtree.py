from tools import *
import numpy as np
    
class Rect:

    def __init__(self, cx, cy, w, h):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.west_edge, self.east_edge = cx - w/2, cx + w/2
        self.north_edge, self.south_edge = cy - h/2, cy + h/2

    def __str__(self):
        return '({:.2f}, {:.2f}, {:.2f}, {:.2f})'.format(self.west_edge,
                    self.north_edge, self.east_edge, self.south_edge)

    def contains(self, point):
        
        try:
            point_x, point_y = point.vector[0], point.vector[1]
        except AttributeError:
            point_x, point_y = point

        return (point_x >= self.west_edge and
                point_x < self.east_edge and
                point_y >= self.north_edge and
                point_y < self.south_edge)

    def intersects(self, other):
        
        return not (other.west_edge > self.east_edge or
                    other.east_edge < self.west_edge or
                    other.north_edge > self.south_edge or
                    other.south_edge < self.north_edge)

    def draw(self, ax, c='k', lw=1, **kwargs):
        x1, y1 = self.west_edge, self.north_edge
        x2, y2 = self.east_edge, self.south_edge
        ax.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)    
        
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

    def __str__(self):
       
        sp = ' ' * self.depth * 2
        s = str(self.boundary) + '\n'
        s += sp + ', '.join(str(point) for point in self.points)
        if not self.divided:
            return s
        return s + '\n' + '\n'.join([
                sp + 'nw: ' + str(self.nw), sp + 'ne: ' + str(self.ne),
                sp + 'se: ' + str(self.se), sp + 'sw: ' + str(self.sw)])

    def divide(self):
        
        cx, cy = self.boundary.cx, self.boundary.cy
        w, h = self.boundary.w / 2, self.boundary.h / 2
        
        self.nw = QuadTree(Rect(cx - w/2, cy - h/2, w, h),
                                    self.max_points, self.depth + 1)
        self.ne = QuadTree(Rect(cx + w/2, cy - h/2, w, h),
                                    self.max_points, self.depth + 1)
        self.se = QuadTree(Rect(cx + w/2, cy + h/2, w, h),
                                    self.max_points, self.depth + 1)
        self.sw = QuadTree(Rect(cx - w/2, cy + h/2, w, h),
                                    self.max_points, self.depth + 1)
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

    def query(self, boundary, found_points):
       
        if not self.boundary.intersects(boundary): 
            return False

        for point in self.points:
            if boundary.contains(point):
                found_points.append(point)
        
        if self.divided:
            self.nw.query(boundary, found_points)
            self.ne.query(boundary, found_points)
            self.se.query(boundary, found_points)
            self.sw.query(boundary, found_points)
        return found_points
    
if __name__ == "__main__":
    dictionary = {'a':[1,1],'b':[2,4],'c':[3,1],'d':[4,3],'e':[5,6],'f':[6,5]}
    datapoints = [Datapoint(d[1],d[0]) for d in dictionary.items()]
    bound = Rect(0,0,10,10)
    tree = QuadTree(bound, datapoints)
    print(tree)