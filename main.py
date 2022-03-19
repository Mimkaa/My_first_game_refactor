import pygame as pg
import sys
from settings import *
from os import path
from main_menu_stuff import *
from tile_map import *
from particles_origin.objects import Flow
from collisions import ShapeOverlap_DIAG_STATIC,ShapeOverlap_DIAG,Polygon
from maps import Map
from quad_tree.objects import QuadTree,Rect_Tree

import time
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        # flags for additional functional
        self.draw_hitrects=False
        self.draw_rects=False
        self.draw_quad_tree=False
        # mouse
        self.mouse = Flow()
        # main_menu
        self.using_main_menu=True
        self.mainMenu=MainMenu(self)
        # map_manager
        self.map_manager=Map(self.map_folder,['start.tmx','cave_exit.tmx','first_location.tmx'])

    def load_data(self):
        self.main_font=path.join("PixelColeco-4vJW.ttf")
        # folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.sounds_folder = path.join(self.game_folder, 'sound')
        self.music_folder = path.join(self.game_folder, 'music')






    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls=pg.sprite.Group()
        self.decorations=pg.sprite.Group()
        self.characters=pg.sprite.Group()

        # create_a_map
        self.map_manager.create_map()
        self.map_manager.create_objects(self)

        # variables, pointers
        self.current_character=[i for i in self.all_sprites if i.__class__.__name__=='Player'][0]

        # quad tree
        boundary = Rect_Tree((0, 0), self.map_manager.rect.width,self.map_manager.rect.width)
        all_created_trees=[]
        self.quad_tree = QuadTree(boundary, 1,all_created_trees)
        list_objects=list(self.walls)+list(self.decorations)
        for obj in list_objects:
            self.quad_tree.insert(obj)
        self.query_rect=Rect_Tree((0,0),300,300)




    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if not self.using_main_menu:
                self.events()
                self.update()
                self.draw()
            else:
                pg.mouse.set_visible(False)
                self.mainMenu.events()
                self.mainMenu.update()
                self.mainMenu.draw()


    def quit(self):
        pg.quit()
        sys.exit()



    def update(self):
        # update portion of the game loop

        self.all_sprites.update()

        # layer management
        for spr in self.all_sprites:
            self.all_sprites.change_layer(spr, spr.rect.bottom)

        # collisions
        objects_query=self.quad_tree.query(self.query_rect,[])
        for ch in self.characters:
            for obj in objects_query:
                ShapeOverlap_DIAG_STATIC(ch.hit_poly,obj.hit_poly)
            ch.adjust()

        # quad_tree
        self.query_rect.pos=vec(self.current_character.rect.centerx-self.query_rect.width/2,self.current_character.rect.centery-self.query_rect.height/2)

        # update camera
        self.map_manager.camera_update(self.current_character)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):

        #draw_map
        self.map_manager.draw_map(self.screen)

        # draw_quad_tree
        if self.draw_quad_tree:
            self.quad_tree.show(self.screen,self.map_manager.camera.apply_rect)
            q_rect=pg.Rect(self.query_rect.pos.x,self.query_rect.pos.y,self.query_rect.width,self.query_rect.height)
            pg.draw.rect(self.screen,GREEN,self.map_manager.camera.apply_rect(q_rect),1)

        # draw all sprites
        for spr in self.all_sprites:
            self.screen.blit(spr.image,self.map_manager.camera.apply_rect(spr.rect))


        # draw rects
        if self.draw_hitrects:
            sprites=list(self.all_sprites)+list(self.walls)
            for spr in sprites:

                shape=self.map_manager.camera.apply_hit_poly(spr.hit_poly,self.map_manager.rect.topleft)

                for n, p in enumerate(shape.points):
                    pg.draw.line(self.screen, CYAN, (shape.points[n]),
                                 (shape.points[(n + 1) % len(shape.points)]))
                    pg.draw.line(self.screen, CYAN,shape.pos, shape.points[0])


        if self.draw_rects:
            for spr in self.all_sprites:
                pg.draw.rect(self.screen, RED, self.map_manager.camera.apply_rect(spr.rect), 1)


        # fps
        draw_text(self.screen,str(int(self.clock.get_fps())), self.main_font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()


    def events(self):
        # catch all events here

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_h:
                    self.draw_hitrects=not self.draw_hitrects
                if event.key==pg.K_r:
                    self.draw_rects=not self.draw_rects
                if event.key==pg.K_q:
                    self.draw_quad_tree=not self.draw_quad_tree



    def show_start_screen(self):
        self.screen.fill(BLACK)
        draw_text(self.screen,'Spirit`s Life', self.main_font, 100, WHITE, WIDTH/ 2, HEIGHT / 2, align='center')
        pg.display.flip()
        time.sleep(1)
        self.wait_for_key()
    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        count=0
        while waiting:
            count+=1
            if count%2==0:
                draw_text(self.screen,"Press a key to start", self.main_font, 50, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                           align='center')
            else:
                draw_text(self.screen,"Press a key to start", self.main_font, 50, BLACK, WIDTH / 2, HEIGHT * 3 / 4,
                               align='center')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
            pg.display.flip()
            self.clock.tick(5)



# create the game object
g = Game()
g.show_start_screen()
g.new()
g.run()
