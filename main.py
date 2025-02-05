from settings import *
from map import Map

from camera import Camera

from enemy import Enemy, AnimatedSpriteEnemy, Enemies

pygame.init()
pygame.display.set_caption('Endless struggle')
size = width, height
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = f'data/{name}'

    # Если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image

class AnimatedSprite:
    def __init__(self, sprite_sheet, columns, rows):
        self.frames = []
        self.cut_sheet(sprite_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.animation_speed = 100  # Скорость анимации
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
        self.rect.x = width // 2 - 35
        self.rect.y = height // 2 - 35

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()

def start_screen():

    background = pygame.transform.scale(load_image('background.jpg'),size)
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()
    choice = 1
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and choice == 1:
                    return
                elif e.key == pygame.K_DOWN and choice == 1:
                    choice += 1
                    background = pygame.transform.scale(load_image('background1.jpg'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_DOWN and choice == 2:
                    choice += 1
                    background = pygame.transform.scale(load_image('background2.jpg'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_UP and choice == 3:
                    choice -= 1
                    background = pygame.transform.scale(load_image('background1.jpg'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_UP and choice == 2:
                    choice -= 1
                    background = pygame.transform.scale(load_image('background.jpg'), size)
                    screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(50)

    
        
if __name__ == '__main__':
    start_screen()
    fps = 50  # Кадр/с
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()

    map = Map('Map2.tmx')
    cam = Camera(map)
    
    sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    Main_Person = Person(sprite_sheet, columns=6, rows=1, groups=all_sprites)

    # Upload the Enemy image
    enemy_sprite_sheet = pygame.transform.scale(load_image(os.path.join('enemy_idle.png')), (150,50))

    # Creates the class that manages all enemies
    All_Enemies = Enemies(enemy_sprite_sheet, columns=4, rows=1, groups=all_sprites)

    # Sets spawn rate
    All_Enemies.set_spawn_rate()

    while running:  # Главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Main_Person.rect.x -= 5

        if keys[pygame.K_RIGHT]:
            Main_Person.rect.x += 5

        if keys[pygame.K_UP]:
            Main_Person.rect.y -= 5

        if keys[pygame.K_DOWN]:
            Main_Person.rect.y += 5


        screen.fill((0, 0, 0))

        cam.update(Main_Person)
        Main_Person.update()
        for sprite in all_sprites:
            cam.apply(sprite)
        cam.move_map()


        map.render()
        all_sprites.draw(screen)

        #All enemies managing
        All_Enemies.spawning()
        All_Enemies.update()


        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()