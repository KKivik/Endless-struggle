from settings import *

class Map:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f'{DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.topleft = (0, 0)
        self.display_surfsce = pygame.display.get_surface()

    def render(self, offset=(0, 0)):
        self.topleft = (self.topleft[0] + offset[0], self.topleft[1] + offset[1])
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                self.display_surfsce.blit(image, (x * self.tile_size + offset[0], y * self.tile_size + offset[1]))

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))

    def get_rect(self):
        print(self.topleft)
        return self.topleft