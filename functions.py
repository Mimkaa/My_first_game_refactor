import pygame as pg
from os import path
import math
from PIL import Image
vec=pg.Vector2
def draw_text(surf, text, font_name, size, color, x, y, align="nw"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)
    return text_rect

def load_animation( folder, frames, resize=(1, 1),flip=False):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'images')
    folder=path.join(img_folder, folder)
    animation = []
    for img in frames:
        animation.append(pg.image.load(path.join(folder,img)).convert_alpha())
    if resize!=(1,1):
        for num, img in enumerate(animation):
            animation[num] = pg.transform.scale(img, (int(img.get_width() * resize[0]), int(img.get_height() * resize[1])))

    if flip:
        for num, img in enumerate(animation):
            animation[num]=pg.transform.flip(animation[num], True, False)

    return animation

def vec2int(v):
    return [int(v.x), int(v.y)]

def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def distance_vec(vec1,vec2):
    return math.sqrt((vec1.x-vec2.x)**2+(vec1.y-vec2.y)**2)

def find_the_closest_out_of_a_sequence(coords,seque):
    dict_dist={}
    seque=[vec(el) for el in seque]
    for el in seque:
        dict_dist[tuple(vec2int(el))]=distance(el.x,el.y,coords.x,coords.y)
    sorted_dict={k: v for k, v in sorted(dict_dist.items(), key=lambda item: item[1])}
    key=list(sorted_dict.keys())[0]
    return key

def image_bottom_height(image,percent):
    raw_str = pg.image.tostring(image, "RGBA", False)
    img = Image.frombytes("RGBA", image.get_size(), raw_str)
    cropped_image=img.crop((0,img.height*percent,img.width,img.height))
    image= pg.image.fromstring(cropped_image.tobytes(), cropped_image.size, "RGBA")
    msk=pg.mask.from_surface(image)
    outline=msk.outline()
    outline.sort(key=lambda x:x[0])
    return outline[0][0],cropped_image.height,outline[-1][0]-outline[0][0]

def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key


def read_image_for_cloth(img,scale=5):
    # points from an image
    points=[]
    grounded_p=[]
    image = Image.open(img).convert('L')
    image=image.transpose(Image.FLIP_LEFT_RIGHT)
    image=image.rotate(90, expand=True)


    # separating by rows
    mat=[]
    additional=[]
    data=list(image.getdata())
    #data.reverse()

    for i in data:
        additional.append(i)
        if len(additional)==image.size[0]:
            mat.append(additional)
            additional=[]


    # getting coords of points
    for i ,row in enumerate(mat):
        for j,col in enumerate(row):
            if mat[i][j]!=255 :
                points.append([i,j])
            if mat[i][j]>50 and mat[i][j]<255:
                grounded_p.append([i,j])

    #diagonals ,[1,1],[-1,1],[-1,-1],[1,-1]]
    #connections
    conns=[[1,0],[-1,0],[0,-1],[0,1]]
    connections=[]
    for p in points:
        for c in conns:
            if vec2int(vec(p)+vec(c)) in points:
                connections.append([points.index(p),points.index(vec2int(vec(p)+vec(c)))])

    grounded=[points.index(p) for p in grounded_p]
    return points,connections,grounded,scale,image.size