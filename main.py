from settings import *

pygame.init()
size = width, height
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Person(pygame.sprite.Sprite):
    image = load_image("person.png")
    image = pygame.transform.scale(image, (70, 70))

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = 300
        self.sign = 1

    def update(self):
        pass

if __name__ == '__main__':
    fps = 50  # кадр/с

    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()

    Main_Person = Person(all_sprites)
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
