from settings import *
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surfsce = pygame.display.get_surface()
