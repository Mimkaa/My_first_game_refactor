import pygame as pg
from functions import image_bottom_height
from collisions import Polygon,ShapeOverlap_DIAG_STATIC
vec=pg.Vector2
class Parent_Decoration(pg.sprite.Sprite):
    def __init__(self,images,pos,game,groups,having_bottom=None):
        self.groups=game.decorations,groups
        super().__init__(self.groups)
        self.pos=vec(pos)
        self.game=game
        self.images=images
        self.rect=self.images[0].get_rect()
        self.current_frame = 0
        self.last_update = 0
        self._layer =self.rect.bottom



        if having_bottom:
            # start_width, wall_height, wall_width = image_bottom_height(self.images[0],having_bottom)
            # self.hit_rect=pg.Rect(self.rect.left + start_width,self.rect.bottom - wall_height,wall_width,wall_height)
            self.create_hit_poly_rect(having_bottom)
        else:
            self.hit_rect=self.rect.copy()

    def create_hit_poly_rect(self,percent):
        start_width, wall_height, wall_width = image_bottom_height(self.images[0], percent)

        self.hit_poly = Polygon(vec(0, 0), shape='rect')

        self.hit_poly.set_originals(
            [vec(-wall_width / 2, -wall_height / 2), vec(-wall_width / 2, -wall_height / 2) + vec(wall_width, 0),
             vec(-wall_width / 2, -wall_height / 2) + vec(wall_width, wall_height),
             vec(-wall_width / 2, -wall_height / 2) + vec(0, wall_height)
             ])
        self.hit_poly.set_points(
            [vec(-wall_width / 2, -wall_height / 2), vec(-wall_width / 2, -wall_height / 2) + vec(wall_width, 0),
             vec(-wall_width / 2, -wall_height / 2) + vec(wall_width, wall_height),
             vec(-wall_width / 2, -wall_height / 2) + vec(0, wall_height)
             ])

        self.hit_poly.set_pos(self.pos)
        self.hit_poly.update()
        self.hit_poly.create_sides()


class Mashroom(Parent_Decoration):
    def __init__(self,images,game,pos):
        super().__init__(images,pos,game,game.all_sprites,having_bottom=0.6)
        self.image=self.images[0]

    def update(self):
        self.hit_poly.set_pos(self.pos)
        self.animate()

    def animate(self):
        now=pg.time.get_ticks()
        if now-self.last_update>2000:
            self.last_update=now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.rect=self.image.get_rect()
        self.rect.bottom = self.hit_poly.bottom
        self.rect.centerx = self.hit_poly.centerx