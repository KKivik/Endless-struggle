from settings import *
from map import Map

from bullet import Bullet

from camera import Camera

from enemy import Enemy, AnimatedSpriteEnemy, Enemies

pygame.init()
pygame.display.set_caption('Endless struggle')
size = width, height
screen = pygame.display.set_mode(size)

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
        self.health = 100 #health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("Main Person is dead!")
            return True  # Персонаж умер
        return False  # Персонаж еще жив

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()

def start_screen():

    pygame.mixer.music.load("data/Menu_music.mp3")  # Укажите путь к файлу
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    background = pygame.transform.scale(load_image('background.png'),size)
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
                    pygame.mixer.music.stop()
                    return
                elif e.key == pygame.K_DOWN and choice == 1:
                    choice += 1
                    background = pygame.transform.scale(load_image('background1.png'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_DOWN and choice == 2:
                    choice += 1
                    background = pygame.transform.scale(load_image('background2.png'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_UP and choice == 3:
                    choice -= 1
                    background = pygame.transform.scale(load_image('background1.png'), size)
                    screen.blit(background, (0, 0))
                elif e.key == pygame.K_UP and choice == 2:
                    choice -= 1
                    background = pygame.transform.scale(load_image('background.png'), size)
                    screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(50)

def end_screen():
    FPS = 50

    background = pygame.transform.scale(load_image('end.png'), size)
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)
        
if __name__ == '__main__':

    start_screen()
    fps = 50  # Кадр/с
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    map = Map('Map2.tmx')
    cam = Camera(map)

    pygame.mixer.music.load("data/Main_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    
    sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    Main_Person = Person(sprite_sheet, columns=6, rows=1, groups=all_sprites)

    # Upload the Enemy image
    enemy_sprite_sheet = pygame.transform.scale(load_image(os.path.join('enemy_idle.png')), (150,50))

    # Creates the class that manages all enemies
    All_Enemies = Enemies(enemy_sprite_sheet, columns=4, rows=1, target_groups=[all_sprites])

    # Sets spawn rate
    All_Enemies.set_spawn_rate()

    while running:  # Главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_center = Main_Person.rect.center
                    mouse_pos = pygame.mouse.get_pos()
                    Bullet(player_center, mouse_pos, [all_sprites, bullets_group])

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

        Main_Person.update()
        map.render()

        #All enemies managing
        All_Enemies.spawning()
        All_Enemies.update()
        bullets_group.update()

        hits = pygame.sprite.groupcollide(All_Enemies.enemies_group, bullets_group, True, True)
        if hits: # Add plus one to number of dead bodies 
            All_Enemies.add_dead_body()


        death = pygame.sprite.spritecollide(Main_Person, All_Enemies.enemies_group, False)
        if death:  # Если есть коллизия
            for enemy in death:  # Обрабатываем каждого врага, который столкнулся с персонажем
                if Main_Person.take_damage(10):  # Персонаж получает урон
                    running = False  # Остановка игры (или другая логика)


        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

    pygame.mixer.music.stop()

    pygame.quit()
