from settings import *
import pygame as pg
from functions import image_bottom_height
from collisions import *
vec=pg.Vector2
class Player(pg.sprite.Sprite):
    def __init__(self,images,game, pos):
        self.images=images
        self.game=game
        self.image=self.images['PLAYER_STAY'][0]
        self.pos=vec(pos)
        self.rect=self.image.get_rect()

        self.rect.center=self.pos
        self.groups = game.all_sprites,game.characters
        pg.sprite.Sprite.__init__(self, self.groups)

        # self.hit_rect = pg.Rect((self.rect.left + start_width, self.rect.bottom - wall_height,
        #                          wall_width, wall_height))

        # self.hit_rect.center = self.pos

        self.create_hit_poly_rect()

        #layer
        self._layer = self.rect.bottom

        self.vel = vec(0, 0)
        self.name="YOU"
        self.name_color=PURPLE

        self.walking=False
        self.current_frame = 0
        self.last_update = 0
        self.dir_vec=vec(0,1)
        self.speed = 300
        self.time_between_frames = 100
        # animation switches
        self.gluttony=False


    def create_hit_poly_rect(self):
        start_width,wall_height, wall_width = image_bottom_height(self.image, 0.75)

        self.hit_poly = Polygon(vec(0,0),shape='rect')

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



    def get_keys(self):
        self.vel = vec(0, 0)
        #if not self.eat and self.game.cutscene_manager.cut_scene==None and self.game.current_character==self.name:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
            self.dir_vec=vec(-1,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
            self.dir_vec = vec(1, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -self.speed
            self.dir_vec = vec(0, -1)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = self.speed
            self.dir_vec = vec(0, 1)
        if keys[pg.K_TAB]  :
            if not self.gluttony:
                self.gluttony=True
                self.current_frame=-1
        if keys[pg.K_RSHIFT] or keys[pg.K_LSHIFT]:
            self.speed=450
            self.time_between_frames = 70
        else:
            self.speed = 300
            self.time_between_frames = 100

    def moving_animation(self):
        if self.vel!=vec(0,0):
            self.walking=True
        else:
            self.walking=False

        now = pg.time.get_ticks()

        if now - self.last_update > self.time_between_frames:
                    self.last_update = now
                    if not self.walking:
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_STAY'])
                        if self.dir_vec==vec(0,1):
                            self.image=self.images['PLAYER_STAY'][self.current_frame]
                            self.rect=self.image.get_rect()
                        elif self.dir_vec==vec(0,-1):
                            self.image = self.images['PLAYER_STAY_BACK'][self.current_frame]
                            self.rect = self.image.get_rect()
                        elif self.dir_vec==vec(1,0):
                            self.image = self.images['PLAYER_STAY_RIGHT'][self.current_frame]
                            self.rect = self.image.get_rect()
                        elif self.dir_vec==vec(-1,0):
                            self.image = self.images['PLAYER_STAY_LEFT'][self.current_frame]
                            self.rect = self.image.get_rect()
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_MOVE_FORWARD'])
                        if self.dir_vec==vec(0,1):
                            self.image=self.images['PLAYER_MOVE_FORWARD'][self.current_frame]
                            self.rect=self.image.get_rect()
                        elif self.dir_vec==vec(0,-1):
                            self.image = self.images['PLAYER_MOVE_BACK'][self.current_frame]
                            self.rect = self.image.get_rect()
                        elif self.dir_vec==vec(1,0):
                            self.image = self.images['PLAYER_MOVE_RIGHT'][self.current_frame]
                            self.rect = self.image.get_rect()
                        elif self.dir_vec==vec(-1,0):
                            self.image = self.images['PLAYER_MOVE_LEFT'][self.current_frame]
                            self.rect = self.image.get_rect()
        self.rect.bottom = self.hit_poly.bottom
        self.rect.centerx = self.hit_poly.centerx
        # self.rect.center=self.hit_poly.pos




    def gluttony_animation(self):
        now = pg.time.get_ticks()


        if self.dir_vec==vec(0,1):
            if now - self.last_update >self.time_between_frames:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_GLATTONY_FORWARD_ANIMATION'])
                        self.image =self.images['PLAYER_GLATTONY_FORWARD_ANIMATION'][self.current_frame]
                        self.rect=self.image.get_rect()

            if self.current_frame== len(self.images['PLAYER_GLATTONY_FORWARD_ANIMATION'])-2:
                self.rect.center=self.hit_poly.center
            else:
                self.rect.bottom = self.hit_poly.bottom
                self.rect.centerx = self.hit_poly.centerx

            if self.current_frame==len(self.images['PLAYER_GLATTONY_FORWARD_ANIMATION'])-1:
                self.gluttony=not self.gluttony
        elif self.dir_vec==vec(0,-1):
            if now - self.last_update >self.time_between_frames:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_GLATTONY_BACKWARD_ANIMATION'])
                        self.image =self.images['PLAYER_GLATTONY_BACKWARD_ANIMATION'][self.current_frame]
                        self.rect=self.image.get_rect()


            self.rect.bottom = self.hit_poly.bottom
            self.rect.centerx = self.hit_poly.centerx

            if self.current_frame==len(self.images['PLAYER_GLATTONY_BACKWARD_ANIMATION'])-1:
                self.gluttony=not self.gluttony
        elif self.dir_vec==vec(-1,0):
            if now - self.last_update >self.time_between_frames:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_GLATTONY_LEFT_ANIMATION'])
                        self.image =self.images['PLAYER_GLATTONY_LEFT_ANIMATION'][self.current_frame]
                        self.rect=self.image.get_rect()

            if self.current_frame == len(self.images['PLAYER_GLATTONY_LEFT_ANIMATION']) - 2:
                self.rect.bottom = self.hit_poly.bottom
                self.rect.right = self.hit_poly.right
            else:
                self.rect.bottom = self.hit_poly.bottom
                self.rect.centerx = self.hit_poly.centerx

            if self.current_frame==len(self.images['PLAYER_GLATTONY_LEFT_ANIMATION'])-1:
                self.gluttony=not self.gluttony

        elif self.dir_vec==vec(1,0):
            if now - self.last_update >self.time_between_frames:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.images['PLAYER_GLATTONY_RIGHT_ANIMATION'])
                        self.image =self.images['PLAYER_GLATTONY_RIGHT_ANIMATION'][self.current_frame]
                        self.rect=self.image.get_rect()

            if self.current_frame == len(self.images['PLAYER_GLATTONY_RIGHT_ANIMATION']) - 2:
                self.rect.bottom = self.hit_poly.bottom
                self.rect.left = self.hit_poly.left
            else:
                self.rect.bottom = self.hit_poly.bottom
                self.rect.centerx = self.hit_poly.centerx

            if self.current_frame==len(self.images['PLAYER_GLATTONY_RIGHT_ANIMATION'])-1:
                self.gluttony=not self.gluttony


    def collisions(self,group):

        for spr in group:

            ShapeOverlap_DIAG_STATIC(self.hit_poly,spr.hit_poly)
            #ShapeOverlap_SAT_STATIC(self.hit_poly,spr.hit_poly)

        self.pos = self.hit_poly.pos
        self.hit_poly.set_pos(self.pos)



    def animate(self):
        if self.gluttony:
           self.gluttony_animation()
        else:
            self.moving_animation()

    def adjust(self):
        self.pos = self.hit_poly.pos
        self.hit_poly.set_pos(self.pos)
        self.animate()

    def update(self):
        self.get_keys()

        self.pos+=self.vel*self.game.dt
        self.hit_poly.set_pos(self.pos)

        # animations
        self.animate()









class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, pos,w,h):
        self.groups =  game.walls
        self.width=w
        self.height=h
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos=vec(pos)
        self.create_hit_poly_rect(w,h)


    def create_hit_poly_rect(self,w,h):
        wall_width, wall_height = w,h

        self.hit_poly = Polygon(vec(0,0),shape='rect')

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


