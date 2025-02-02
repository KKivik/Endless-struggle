from settings import *
class Camera(pygame.sprite.Group):
    def __init__(self, map):
        super().__init__()
        self.display_surfsce = pygame.display.get_surface()
        #camera offset
        self.offset = pygame.math.Vector2(500, 100)
        self.map = map
        self.map_rect = self.map.get_rect()

    def custom_draw(self):
        map_offset = self.map_rect + self.offset
        self.map.render(map_offset)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surfsce.blit(sprite.image, offset_pos)