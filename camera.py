from settings import *
class Camera(pygame.sprite.Group):
    def __init__(self, map):
        super().__init__()

        # camera offset
        self.display_surfsce = pygame.display.get_surface()
        self.half_w = self.display_surfsce.get_size()[0] // 2
        self.half_h = self.display_surfsce.get_size()[1] // 2

        self.offset = pygame.math.Vector2()
        self.map = map
        self.map_rect = self.map.get_rect()

    def center_camera_target(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h


    def custom_draw(self, person):
        map_offset = self.map_rect + self.offset
        self.center_camera_target(person)
        self.map.render(map_offset)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surfsce.blit(sprite.image, offset_pos)