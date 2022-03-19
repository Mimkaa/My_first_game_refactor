import pygame as pg
import sys
from .settings import *
from .objects import *
from math import atan2,cos,sin
import numpy
from PIL import Image
from pygame.locals import *
from os import path
import numpy
from PIL import Image, ImageDraw
import math
import PIL
import base64
from io import BytesIO
import ast

import dill
import pickle

def encode(data):

        for key,val in data.items():
            if val.__class__.__name__=="Surface":
                raw_str = pg.image.tostring(val, "RGBA", False)
                img = PIL.Image.frombytes("RGBA",val.get_size(), raw_str)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue())
                data[key]=img_str
            elif type(val).__module__ != object.__module__:
                data[key]=pickle.dumps(val)

            if type(val)==list:
                if len(val)>0 and type(val[0]).__module__ != object.__module__:
                    new_list=[pickle.dumps(el) for el in val]
                    data[key]=new_list
        return data


def complete_rewrite_encode(dictt):
    for key,val in dictt.items():
                for dict in val:
                    for key,val in dict.items():
                        dict[key]=encode(val)

    with open(path.join(path.dirname(__file__), 'data.txt'), 'w') as f:
                f.write(str(dictt)+'\n')



def decode():
    with open(path.join(path.dirname(__file__), 'data.txt'), 'r') as f:
                strr=f.read()
                dictt=ast.literal_eval(strr)
    # decoding pickle
    for key,val in dictt.items():
        for pos_dict in val:
            for key0,val0 in pos_dict.items():
                for key1,val1 in val0.items():

                    if type(val1)==bytes and dill.pickles(val1) :
                        try:
                            val0[key1]=pickle.loads(val1)
                        except :
                            pass

                    if type(val1)==list and len(val1)>0 and type(val1[0])==bytes and dill.pickles(val1[0]):
                        new_listt=[pickle.loads(el) for el in val1]
                        val0[key1]=new_listt

    # decode images from base64
    for key,val in dictt.items():
        for pos_dict in val:
            for key0,val0 in pos_dict.items():
                for key1,val1 in val0.items():
                    if type(val1)==bytes:
                        im_bytes = base64.b64decode(val1)   # im_bytes is a binary image
                        im_file = BytesIO(im_bytes)  # convert image to file-like object
                        img = Image.open(im_file)   # img is now PIL Image object
                        pg_image=pg.image.fromstring(img.tobytes(), img.size, "RGBA")
                        val0[key1]=pg_image

    return dictt




