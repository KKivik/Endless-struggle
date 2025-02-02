from settings import *
from map import Map

pygame.init()
pygame.display.set_caption('Endless struggle')
size = width, height
screen = pygame.display.set_mode(size)

<<<<<<< Updated upstream
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
=======
class AnimatedSprite:
    def __init__(self, sprite_sheet, columns, rows):
        self.frames = []
        self.cut_sheet(sprite_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.animation_speed = 100  # Скорость анимации (в миллисекундах)
        self.last_update = pygame.time.get_ticks()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface(pygame.Rect(col * self.rect.width, row * self.rect.height,
                                                      self.rect.width, self.rect.height))
                self.frames.append(frame)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def get_current_frame(self):
        return self.frames[self.cur_frame]


class Person(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, columns, rows, groups):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(groups)
        self.animation = AnimatedSprite(sprite_sheet, columns, rows)
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 30
        self.rect.y = height // 2 - 30

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()
>>>>>>> Stashed changes

if __name__ == '__main__':
    fps = 50  # кадр/с

    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()

    card = Map('Map2.tmx')
<<<<<<< Updated upstream
    Main_Person = Person(player)
=======
    sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    Main_Person = Person(sprite_sheet, columns=6, rows=1, groups=all_sprites)
>>>>>>> Stashed changes

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
