import pygame as pg
from settings import *
import pytmx


#class Map:
    #def __init__(self, filename):
        #self.data = []
        #with open(filename, 'rt') as f:
            #for line in f:
                #self.data.append(line.strip())

        #self.tilewidth = len(self.data[0])
        #self.tileheight = len(self.data)
        #self.width = self.tilewidth * TILESIZE
        #self.height = self.tileheight * TILESIZE


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
        self.pos1=0
        self.pos2=0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    def apply_for_water(self,entity):
        return entity.rect.move(self.camera.x,self.camera.y+entity.rect.height)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.hit_rect.centerx + int(WIDTH / 2)
        y = -target.hit_rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)



    def update_for_water(self,target):
        x = -target.rect.left
        y = -target.rect.top
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)