class ShadowCasting:
    # def __init__(self,image_width_in_tiles,image_height_in_tiles,dist_x,dist_y,mode=0):
    #     self.light_on=False
    #     self.fancy_mode=False
    #     self.mode_i_will_use_for_the_game=False
    #     self.width=image_width_in_tiles*TILESIZE
    #     self.height=image_height_in_tiles*TILESIZE
    #     self.dist_from_coords_beginning = [dist_x - self.width//2, dist_y-self.height//2]
    #     if mode==1:
    #         self.fancy_mode=True
    #     elif mode==2:
    #         self.mode_i_will_use_for_the_game=True
    #     elif mode==0:
    #         pass
    #     self.light_radius=200
    #     self.number_circles=40
    #     self.moving=False
    #     # for vertices moving
    #     self.move_these=[]
    #
    #     # cache
    #     self.cache={}
    #
    #     self.world=[Cell() for i in range(image_width_in_tiles*image_height_in_tiles)]
    #     self.vecEdges=[]
    #     self.vecVisibilityPolygonPoints=[]
    #     self.list_triangles=[]
    #     self.image=pg.Surface((image_width_in_tiles*TILESIZE,image_height_in_tiles*TILESIZE),pg.SRCALPHA)
    #     self.rect=self.image.get_rect()
    #     self.allows_events=True
    #     self.pos_fixed=[]
    #     self.draw_rects=True
    def __init__(self,mode=0,**dict):
        self.__dict__.update(dict)
        if mode==1:
            self.fancy_mode=True
        elif mode==2:
            self.mode_i_will_use_for_the_game=True
        elif mode==0:
            pass




    def ConvertTileMapToMapOfPolygons(self,sx,sy,w,h):
        width=self.width//TILESIZE
        # cleaning everything up
        self.vecEdges.clear()
        for x in range(w):
            for y in range(h):
                self.world[(y+sy)*width+(x+sx)].edge_exists=[False for i in range(4)]
                self.world[(y + sy) * width + (x + sx)].edge_id=[0 for i in range(4)]

        # iterating through the map from topleft to bottomright
        for x in range(1,w-1):
            for y in range(1,h-1):
                # convenient indices these are neighbours
                i=(y+sy)*width+(x+sx)
                n=(y+sy-1)*width+(x+sx)
                s=(y+sy+1)*width+(x+sx)
                w=(y+sy)*width+(x+sx-1)
                e = (y + sy ) * width + (x + sx +1)
                # check if cell exists
                if self.world[i].exists:
                    # if it has no western neighbour it needs a western edge
                    if not self.world[w].exists:
                        # it can extend from its northern neighbour or create a new one
                        if self.world[n].edge_exists[WEST]:
                            # extend the edge downwards
                            self.vecEdges[self.world[n].edge_id[WEST]].ey+=TILESIZE
                            self.world[i].edge_id[WEST]=self.world[n].edge_id[WEST]
                            self.world[i].edge_exists[WEST]=True
                        else:
                            # norther neighbour does not have one
                            edge=Edge((sx+x)*TILESIZE,(sy+y)*TILESIZE,(sx+x)*TILESIZE,(sy+y)*TILESIZE+TILESIZE)

                            # add the edge to the polygon pool
                            edge_id=len(self.vecEdges)
                            self.vecEdges.append(edge)

                            # Update tile information with edge information
                            self.world[i].edge_id[WEST]=edge_id
                            self.world[i].edge_exists[WEST]=True

                    # if it has no eastern neighbour it needs a eastern edge
                    if not self.world[e].exists:
                        # it can extend from its northern neighbour or create a new one
                        if self.world[n].edge_exists[EAST]:
                            # extend the edge downwards
                            self.vecEdges[self.world[n].edge_id[EAST]].ey += TILESIZE
                            self.world[i].edge_id[EAST] = self.world[n].edge_id[EAST]
                            self.world[i].edge_exists[EAST] = True
                        else:
                            # norther neighbour does not have one
                            edge = Edge((sx + x+1) * TILESIZE, (sy + y) * TILESIZE, (sx + x+1) * TILESIZE,
                                        (sy + y) * TILESIZE + TILESIZE)

                            # add the edge to the polygon pool
                            edge_id = len(self.vecEdges)
                            self.vecEdges.append(edge)

                            # Update tile information with edge information
                            self.world[i].edge_id[EAST] = edge_id
                            self.world[i].edge_exists[EAST] = True

                    # if it has no northern neighbour it needs a northern edge
                    if not self.world[n].exists:
                        # it can extend from its western neighbour or create a new one
                        if self.world[w].edge_exists[NORTH]:
                            # extend the edge eastward(right)
                            self.vecEdges[self.world[w].edge_id[NORTH]].ex += TILESIZE
                            self.world[i].edge_id[NORTH] = self.world[w].edge_id[NORTH]
                            self.world[i].edge_exists[NORTH] = True
                        else:
                            # western neighbour does not have one
                            edge = Edge((sx + x ) * TILESIZE, (sy + y) * TILESIZE, (sx + x ) * TILESIZE+ TILESIZE,
                                        (sy + y) * TILESIZE )

                            # add the edge to the polygon pool
                            edge_id = len(self.vecEdges)
                            self.vecEdges.append(edge)

                            # Update tile information with edge information
                            self.world[i].edge_id[NORTH] = edge_id
                            self.world[i].edge_exists[NORTH] = True

                    # if it has no southern neighbour it needs a southern edge
                    if not self.world[s].exists:
                        # it can extend from its western neighbour or create a new one
                        if self.world[w].edge_exists[SOUTH]:
                            # extend the edge eastward(right)
                            self.vecEdges[self.world[w].edge_id[SOUTH]].ex += TILESIZE
                            self.world[i].edge_id[SOUTH] = self.world[w].edge_id[SOUTH]
                            self.world[i].edge_exists[SOUTH] = True
                        else:
                            # western neighbour does not have one
                            edge = Edge((sx + x) * TILESIZE, (sy + y+1) * TILESIZE, (sx + x) * TILESIZE + TILESIZE,
                                        (sy + y+1) * TILESIZE)

                            # add the edge to the polygon pool
                            edge_id = len(self.vecEdges)
                            self.vecEdges.append(edge)

                            # Update tile information with edge information
                            self.world[i].edge_id[SOUTH] = edge_id
                            self.world[i].edge_exists[SOUTH] = True


    def CalculateVisibilityPolygon(self,ox,oy,radius):
        # get rid of existing polygon
        self.vecVisibilityPolygonPoints.clear()
        self.list_triangles.clear()
        # for each edge in Polygonmap
        for edge in self.vecEdges:
            # take each edge
            for i in range(2):
                if i==0:
                    rdx=edge.sx-ox
                    rdy=edge.sy-oy
                else:
                    rdx = edge.ex - ox
                    rdy = edge.ey - oy

                base_ang=atan2(rdy,rdx)

                # angle for 3 additional rays
                ang=0

                # for each point cast 3 rays (1 directly, and 2 others this a tiny angle offset)
                for j in range(3):
                    if j==0:
                        ang=base_ang-0.0001
                    if j==1:
                        ang=base_ang
                    if j==2:
                        ang=base_ang+0.0001

                    # create a ray along angle for required distance
                    rdx=radius*cos(ang)
                    rdy=radius*sin(ang)

                    min_t1=float('inf')
                    min_px,min_py,min_ang=0.,0.,0.
                    valid=False
                    # check rey intersection at all points
                    for edge2 in self.vecEdges:
                        # line(between start and the end of an edge) segment vector
                        sdx=edge2.ex-edge2.sx
                        sdy=edge2.ey-edge2.sy
                        # check if edges  do not overlap with casted rays
                        if abs(sdx-rdx)>0. and abs(sdy-rdy)>0.:
                            # t2 is normalized distance from line segment start to line segment end of intersect point
                            t2=(rdx*(edge2.sy-oy)+(rdy*(ox-edge2.sx)))/(sdx*rdy-sdy*rdx)
                            # t1 is a normalized distance from source along ray to ray length of intersect point
                            t1=(edge2.sx+sdx*t2-ox)/rdx

                            # if intersect point exists along ray ,and along line seg than point is valid
                            if (t1>0 and t2>=0 and t2<=1.):
                                if (t1<min_t1):
                                    min_t1=t1
                                    min_px=ox+rdx*t1
                                    min_py= oy + rdy * t1
                                    min_ang=atan2(min_py-oy,min_px-ox)
                                    valid=True
                    # add intersection points of visible polygon perimeter
                    if valid:
                        self.vecVisibilityPolygonPoints.append((min_ang,min_px,min_py))
        self.vecVisibilityPolygonPoints.sort(key=lambda x:x[0])






    def surf_PIL(self,surface):
        strFormat = 'RGBA'
        raw_str = pg.image.tostring(surface, strFormat, False)
        image = Image.frombytes(strFormat, surface.get_size(), raw_str)
        return image

    def PIL_surf(self,image):
        strFormat = 'RGBA'
        raw_str = image.tostring("raw", strFormat)
        surface = pg.image.fromstring(raw_str, image.size, strFormat)
        return surface

    def get_pixels_grey(self,surf):
        surf=self.surf_PIL(surf).convert('L')
        pixels=surf.getdata()
        return pixels

    def get_pixels(self,surf):
        surf=self.surf_PIL(surf)
        pixels=surf.getdata()
        return pixels

    def update(self):

        # update portion of the game loop


        if not self.pos_fixed:
            mx, my = pg.mouse.get_pos()
        else:
            mx,my=self.pos_fixed[0],self.pos_fixed[1]
        mx-=self.dist_from_coords_beginning[0]
        my-=self.dist_from_coords_beginning[1]
        # move a vertices
        if self.moving:
            for ver in self.move_these:
                if ver[1]=='start':
                    self.vecEdges[ver[0]].sx=mx
                    self.vecEdges[ver[0]].sy=my

                elif ver[1]=='end':
                    self.vecEdges[ver[0]].ex=mx
                    self.vecEdges[ver[0]].ey=my

        if self.light_on:


            self.CalculateVisibilityPolygon(mx, my, 1000.)
            # getting rid of duplicates

            for (v, v2) in zip(self.vecVisibilityPolygonPoints[::2], self.vecVisibilityPolygonPoints[1::2]):
                    if v[1]-v2[1]<0.1 and v[2]-v2[2]<0.1:
                        self.vecVisibilityPolygonPoints.pop(self.vecVisibilityPolygonPoints.index(v))

            for i in range(len(self.vecVisibilityPolygonPoints)-1):
                self.list_triangles.append(Triangle(((mx, my), (self.vecVisibilityPolygonPoints[i][1],self.vecVisibilityPolygonPoints[i][2]),(self.vecVisibilityPolygonPoints[i+1][1],self.vecVisibilityPolygonPoints[i+1][2]))))
            self.list_triangles.append(Triangle(((mx, my), (self.vecVisibilityPolygonPoints[len(self.vecVisibilityPolygonPoints) - 1][1],self.vecVisibilityPolygonPoints[len(self.vecVisibilityPolygonPoints) - 1][2]), (self.vecVisibilityPolygonPoints[0][1],self.vecVisibilityPolygonPoints[0][2]))))





    def create_cell(self):
        mx,my=pg.mouse.get_pos()
        mx -= self.dist_from_coords_beginning[0]
        my -= self.dist_from_coords_beginning[1]
        # getting coord in 1d
        index=int((my//TILESIZE)*self.width/TILESIZE+(mx//TILESIZE))

        self.world[index].exists=not self.world[index].exists


        self.ConvertTileMapToMapOfPolygons(0,0,self.width//TILESIZE,self.height//TILESIZE)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.image, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.image, LIGHTGREY, (0, y), (WIDTH, y))

    def grayscale(self, img):
        arr = pg.surfarray.array3d(img)
        # luminosity filter
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        arr = numpy.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pg.surfarray.make_surface(arr)

    def pixel(self,surface, color, pos):
        surface.fill(color, (pos, (1, 1)))



    def draw_circles(self,number,dist,decrement,alpha=255,simple=(False,0,WHITE)):


        if not simple[0]:
            start=0
            final=pg.Surface(((dist+number*dist)*2,(dist+number*dist)*2))
            for i in range(number):
                surf=pg.Surface((start*2,start*2),pg.SRCALPHA)
                pg.draw.circle(surf,(255,255,255,alpha),(start,start),start)

                start+=dist
                alpha-=decrement

                if alpha<10:
                    alpha=10
                final.blit(surf,(final.get_width()//2-start,final.get_height()//2-start))

            #self.screen.blit(final,(mx-final.get_width()//2,my-final.get_height()//2))
        else:
            final=pg.Surface((simple[1]*2,simple[1]*2),pg.SRCALPHA)
            pg.draw.circle(final,simple[2],(simple[1],simple[1]),simple[1])

        return final




    def distance(self,x1,y1,x2,y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def cut_a_polygon_out_of_surface(self,outline,surf,transparency=255):
        # read image as RGB and add alpha (transparency)
        raw_str = pg.image.tostring(surf, "RGBA", False)
        img = Image.frombytes("RGBA", surf.get_size(), raw_str)

        # convert to numpy (for convenience)
        imArray = numpy.asarray(img)

        # create mask

        polygon = outline
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
        mask = numpy.array(maskIm)

        # assemble new image (uint8: 0-255)
        newImArray = numpy.empty(imArray.shape,dtype='uint8')

        # colors (three first columns, RGB)
        newImArray[:,:,:3] = imArray[:,:,:3]

        # transparency (4th column)
        newImArray[:,:,3] = mask*transparency

        # back to Image from numpy
        newIm = Image.fromarray(newImArray, "RGBA")
        image= pg.image.fromstring(newIm.tobytes(), newIm.size, "RGBA")
        return image

    def from_1d_to_2d(self,index):
        x = index % (WIDTH//TILESIZE)
        y = index//(WIDTH//TILESIZE)
        return (x*TILESIZE,y*TILESIZE)

    def encode(self,data):
        for key,val in data.items():
            if val.__class__.__name__=="Surface":
                raw_str = pg.image.tostring(val, "RGBA", False)
                img = PIL.Image.frombytes("RGBA",val.get_size(), raw_str)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue())
                data[key]=img_str
            elif type(val).__module__ != object.__module__:
                data[key]=pickle.dumps(val)

            if type(val)==list:
                if len(val)>0 and type(val[0]).__module__ != object.__module__:
                    new_list=[pickle.dumps(el) for el in val]
                    data[key]=new_list
        return data

    def save(self,map_num,coords,data):

        try:

            with open(path.join(path.dirname(__file__), 'data.txt'), 'r') as f:
                strr=f.read()
                dictt=ast.literal_eval(strr)
            # decoding pickle
            for key,val in dictt.items():
                for pos_dict in val:
                    for key0,val0 in pos_dict.items():
                        for key1,val1 in val0.items():

                            if type(val1)==bytes and dill.pickles(val1) :
                                try:
                                    val0[key1]=pickle.loads(val1)
                                except :
                                    pass

                            if type(val1)==list and len(val1)>0 and type(val1[0])==bytes and dill.pickles(val1[0]):
                                new_listt=[pickle.loads(el) for el in val1]
                                val0[key1]=new_listt

            # decode images from base64
            for key,val in dictt.items():
                for pos_dict in val:
                    for key0,val0 in pos_dict.items():
                        for key1,val1 in val0.items():
                            if type(val1)==bytes:
                                im_bytes = base64.b64decode(val1)   # im_bytes is a binary image
                                im_file = BytesIO(im_bytes)  # convert image to file-like object
                                img = Image.open(im_file)   # img is now PIL Image object
                                pg_image=pg.image.fromstring(img.tobytes(), img.size, "RGBA")
                                val0[key1]=pg_image

            opened_data_dict=dictt


            # adding new data


            if map_num in opened_data_dict.keys():

                opened_data_dict[map_num].append({coords:data})
            else:
                opened_data_dict[map_num]=[{coords:data}]


            # encoding and saving into a txt file
            for key,val in opened_data_dict.items():
                for dict in val:
                    for key,val in dict.items():
                        dict[key]=self.encode(val)

            with open(path.join(path.dirname(__file__), 'data.txt'), 'w') as f:
                f.write(str(opened_data_dict)+'\n')


        except :
            data=self.encode(data)
            data_dict={map_num:[{coords:data}]}

            with open(path.join(path.dirname(__file__), 'data.txt'), 'w') as f:
                f.write(str(data_dict)+'\n')



    def render(self):
        self.buffLightRay=pg.Surface((WIDTH,HEIGHT))
        self.buffLightTex=pg.Surface((WIDTH,HEIGHT),pg.SRCALPHA)

        if not self.pos_fixed:
            mx, my = pg.mouse.get_pos()
        else:
            mx,my=self.pos_fixed[0],self.pos_fixed[1]

        mx -= self.dist_from_coords_beginning[0]
        my -= self.dist_from_coords_beginning[1]
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #self.draw_grid()



        self.buffLightTex.fill(BLACK)

        if self.light_on:

            # rendering a fancy effect
            if self.fancy_mode:
                cells=[]
                for n,cell in enumerate(self.world):
                    if cell.exists:
                        coords_2d=self.from_1d_to_2d(n)
                        cells.append(self.distance(coords_2d[0],coords_2d[1],mx,my))
                the_clothest_cell=min(cells)

                if the_clothest_cell<200+TILESIZE:
                    if (int(mx-self.light_radius),int(my-self.light_radius)) not in self.cache.keys():
                        self.buffLightRay.fill(BLACK)

                        for tri in self.list_triangles:
                            pg.draw.polygon(self.buffLightRay,WHITE,(tri.vectors[0],tri.vectors[1],tri.vectors[2]))
                        # create a surface with a circle
                        surf_with_circle=pg.Surface((WIDTH,HEIGHT))
                        # width and image of the light

                        pg.draw.circle(surf_with_circle,WHITE,(mx,my),self.light_radius)
                        #  step with a multiply blend mode
                        self.buffLightRay.blit(surf_with_circle,(0,0),special_flags=BLEND_MULT)
                        # getting the polygon
                        self.buffLightRay.set_colorkey(BLACK)
                        mask_circle_rays=pg.mask.from_surface(self.buffLightRay)
                        circle_rays_outline=mask_circle_rays.outline()
                        circle_rays_outline=[(i-mx+self.light_radius,j-my+self.light_radius) for i,j in circle_rays_outline]
                        outline_cropped=pg.Surface((self.light_radius*2,self.light_radius*2),pg.SRCALPHA)
                        pg.draw.polygon(outline_cropped,WHITE,circle_rays_outline)
                        light_surf=self.draw_circles(self.number_circles,self.light_radius//self.number_circles,2,alpha=80)#simple=[True,250,(255,255,255,90)]
                        final=self.cut_a_polygon_out_of_surface(circle_rays_outline,light_surf,transparency=120 )
                        #final.set_alpha(100)
                        #pg.draw.polygon(self.screen,WHITE,circle_rays_outline)
                        self.image.blit(final,(mx-self.light_radius,my-self.light_radius))
                        self.cache[(int(mx-self.light_radius),int(my-self.light_radius))]=final

                    else:
                        self.image.blit(self.cache[(mx-self.light_radius,my-self.light_radius)],(mx-self.light_radius,my-self.light_radius))
                else:
                    surf=self.draw_circles(self.number_circles,self.light_radius//self.number_circles,2,alpha=80)
                    surf.set_colorkey(BLACK)
                    self.image.blit(surf,(mx-self.light_radius,my-self.light_radius))


            elif self.mode_i_will_use_for_the_game:
                self.buffLightRay.fill(BLACK)
                for tri in self.list_triangles:
                    pg.draw.polygon(self.buffLightRay,WHITE,(tri.vectors[0],tri.vectors[1],tri.vectors[2]))
                # create a surface with a circle
                surf_with_circle=pg.Surface((WIDTH,HEIGHT))
                # width and image of the light

                pg.draw.circle(surf_with_circle,WHITE,(mx,my),self.light_radius)
                #  step with a multiply blend mode
                self.buffLightRay.blit(surf_with_circle,(0,0),special_flags=BLEND_MULT)
                # getting the polygon
                self.buffLightRay.set_colorkey(BLACK)
                mask_circle_rays=pg.mask.from_surface(self.buffLightRay)
                circle_rays_outline=mask_circle_rays.outline()

                final=pg.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
                pg.draw.polygon(final,(255,255,255,150),circle_rays_outline)
                self.image.blit(final,(0,0))



            # simple mode
            else:
                for tri in self.list_triangles:
                    pg.draw.polygon(self.image,WHITE,(tri.vectors[0],tri.vectors[1],tri.vectors[2]))







        if self.draw_rects:
            # draw edges and cells
            for x in range(self.width//TILESIZE):
                for y in range(self.height//TILESIZE):
                    if self.world[y*self.width//TILESIZE+x].exists:
                        pg.draw.rect(self.image,BLUE,(x*TILESIZE,y*TILESIZE,TILESIZE,TILESIZE))

            for v in self.vecEdges:
                pg.draw.line(self.image,RED,(v.sx,v.sy),(v.ex,v.ey),2)
                pg.draw.circle(self.image,GREEN,(v.sx,v.sy),3)
                pg.draw.circle(self.image, GREEN, (v.ex, v.ey), 3)

        return self.image



    def events(self):
        # catch all events here
        if self.allows_events:
            for event in pg.event.get():


                if event.type==pg.MOUSEBUTTONDOWN and event.button == 3 :
                    self.create_cell()
                    self.cache.clear()


                if event.type==pg.MOUSEBUTTONDOWN and event.button == 2:
                    self.mode_i_will_use_for_the_game=not self.mode_i_will_use_for_the_game

                if event.type==pg.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = pg.mouse.get_pos()
                        self.CalculateVisibilityPolygon(mx, my, 1000.)




                if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and len(self.vecVisibilityPolygonPoints)>1 and not self.light_on :

                        self.light_on=not self.light_on
                elif event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and len(self.vecVisibilityPolygonPoints)>1 and  self.light_on and not self.pos_fixed:
                    mx,my=pg.mouse.get_pos()
                    self.pos_fixed=[mx,my]
                elif event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and len(self.vecVisibilityPolygonPoints)>1 and  self.light_on and self.pos_fixed:
                    self.light_on=not self.light_on
                    self.pos_fixed.clear()








                if event.type == pg.KEYDOWN:

                    if event.key==pg.K_RETURN:
                        self.allows_events=not self.allows_events

                    if event.key == pg.K_a:
                        self.create_cell()
                        self.cache.clear()

                    if event.key==pg.K_s:
                        mx, my = pg.mouse.get_pos()
                        self.CalculateVisibilityPolygon(mx, my, 1000.)

                    if event.key==pg.K_s and len(self.vecVisibilityPolygonPoints)>1:

                        self.light_on=not self.light_on
                    if event.key==pg.K_f:
                        self.fancy_mode=not self.fancy_mode
                    if event.key==pg.K_m:

                        self.move_these.clear()
                        self.moving=not self.moving
                        mx,my=pg.mouse.get_pos()
                        mx -= self.dist_from_coords_beginning[0]
                        my -= self.dist_from_coords_beginning[1]
                        # cells={}
                        # for n,cell in enumerate(self.world):
                        #     if cell.exists:
                        #         coords_2d=self.from_1d_to_2d(n)
                        #         cells[n]=(self.distance(coords_2d[0],coords_2d[1],mx,my))
                        #
                        # min_list=min(cells.values())
                        # cell={k:v for k,v in cells.items() if v==min_list }
                        # edges=self.world[list(cell.keys())[0]].edge_id
                        #
                        # vertices={}
                        # for edge in edges:
                        #     vertices[edge]=(self.distance(self.vecEdges[edge].sx,self.vecEdges[edge].sy,mx,my),self.distance(self.vecEdges[edge].ex,self.vecEdges[edge].ey,mx,my))


                        vertices={}
                        for edge,ed in enumerate(self.vecEdges):
                            vertices[edge]=(self.distance(self.vecEdges[edge].sx,self.vecEdges[edge].sy,mx,my),self.distance(self.vecEdges[edge].ex,self.vecEdges[edge].ey,mx,my))

                        # getting 2 vertices of 2 edges

                        for i in range(2):
                            values=list(vertices.values())
                            first_ver=sorted(values,key=lambda x:min(x))[0]
                            ver={k:v for k,v in vertices.items() if v==first_ver }
                            if vertices[list(ver.keys())[0]][0]==min(vertices[list(ver.keys())[0]]):
                                self.move_these.append((list(ver.keys())[0],'start'))
                            else:
                                self.move_these.append((list(ver.keys())[0],'end'))
                            vertices.pop(list(ver.keys())[0])
                    if event.key==pg.K_r:
                        self.draw_rects=not self.draw_rects





