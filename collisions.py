import pygame as pg
from settings import *
import math
import pickle
vec=pg.Vector2

class Polygon:
    def __init__(self,pos,shape='poly'):
        self.points=[]
        self.pos=vec(pos)
        self.angle=0
        self.originals=[]
        self.overlap=False
        self.shape='rect'

    def create_sides(self):
        self.topleft=self.points[0]
        self.topright=self.points[1]
        self.bottomleft=self.points[2]
        self.bottomright=self.points[3]
        self.top=self.points[0].y
        self.left=self.points[0].x
        self.right=self.points[0].x+self.topright.x-self.topleft.x
        self.bottom=self.points[0].y+self.bottomleft.y-self.topleft.y
        self.centerx=self.points[0].x+(self.topright.x-self.topleft.x)/2
        self.centery = self.points[0].y+(self.bottomleft.y-self.topleft.y) / 2
        self.width=self.topright.x-self.topleft.x
        self.height=self.bottomleft.y-self.topleft.y
        self.center=vec(self.points[0].x+(self.topright.x-self.topleft.x)/2,self.points[0].y+(self.bottomleft.y-self.topleft.y) / 2)

    def rotate(self,angle):
        self.angle+=angle
    def set_originals(self,orig):
        if not self.originals:
            self.originals=orig
    def set_points(self,points):
        if not self.points:
            self.points=points

    def move(self,dir):
        vel=vec(math.cos(self.angle),math.sin(self.angle)).normalize()
        vel.scale_to_length(dir)
        self.pos+=vel
    def set_pos(self,pos):
        self.pos=pos
        self.update()


    def update(self):

        for n,point in enumerate(self.points):
            self.points[n].x=(self.originals[n].x*math.cos(self.angle)-self.originals[n].y*math.sin(self.angle))+self.pos.x
            self.points[n].y=(self.originals[n].x*math.sin(self.angle)+self.originals[n].y*math.cos(self.angle))+self.pos.y
        if self.shape=='rect':
            self.create_sides()
    # def copy2(self):
    #     pol=Polygon(self.pos)
    #     pol.angle=self.angle
    #     pol.points=self.points.copy()
    #     pol.originals=self.originals.copy()
    #     pol.overlap=False
    #     return pol

    def copy(self):
        copy= pickle.loads(pickle.dumps(self))
        return copy



def ShapeOverlap_DIAG_STATIC(polyy1, polyy2):
    poly1 = polyy1
    poly2 = polyy2

    for shape in range(2):
        if shape == 1:
            # poly1,poly2=poly2,poly1
            poly2 = polyy1
            poly1 = polyy2
        # check diagonals of polygon

        for p in range(len(poly1.points)):
            line_p1s = poly1.pos
            line_p1e = poly1.points[p]

            # in case the poly is not rotated rect
            if len(polyy1.points) == 4 and len(polyy2.points) == 4:
                top = (polyy1.originals[0] + polyy1.originals[1]) / 2
                top2 = (polyy2.originals[0] + polyy2.originals[1]) / 2
                if math.degrees(math.atan2(top.x, top.y)) == 180 and math.degrees(
                        math.atan2(top2.x, top2.y)) == 180 and shape == 0:
                    line_p1s = poly1.pos
                    line_p1e = (poly1.points[p] + poly1.points[(p + 1) % len(poly1.points)]) / 2

            displacement = vec(0, 0)

            # against edges of the other
            for q in range(len(poly2.points)):

                line_p2s = poly2.points[q]
                line_p2e = poly2.points[(q + 1) % len(poly2.points)]

                # line segment intersection
                d = (line_p2e.x - line_p2s.x) * (line_p1s.y - line_p1e.y) - (line_p1s.x - line_p1e.x) * (
                            line_p2e.y - line_p2s.y)
                if d != 0:
                    t1 = ((line_p2s.y - line_p2e.y) * (line_p1s.x - line_p2s.x) + (line_p2e.x - line_p2s.x) * (
                                line_p1s.y - line_p2s.y)) / d
                    t2 = ((line_p1s.y - line_p1e.y) * (line_p1s.x - line_p2s.x) + (line_p1e.x - line_p1s.x) * (
                                line_p1s.y - line_p2s.y)) / d

                    if t1 >= 0 and t1 < 1. and t2 >= 0. and t2 < 1.:
                        to_add = vec((1 - t1) * (line_p1e.x - line_p1s.x), (1 - t1) * (line_p1e.y - line_p1s.y))
                        displacement += to_add

            if shape == 0:

                polyy1.pos += displacement * -1
                polyy1.update()

            else:

                polyy1.pos += displacement
                polyy1.update()

