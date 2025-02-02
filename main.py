from settings import *
from map import Map
from camera import Camera

pygame.init()
pygame.display.set_caption('Endless struggle')
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
        self.speed = 5

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_RIGHT:
                self.rect = self.rect.move(10, 0)
            if args[0].key == pygame.K_LEFT:
                self.rect = self.rect.move(-10, 0)
            if args[0].key == pygame.K_DOWN:
                self.rect = self.rect.move(0, 10)
            if args[0].key == pygame.K_UP:
                self.rect = self.rect.move(0, -10)

if __name__ == '__main__':
    fps = 60  # кадр/с

    clock = pygame.time.Clock()
    running = True

    map = Map('Map2.tmx')
    all_sprites = Camera(map)
    Main_Person = Person(all_sprites)
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)

        screen.fill((0, 0, 0))
        all_sprites.custom_draw(Main_Person)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
