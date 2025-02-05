from settings import *
class Camera(pygame.sprite.Group):
    def __init__(self, map):
        super().__init__()
        self.display_surfsce = pygame.display.get_surface()
        #camera offset
        self.offset = pygame.math.Vector2(50, 10)
        self.map = map
        self.map_rect = self.map.get_rect()
        self.half_w = self.display_surfsce.get_width()
        self.half_h = self.display_surfsce.get_height()

    def center_camera(self,target):
        self.offset.x = target.rect.x - self.half_w
        self.offset.y = target.rect.y - self.half_h

    def custom_draw(self):
        map_offset = self.map_rect + self.offset
        self.map.render(map_offset)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft
            self.display_surfsce.blit(sprite.image, offset_pos)