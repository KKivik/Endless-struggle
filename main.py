from settings import *
from map import Map

pygame.init()
pygame.display.set_caption('Endless struggle')
size = width, height
screen = pygame.display.set_mode(size)

player = None

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
        self.rect.x = width / 2 - 35
        self.rect.y = height / 2 - 35
        self.speed = 5

    def update(self, movement):
        if movement[pygame.K_w]:
            self.rect.y -= self.speed
        if movement[pygame.K_s]:
            self.rect.y += self.speed
        if movement[pygame.K_a]:
            self.rect.x -= self.speed
        if movement[pygame.K_d]:
            self.rect.x += self.speed

if __name__ == '__main__':
    fps = 50  # кадр/с

    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()

    card = Map('Map2.tmx')
    Main_Person = Person(player)

    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        movement = pygame.key.get_pressed()

        screen.fill((0, 0, 0))

        card.render(screen)

        all_sprites.update()
        player.update(movement)
        all_sprites.update(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
