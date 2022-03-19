import pygame as pg
from settings import *
import random
import math
from os import path
vec=pg.Vector2
class Particle:
    def __init__(self,pos,image):
        self.pos=vec(pos)
        angle=random.uniform(0,math.pi*2)
        self.vel=vec(math.cos(angle),math.sin(angle))
        self.vel*=random.uniform(0.5,2)
        self.acc=vec(0,0)
        self.r=16
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
        self.lifetime -= 20

        self.acc=vec(0,0)
    def boundaries(self):
        if self.pos.y>=HEIGHT-self.r*2:
            self.vel*=-1
            self.pos.y=HEIGHT-self.r*2
    def show(self,surf):
        surf_circle=pg.Surface((self.r*2,self.r*2),pg.SRCALPHA)
        surf_circle2 = pg.Surface((self.r * 3, self.r * 3), pg.SRCALPHA)
        pg.draw.circle(surf_circle2,(45,5,70),(self.r*1.5,self.r*1.5),self.r*1.5)

        self.image=pg.transform.scale(self.image_or,(self.r*2,self.r*2))

        surf_circle.blit(self.image,(0,0))
        surf_circle.set_alpha(self.lifetime)

        surf_circle2.blit(surf_circle,(self.r*0.5,self.r*0.5))
        surf.blit(surf_circle2,(self.pos.x-self.r,self.pos.y-self.r),special_flags = pg.BLEND_RGBA_ADD)#,special_flags = pg.BLEND_RGBA_ADD


class Flow:
    def __init__(self):
        game_folder = path.dirname(__file__)
        self.image= pg.image.load(path.join(game_folder,'light32.png')).convert_alpha()
        self.particles=[]
    def applyForce(self,force):
        for p in self.particles:
            p.applyForce(force)
    def emit(self,pos):
        self.particles += [Particle(pos,self.image) for i in range(3)]
        for n,p in enumerate(self.particles):
            p.update()
            #p.boundaries()
            if p.finished():
                self.particles.pop(n)
    def show(self,surf):
        for p in self.particles:
            p.show(surf)