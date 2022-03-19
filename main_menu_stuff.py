import pygame as pg
from settings import *
import pytweening as tween
from particles_origin.objects import Flow
from functions import *
import random
vec=pg.Vector2
class MenuButton:
    def __init__(self,images,menu,pos,text,text_size,color):
        self.menu=menu
        self.images=images
        self.rect=self.images[0].get_rect()
        self.pos=vec(pos)
        self.text=text
        self.text_size=text_size
        self.color=color
        self.on_button=False

    def draw_button(self,surf):
        if  self.on_button :
            self.rect.center=self.pos
            surf.blit(self.images[0],self.rect)
            draw_text(surf,self.text,FONT,self.text_size,self.color,self.rect.centerx,self.rect.centery,align="center")
        else:
            self.rect.center = self.pos
            surf.blit(self.images[1], self.rect)
            draw_text(surf,self.text, FONT, self.text_size, self.color, self.rect.centerx,self.rect.centery,
                                align="center")

class Menu_Image(pg.sprite.Sprite):
    def __init__(self,images,menu,pos):
        self.menu= menu
        self.group = menu.menu_sprites
        self._layer = 0
        pg.sprite.Sprite.__init__(self, self.group)
        self.images=images
        self.image=self.images['eyes_closed'][0]
        self.pos=pos
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.current_frame=0
        self.last_update = 0

    def update(self):
        now = pg.time.get_ticks()
        mx, my = pg.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
                if   now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.images['eyes_opened'])
                    self.image = self.images['eyes_opened'][self.current_frame]
                    center=self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center=center
        else:
                if   now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.images['eyes_closed'])
                    self.image = self.images['eyes_closed'][self.current_frame]
                    center=self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center=center
    def get_layer(self):
        return self._layer

class MenuFirefly(pg.sprite.Sprite):
    def __init__(self,images, menu, pos):
        self.menu = menu
        self.group = menu.menu_sprites
        self._layer = 1
        self.or_layer=1
        self.images=images
        self.images_origin=images
        pg.sprite.Sprite.__init__(self, self.group)
        self.pos = pos
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = vec(pos)
        self.current_frame = 0
        self.last_update = 0
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir=1
        self.vel = random.randrange(100, 200)
        self.original_width=self.image.get_width()

        rand_val = random.uniform(1.5, 4)
        self.images = [pg.transform.scale(self.images_origin[i],
                                          (int(self.original_width * rand_val), int(self.original_width * rand_val)))
                       for i in range(len(self.images))]


    def update(self,menu_ava):
        self.animate()
        self.pos.y -= self.vel * self.menu.dt
        #bobing motion
        offset = 3 * (self.tween(self.step / 3) - 0.5)
        self.pos.x += offset* self.dir
        self.step += 0.03
        if self.step>3:
            self.step=0
            self.dir*=-1

        self.rect.center=self.pos

        if self.pos.y<-self.rect.height:

            rand_val=random.uniform(1.5,4)
            self.images=[pg.transform.scale(self.images_origin[i],(int(self.original_width*rand_val),int(self.original_width*rand_val))) for i in range(len(self.images))]
            self.vel = random.randrange(100, 200)

            self.pos.y=random.randint(HEIGHT+self.original_width*4,HEIGHT+self.original_width*8)
            self.pos.x=random.randint(0,WIDTH)

        # changing the layer
        if self.rect.width<self.original_width*2.7:
            self.menu.menu_sprites.change_layer(self,menu_ava.get_layer()-1)
        else:
            self.menu.menu_sprites.change_layer(self,self.or_layer)





    def animate(self):
        now = pg.time.get_ticks()

        if now - self.last_update > 400:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect()


class MainMenu:
    def __init__(self,game):
        self.click=False
        self.game=game
        self.button_on = 0
        self.dt=self.game.clock.tick(FPS) / 1000

        # mouse
        self.mouse = Flow()

        self.menu_sprites = pg.sprite.LayeredUpdates()

        # menu img
        menu_image_dict = {'eyes_opened': load_animation('menu', ['menu_not_sleep1.png', 'menu_not_sleep2.png',
                                                                       'menu_not_sleep3.png', 'menu_not_sleep4.png',
                                                                       'menu_not_sleep5.png']),
                           'eyes_closed': load_animation('menu',
                                                              ['menu_sleep1.png', 'menu_sleep2.png', 'menu_sleep3.png',
                                                               'menu_sleep4.png', 'menu_sleep5.png'])
                           }
        self.menu_image = Menu_Image(menu_image_dict, self, (WIDTH // 2, HEIGHT // 2))

        # buttons
        new_game_button = MenuButton(load_animation('menu', ['button2.png', 'button.png']), self,
                                     (WIDTH / 5, HEIGHT / 4), 'NEW_GAME', 50, WHITE)
        height = new_game_button.images[0].get_height()
        leave_button = MenuButton(load_animation('menu', ['button2.png', 'button.png']), self,
                                  (WIDTH / 5, HEIGHT / 4 + height + 10), 'LEAVE', 50, WHITE)
        sound_button = MenuButton(load_animation('menu', ['button2.png', 'button.png']), self,
                                  (WIDTH / 5, (HEIGHT / 4 + height * 2) + 20), 'SOUND:', 50, WHITE)
        self.list_buttons = [new_game_button, leave_button, sound_button]

        # fireflies
        self.fireflies = [MenuFirefly(load_animation('menu', ['filefly1.png', 'filefly2.png', 'filefly3.png']), self,
                                 (random.randint(0, WIDTH), random.randint(HEIGHT + 17 * 4, HEIGHT * 2))) for i in
                     range(100)]
    def update(self):
        self.dt = self.game.dt

        # update mouse
        self.mouse.emit(pg.mouse.get_pos())
        # self.mouse.applyForce((0.5,0))

        self.menu_image.update()

        for f in self.fireflies:
            f.update(self.menu_image)


        for n, b in enumerate(self.list_buttons):
            if b.rect.collidepoint(pg.mouse.get_pos()):
                self.button_on = n
        self.list_buttons[self.button_on].on_button = True

        if self.click and self.list_buttons[self.button_on].text == 'LEAVE':
            self.game.quit()
        if self.click and self.list_buttons[self.button_on].text == 'NEW_GAME':
            self.game.using_main_menu=False
            self.game.new()
            self.game.run()

    def draw(self):
        self.game.screen.fill(DARKBLUE)

        # button drawing
        for b in self.list_buttons:
            b.draw_button(self.game.screen)
            b.on_button = False
        # fps
        draw_text(self.game.screen,str(int(self.game.clock.get_fps())), FONT, 40, WHITE, 50, 50, align="center")

        self.menu_sprites.draw(self.game.screen)
        # draw mouse
        self.mouse.show(self.game.screen)

        pg.display.flip()

    def events(self):
        self.click=False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if any(b.rect.collidepoint(pg.mouse.get_pos()) for b in self.list_buttons) and event.type == pg.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key == pg.K_DOWN:
                    self.button_on += 1
                    if self.button_on >= len(self.list_buttons):
                        self.button_on = 0

                if event.key == pg.K_UP:
                    self.button_on -= 1
                    if self.button_on < 0:
                        self.button_on = len(self.list_buttons) - 1
                if event.key == pg.K_RETURN:
                    self.click = True






