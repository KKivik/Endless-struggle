import pygame
from os.path import join
from os import walk
import os
import sys
import pytmx
import math
import random
from pygame.math import Vector2

width, height = 960, 736
DIR = 'data'
TILE_SIZE = 32

def load_image(name, colorkey=None):
    fullname = f'data/{name}'

    # Если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image

