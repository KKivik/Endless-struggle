from settings import *
from map import Map
from bullet import Bullet
from camera import Camera
from enemy import Enemy, AnimatedSpriteEnemy, Enemies
from labels import Label_for_txt

pygame.init()
pygame.display.set_caption('Endless struggle')
size = width, height
screen = pygame.display.set_mode(size)
vol_of_game = 2
vol_of_menu = 2

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
    def __init__(self, idle_sprite_sheet, walk_sprite_sheet, columns_idle, rows_idle, columns_walk, rows_walk, groups):
        super().__init__(groups)
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!

        # Анимация стоя
        self.idle_animation = AnimatedSprite(idle_sprite_sheet, columns_idle, rows_idle)
        # Анимация ходьбы
        self.walk_animation = AnimatedSprite(walk_sprite_sheet, columns_walk, rows_walk)

        self.current_animation = self.idle_animation

        self.image = self.current_animation.get_current_frame()
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

    def update(self, moving=False):
        if moving:
            self.current_animation = self.walk_animation
        else:
            self.current_animation = self.idle_animation
        self.current_animation.update()
        self.image = self.current_animation.get_current_frame()

def start_screen():
    global vol_of_game, vol_of_menu
    pygame.mixer.music.load("data/Menu_music.mp3")  # Укажите путь к файлу
    pygame.mixer.music.play(-1)
    if vol_of_menu == 0:
        pygame.mixer.music.set_volume(0)
    elif vol_of_menu == 1:
        pygame.mixer.music.set_volume(0.25)
    elif vol_of_menu == 2:
        pygame.mixer.music.set_volume(0.5)
    elif vol_of_menu == 3:
        pygame.mixer.music.set_volume(1)


    background = pygame.transform.scale(load_image('background.png'),size)
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()
    choice = 1
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or ():
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and choice == 1:
                    pygame.mixer.music.stop()
                    game()
                elif e.key == pygame.K_RETURN and choice == 3:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_RETURN and choice == 2:
                    settings()
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

def end_screen(all_enemies):
    FPS = 50

    background = pygame.transform.scale(load_image('end.png'), size)
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()

    text_color = (255, 0, 0)
    text = pygame.font.Font(None, 40).render(f'{all_enemies.number_of_killed_enemies}', True, text_color)
    text_rect = text.get_rect()
    text_rect.x = 230
    text_rect.y = 335
    screen.blit(text, text_rect)

    pygame.mixer.music.load("data/Death_musik.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    start_screen()
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)