def ShapeOverlap_DIAG(polyy1,polyy2):
    poly1=polyy1
    poly2=polyy2
    for shape in range(2):
        if shape==1:
            poly2 = polyy1
            poly1 = polyy2
        # check diagonals of polygon
        for p in range(len(poly1.points)):
            line_p1s=poly1.pos
            line_p1e=poly1.points[p]
            # against edges of the other
            for q in range(len(poly2.points)):
                line_p2s=poly2.points[q]
                line_p2e=poly2.points[(q+1)%len(poly2.points)]

                # line segment intersection
                d = (line_p2e.x - line_p2s.x) * (line_p1s.y - line_p1e.y) - (line_p1s.x - line_p1e.x) * (line_p2e.y - line_p2s.y)
                if d!=0:
                    t1 = ((line_p2s.y - line_p2e.y) * (line_p1s.x - line_p2s.x) + (line_p2e.x - line_p2s.x) * (line_p1s.y - line_p2s.y)) / d
                    t2 = ((line_p1s.y - line_p1e.y) * (line_p1s.x - line_p2s.x) + (line_p1e.x - line_p1s.x) * (line_p1s.y - line_p2s.y)) / d

                    if t1 >= 0 and t1 < 1. and t2 >= 0. and t2 < 1.:
                        return True

    return False

def ShapeOverlap_SAT(polyy1,polyy2):
    poly1=polyy1
    poly2=polyy2

    for shape in range(2):
        if shape==1:
            poly1=polyy2
            poly2=polyy1
        for edge in range(len(poly1.points)):
            b=(edge+1)%len(poly1.points)
            # a fancy way of getting a normal to an edge
            axisProj=vec(-(poly1.points[b].y-poly1.points[edge].y),(poly1.points[b].x-poly1.points[edge].x))

            # work out min and max 1D points poly1
            min_poly1=float('inf')
            max_poly1=float('-inf')
            for p in range(len(poly1.points)):
                dot=(poly1.points[p].x*axisProj.x+poly1.points[p].y*axisProj.y)

                min_poly1=min(min_poly1,dot)
                max_poly1=max(max_poly1,dot)

            # work out min and max 1D points poly2
            min_poly2=float('inf')
            max_poly2=float('-inf')
            for p in range(len(poly2.points)):
                dot=(poly2.points[p].x*axisProj.x+poly2.points[p].y*axisProj.y)
                min_poly2=min(min_poly2,dot)
                max_poly2=max(max_poly2,dot)

            if not (max_poly2>=min_poly1 and max_poly1>=min_poly2):
                return False


    return True



def ShapeOverlap_SAT_STATIC(polyy1,polyy2):
    poly1=polyy1
    poly2=polyy2
    overlap=float('inf')
    for shape in range(2):
        if shape==1:
            poly1,poly2=poly2,poly1
        for edge in range(len(poly1.points)):
            b=(edge+1)%len(poly1.points)
            # a fancy way of getting a normal to an edge
            axisProj=vec(-(poly1.points[b].y-poly1.points[edge].y),(poly1.points[b].x-poly1.points[edge].x))
            axisProj=axisProj.normalize()
            # work out min and max 1D points poly1
            min_poly1=float('inf')
            max_poly1=float('-inf')
            for p in range(len(poly1.points)):
                dot=(poly1.points[p].x*axisProj.x+poly1.points[p].y*axisProj.y)

                min_poly1=min(min_poly1,dot)
                max_poly1=max(max_poly1,dot)

            # work out min and max 1D points poly2
            min_poly2=float('inf')
            max_poly2=float('-inf')
            for p in range(len(poly2.points)):
                dot=(poly2.points[p].x*axisProj.x+poly2.points[p].y*axisProj.y)
                min_poly2=min(min_poly2,dot)
                max_poly2=max(max_poly2,dot)
            # calculate the overlap
            overlap=min(min(max_poly1,max_poly2)-max(min_poly1,min_poly2),overlap)

            if not (max_poly2>=min_poly1 and max_poly1>=min_poly2):
                return False
    # if we got here objects overlapped
    # and we will displace poly1 along the vector between their centers
    d=polyy2.pos-polyy1.pos
    d=d.normalize()
    polyy1.pos-=d*overlap

    return False