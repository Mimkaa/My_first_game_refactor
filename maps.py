import pytmx
import pygame as pg
from os import path
from sprites import *
from decorations import *
from settings import *
from functions import load_animation
vec=pg.Vector2
class TiledMap:
    def __init__(self,filename):
        tm=pytmx.load_pygame(filename,pixelalpha=True)
        self.width=tm.width*tm.tilewidth
        self.height=tm.height*tm.tileheight
        self.tmxdata=tm
        self.filename=filename
    def render(self,surface):
        # find the image for each number
        ti=self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile=ti(gid)
                    if tile:
                        surface.blit(tile,(x*self.tmxdata.tilewidth,y*self.tmxdata.tileheight))
    def make_map(self):
        temp_surface=pg.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface
    def __repr__(self):
        return f'{self.filename}'


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, height, width)
        self.width = width
        self.height = height
        self.prev_pos=vec(0,0)




    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_for_water(self,entity):
        return entity.rect.move(self.camera.x,self.camera.y+entity.rect.height)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    def apply_hit_poly(self,poly,start_pos):
        shape = poly.copy()
        shape.set_pos(shape.pos - vec(start_pos) + self.prev_pos)
        return shape

    def update(self,target):
        x = -target.hit_poly.pos.x + int(WIDTH / 2)
        y = -target.hit_poly.pos.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.prev_pos=vec(x,y)



    def update_for_water(self,target):
        x = -target.rect.left
        y = -target.rect.top
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)


class Map:
    def __init__(self,folder,names):
        self.map_names = names
        self.current_map=0
        self.folder=folder
    def create_map(self):
        self.map_data = TiledMap(path.join(self.folder, self.map_names[self.current_map]))
        self.image=self.map_data.make_map()
        self.rect=self.image.get_rect()
        self.camera=Camera(self.rect.width,self.rect.height)

    def change_forward(self):
        self.current_map+=1%len(self.map_names)
    def change_backward(self):
        self.current_map-=1
    def draw_map(self,surf):
        surf.blit(self.image, self.camera.apply_rect(self.rect))

    def create_objects(self,game):
        for tile_object in self.map_data.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name=='player':
                dict_images={'PLAYER_STAY' :load_animation('re_player',['front_idle_animation1.png', 'front_idle_animation2.png', 'front_idle_animation3.png',
                               'front_idle_animation4.png', 'front_idle_animation5.png'],resize=(3,3)),
                'PLAYER_MOVE_FORWARD' :load_animation('re_player',['interpolation_for_going_forward_animetion.png', 'front_going_animation1.png',
                                       'front_going_animation2.png', 'front_idle_animation3.png',
                                       'front_going_animation3.png', "front_going_animation4.png"],resize=(3,3)),
                'PLAYER_MOVE_BACK' :load_animation('re_player',['interpolation_for_going_backward_animetion.png', 'back_going_animation1.png',
                                    'back_going_animation2.png', 'back_idle_animation3.png',
                                    'back_going_animation3.png', "back_going_animation4.png"],resize=(3,3)),
                'PLAYER_MOVE_LEFT' :load_animation('re_player',['left_idle_animation3.png', 'left_going_animation1.png',
                                    'left_going_animation2.png', 'left_idle_animation3.png',
                                    'left_going_animation3.png', 'left_going_animation4.png'],resize=(3,3)),
                'PLAYER_MOVE_RIGHT': load_animation('re_player', ['left_idle_animation3.png',
                                                              'left_going_animation1.png',
                                                              'left_going_animation2.png',
                                                              'left_idle_animation3.png',
                                                              'left_going_animation3.png',
                                                              'left_going_animation4.png'],
                                                resize=(3, 3),flip=True),
                'PLAYER_STAY_BACK' :load_animation('re_player',['back_idle_animation1.png', 'back_idle_animation2.png', 'back_idle_animation3.png',
                                    'back_idle_animation4.png', 'back_idle_animation5.png'],resize=(3,3)),
                'PLAYER_STAY_LEFT' :load_animation('re_player' ,['left_idle_animation1.png', 'left_idle_animation2.png', 'left_idle_animation3.png',
                                    'left_idle_animation4.png', 'left_idle_animation5.png'],resize=(3,3)),
                'PLAYER_STAY_RIGHT': load_animation('re_player',
                                        ['left_idle_animation1.png', 'left_idle_animation2.png',
                                         'left_idle_animation3.png',
                                         'left_idle_animation4.png',
                                         'left_idle_animation5.png'], resize=(3, 3),flip=True),

                'PLAYER_GLATTONY_FORWARD_ANIMATION' : load_animation('player',['glattony_forward1.png', 'glattony_forward2.png',
                                                                  'glattony_forward3.png', 'glattony_forward4.png',
                                                                  'glattony_forward5.png'], resize=(0.9, 0.9)),
                'PLAYER_GLATTONY_BACKWARD_ANIMATION' : load_animation('player',['standing_back1.png', 'standing_back2.png',
                                                      'glattony_backward1.png', 'glattony_backward2.png',
                                                      'glattony_backward3.png'], resize=(0.9, 0.9)),
                'PLAYER_GLATTONY_RIGHT_ANIMATION' : load_animation('player',['glattony_right1.png', 'glattony_right2.png', 'glattony_right3.png',
                                                   'glattony_right4.png', 'glattony_right5.png'], resize=(0.9, 0.9)),

                'PLAYER_GLATTONY_LEFT_ANIMATION': load_animation('player', ['glattony_right1.png',
                                                                      'glattony_right2.png',
                                                                      'glattony_right3.png',
                                                                      'glattony_right4.png',
                                                                      'glattony_right5.png'],
                                                           resize=(0.9, 0.9),flip=True)

                }

                self.player=Player(dict_images,game,obj_center)

            if tile_object.name=="mashroom":
                Mashroom(load_animation("vegetation",['mashroom1.png', 'mashroom2.png', 'mashroom3.png']),game,obj_center)
            if tile_object.name=='wall':
                Obstacle(game,obj_center,tile_object.width,tile_object.height)

    def camera_update(self,target):

        self.camera.update(target)