def settings():
    global vol_of_menu, vol_of_game
    pygame.mixer.music.load("data/Menu_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(vol_of_menu / 4)  # Используем текущую громкость меню

    # Начальное изображение в зависимости от текущих настроек
    if vol_of_game == 0:
        background_img = 'es_game_0_fixxed.png'
    elif vol_of_game == 1:
        background_img = 'es_game_25_fixxed.png'
    elif vol_of_game == 2:
        background_img = 'es_game_50_fixxed.png'
    elif vol_of_game == 3:
        background_img = 'es_game_100_fixxed.png'

    background = pygame.transform.scale(load_image(background_img), size)
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()
    choice = 1  # 1 - громкость игры, 2 - громкость меню, 3 - назад

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if choice == 1:  # Громкость игры
                        vol_of_game = (vol_of_game + 1) % 4
                        if vol_of_game == 0:
                            background_img = 'es_game_0_fixxed.png'
                        elif vol_of_game == 1:
                            background_img = 'es_game_25_fixxed.png'
                        elif vol_of_game == 2:
                            background_img = 'es_game_50_fixxed.png'
                        elif vol_of_game == 3:
                            background_img = 'es_game_100_fixxed.png'
                    elif choice == 2:  # Громкость меню
                        vol_of_menu = (vol_of_menu + 1) % 4
                        pygame.mixer.music.set_volume(vol_of_menu / 4)
                        if vol_of_menu == 0:
                            background_img = 'es_menu_0.png'
                        elif vol_of_menu == 1:
                            background_img = 'es_menu_25.png'
                        elif vol_of_menu == 2:
                            background_img = 'es_menu_50.png'
                        elif vol_of_menu == 3:
                            background_img = 'es_menu_100.png'
                    elif choice == 3:  # Назад
                        start_screen()
                        return

                    # Обновляем фон
                    background = pygame.transform.scale(load_image(background_img), size)
                    screen.blit(background, (0, 0))

                elif e.key == pygame.K_DOWN:
                    choice = min(choice + 1, 3)
                    # Обновляем изображение для показа выбранного пункта
                    if choice == 1:
                        if vol_of_game == 0:
                            background_img = 'es_game_0_fixxed.png'
                        elif vol_of_game == 1:
                            background_img = 'es_game_25_fixxed.png'
                        elif vol_of_game == 2:
                            background_img = 'es_game_50_fixxed.png'
                        elif vol_of_game == 3:
                            background_img = 'es_game_100_fixxed.png'
                    elif choice == 2:
                        if vol_of_menu == 0:
                            background_img = 'es_menu_0.png'
                        elif vol_of_menu == 1:
                            background_img = 'es_menu_25.png'
                        elif vol_of_menu == 2:
                            background_img = 'es_menu_50.png'
                        elif vol_of_menu == 3:
                            background_img = 'es_menu_100.png'
                    elif choice == 3:
                        start_screen()
                        return

                    background = pygame.transform.scale(load_image(background_img), size)
                    screen.blit(background, (0, 0))

                elif e.key == pygame.K_UP:
                    choice = max(choice - 1, 1)
                    # Аналогично обработке K_DOWN
                    if choice == 1:
                        if vol_of_game == 0:
                            background_img = 'es_game_0_fixxed.png'
                        elif vol_of_game == 1:
                            background_img = 'es_game_25_fixxed.png'
                        elif vol_of_game == 2:
                            background_img = 'es_game_50_fixxed.png'
                        elif vol_of_game == 3:
                            background_img = 'es_game_100_fixxed.png'
                    elif choice == 2:
                        if vol_of_menu == 0:
                            background_img = 'es_menu_0.png'
                        elif vol_of_menu == 1:
                            background_img = 'es_menu_25.png'
                        elif vol_of_menu == 2:
                            background_img = 'es_menu_50.png'
                        elif vol_of_menu == 3:
                            background_img = 'es_menu_100.png'
                    elif choice == 3:
                        start_screen()
                        return

                    background = pygame.transform.scale(load_image(background_img), size)
                    screen.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(50)

def game():
    global vol_of_game
    fps = 50  # Кадр/с
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    Label_kill = Label_for_txt(screen)

    map = Map('Map3.tmx')
    cam = Camera(map)

    pygame.mixer.music.load("data/Main_music.mp3")
    pygame.mixer.music.play(-1)
    if vol_of_game == 0:
        pygame.mixer.music.set_volume(0)
    elif vol_of_game == 1:
        pygame.mixer.music.set_volume(0.25)
    elif vol_of_game == 2:
        pygame.mixer.music.set_volume(0.5)
    elif vol_of_game == 3:
        pygame.mixer.music.set_volume(1)

    idle_sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    walk_sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-walk.png'))

    Main_Person = Person(
        idle_sprite_sheet=idle_sprite_sheet,
        walk_sprite_sheet=walk_sprite_sheet,
        columns_idle=6, rows_idle=1,
        columns_walk=4, rows_walk=1,
        groups=all_sprites
    )

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
        moving = False

        if keys[pygame.K_LEFT]:
            Main_Person.rect.x -= 5
            moving = True

        if keys[pygame.K_RIGHT]:
            Main_Person.rect.x += 5
            moving = True

        if keys[pygame.K_UP]:
            Main_Person.rect.y -= 5
            moving = True

        if keys[pygame.K_DOWN]:
            Main_Person.rect.y += 5
            moving = True


        screen.fill((0, 0, 0))

        cam.update(Main_Person)

        Main_Person.update(moving=moving)

        for sprite in all_sprites:
            cam.apply(sprite)

        cam.move_map()
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
                    pygame.mixer.music.stop()
                    end_screen(All_Enemies)
                    running = False  # Остановка игры (или другая логика)


        all_sprites.draw(screen)
        Label_kill.draw_button('Killed:', True)
        Label_kill.draw_button(f'{All_Enemies.number_of_killed_enemies}', False)
        pygame.display.flip()
        clock.tick(fps)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == '__main__':
    start_screen()