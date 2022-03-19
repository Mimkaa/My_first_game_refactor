import pygame as pg
vec=pg.Vector2
from collisions import ShapeOverlap_SAT,Polygon
from settings import *

class Point:
    def __init__(self,pos):
        self.pos=vec(pos)

class Rect_Tree:
    def __init__(self,pos,width,height):
        self.pos=vec(pos)
        self.height=height
        self.width=width
    def contains(self,pos):
        return (pos.x>self.pos.x and pos.x<self.pos.x+self.width and pos.y>self.pos.y and pos.y<self.pos.y+self.height)
    def intersects(self,range):
        return not (range.pos.x>self.pos.x+self.width or range.pos.x+range.width<self.pos.x or range.pos.y>self.pos.y+self.height or range.pos.y+range.height<self.pos.y)



class QuadTree:
    def __init__(self,boundary,capacity,rects_trees):
        self.boundary=boundary
        self.capacity=capacity
        self.points=[]
        self.divided=False
        self.rects_trees=rects_trees
        self.rects_trees.append(self)
    def insert(self,obj):


        if not self.boundary.contains(obj.pos): #not ShapeOverlap_SAT(obj.hit_poly,hit_boundary):
            return False
        elif len(self.points)<self.capacity:
            self.points.append(obj)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northwest.insert(obj):
                return True
            elif self.southwest.insert(obj):
                return True
            elif self.northeast.insert(obj):
                return True
            elif self.southeast.insert(obj):
                return True
            # additional check to insert in other trees if shape is bigger
            new_trees=[self.northwest,self.northeast,self.southeast,self.southwest]
            for tree in new_trees:
                hit_boundary = Polygon(vec(0, 0), shape='rect')
                hit_boundary.set_originals(
                    [vec(0, 0), vec(0, 0) + vec(tree.boundary.width, 0),
                     vec(0, 0) + vec(tree.boundary.width, tree.boundary.height),
                     vec(0, 0) + vec(0, tree.boundary.height)
                     ])
                hit_boundary.set_points(
                    hit_boundary.originals.copy()
                )
                hit_boundary.set_pos(tree.boundary.pos)


                if ShapeOverlap_SAT(obj.hit_poly, hit_boundary):
                    tree.points.append(obj)
    def subdivide(self):
        nw=Rect_Tree((self.boundary.pos.x,self.boundary.pos.y),self.boundary.width//2,self.boundary.height//2)
        self.northwest=QuadTree(nw,self.capacity,self.rects_trees)
        ne=Rect_Tree((self.boundary.pos.x+self.boundary.width//2,self.boundary.pos.y),self.boundary.width//2,self.boundary.height//2)
        self.northeast=QuadTree(ne,self.capacity,self.rects_trees)
        sw=Rect_Tree((self.boundary.pos.x,self.boundary.pos.y+self.boundary.height//2),self.boundary.width//2,self.boundary.height//2)
        self.southwest=QuadTree(sw,self.capacity,self.rects_trees)
        se=Rect_Tree((self.boundary.pos.x+self.boundary.width//2,self.boundary.pos.y+self.boundary.height//2),self.boundary.width//2,self.boundary.height//2)
        self.southeast=QuadTree(se,self.capacity,self.rects_trees)

        self.divided=True
    def query(self,range,found):

        if not self.boundary.intersects(range):
            return []
        else:
            for obj in self.points:

                # if range.contains(obj.pos):
                    found.append(obj)
            if self.divided:
                self.northwest.query(range,found)
                self.northeast.query(range,found)
                self.southwest.query(range,found)
                self.southeast.query(range,found)
        return found


    def show(self,surf,function):
        rect=pg.Rect(self.boundary.pos.x,self.boundary.pos.y,self.boundary.width,self.boundary.height)
        pg.draw.rect(surf,WHITE,function(rect),1)
        if self.divided:
            self.northeast.show(surf,function)
            self.northwest.show(surf,function)
            self.southeast.show(surf,function)
            self.southwest.show(surf,function)
