import pygame as pg
vec=pg.Vector2
class Edge:
    def __init__(self,sx,sy,ex,ey):
        self.sx=sx
        self.sy=sy
        self.ex=ex
        self.ey=ey
    def __repr__(self):
        return f"start:{(self.sx,self.sy)},end:{(self.ex,self.ey)}"
class Cell:
    def __init__(self):
        self.edge_id=[]
        self.edge_exists=[]
        self.exists=False


class Triangle:
    def __init__(self,vectors):
        self.vectors=[vec(vector) for vector in vectors]


