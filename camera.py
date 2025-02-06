from settings import *
from bullet import Bullet

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, map):
        self.dx = 0
        self.dy = 0
        self.map = map

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if isinstance(obj, Bullet):
            # Для пуль используем мировые координаты с учетом смещения камеры
            obj.rect.centerx = obj.world_x + self.dx
            obj.rect.centery = obj.world_y + self.dy
        else:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def move_map(self):
        self.map.offset[0] += self.dx
        self.map.offset[1] += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
