import pygame as pg
from settings import *
import random
import math
from os import path
vec=pg.Vector2

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Particle:
    def __init__(self,pos,image) :
        self.pos=vec(pos)
        angle=random.uniform(0,math.pi*2)
        self.vel=vec(math.cos(angle),math.sin(angle))
        self.vel*=random.uniform(0.5,2)
        self.acc=vec(0,0)
        self.r=8
        self.lifetime=255
        self.image=image
        self.image_or=image
    def applyForce(self,force):
        self.acc+=force

    def finished(self):
        return self.lifetime<=0



    def update(self):
        self.vel+=self.acc
        self.pos+=self.vel
        self.lifetime -= 15

        self.acc=vec(0,0)
    def boundaries(self):
        if self.pos.y>=HEIGHT-self.r*2:
            self.vel*=-1
            self.pos.y=HEIGHT-self.r*2
    def show(self,surf):
        surf_circle=pg.Surface((self.r*2,self.r*2),pg.SRCALPHA)
        surf_circle2 = pg.Surface((self.r * 3, self.r * 3), pg.SRCALPHA)
        pg.draw.circle(surf_circle2,(1,50,80),(self.r*1.5,self.r*1.5),self.r*1.5)

        self.image=pg.transform.scale(self.image_or,(self.r*2,self.r*2))

        surf_circle.blit(self.image,(0,0))
        surf_circle.set_alpha(self.lifetime)

        surf_circle2.blit(surf_circle,(self.r*0.5,self.r*0.5))
        surf.blit(surf_circle2,(self.pos.x-self.r,self.pos.y-self.r),special_flags = pg.BLEND_RGBA_ADD)#,special_flags = pg.BLEND_RGBA_ADD


class Flow:
    def __init__(self):
        game_folder=path.dirname(__file__)
        self.image= pg.image.load(path.join(game_folder,'light32.png')).convert_alpha()
        self.particles=[]
        self.p_pos=(0,0)
        self.max_y=0
        self.max_x = 0
    def applyForce(self,force):
        for p in self.particles:
            p.applyForce(force)
    def emit(self):
        self.particles += [Particle((self.max_x/2+8,17),self.image) for i in range(5)]
        for n,p in enumerate(self.particles):
            p.update()
            #p.boundaries()
            if p.finished():
                if self.max_y<p.pos.y:
                    self.max_y=p.pos.y+16
                if self.max_x<p.pos.x:
                    self.max_x=p.pos.x+16
                self.particles.pop(n)
    def render(self):
        # coords_x=[c.pos.x for c in self.particles]
        # coords_y = [c.pos.y for c in self.particles]
        # minx=min(coords_x)
        # miny=min(coords_y)
        # maxx = max(coords_x)
        # maxy = max(coords_y)
        # self.max_x=maxx-minx+64
        # self.max_y = maxy - miny+64
        surface_render=pg.Surface((self.max_x+32,self.max_y+16),pg.SRCALPHA)
        for p in self.particles:
            p.show(surface_render)
        return surface_render