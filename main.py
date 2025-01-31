from settings import *
from map import Map

pygame.init()
size = width, height
screen = pygame.display.set_mode(size)

class Person(pygame.sprite.Sprite):
    name = 'person.png'
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (70, 70))

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 - 30
        self.rect.y = height / 2 - 30
        self.sign = 1

    def update(self):
        pass

if __name__ == '__main__':
    fps = 50  # кадр/с

    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()

    card = Map('Map.tmx')
    Main_Person = Person(all_sprites)
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((0, 0, 0))
        card.render(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
