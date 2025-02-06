from settings import *

class Map:
    def __init__(self, filename):
        #image of map
        self.map = pytmx.load_pygame(f'{DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.display_surface = pygame.display.get_surface()
        #offset of map
        self.offset = [0, 0]

    def render(self):
        start_x = int(-self.offset[0] // self.tile_size)
        start_y = int(-self.offset[1] // self.tile_size)
        end_x = int((-self.offset[0] + width) // self.tile_size) + 1
        end_y = int((-self.offset[1] + height) // self.tile_size) + 1

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                # Используем модульную арифметику для повторения карты
                tile_x = x % self.width
                tile_y = y % self.height

                # Получаем изображение тайла
                image = self.map.get_tile_image(tile_x, tile_y, 0)
                if image:
                    # Вычисляем экранные координаты тайла
                    screen_x = x * self.tile_size + self.offset[0]
                    screen_y = y * self.tile_size + self.offset[1]
                    self.display_surface.blit(image, (screen_x, screen_y))

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))

    def get_rect(self):
        return self.topleft