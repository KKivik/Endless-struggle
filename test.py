from settings import *
from map import Map
import pygame
import os

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
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 35  # Центрируем персонажа
        self.rect.y = height // 2 - 35
        self.speed = 5  # Скорость перемещения

    def update(self, keys):
        # Обработка движения в зависимости от нажатых клавиш
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
        """Разделяет спрайт-лист на отдельные фреймы."""
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface(pygame.Rect(col * self.rect.width, row * self.rect.height,
                                                      self.rect.width, self.rect.height))
                self.frames.append(frame)

    def update(self):
        """Обновляет текущий фрейм анимации."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def get_current_frame(self):
        """Возвращает текущий фрейм анимации."""
        return self.frames[self.cur_frame]

class Person(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, columns, rows, groups):
        super().__init__(groups)
        self.animation = AnimatedSprite(sprite_sheet, columns, rows)  # Создаем объект анимации
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 35
        self.rect.y = height // 2 - 35
        self.speed = 5  # Скорость движения

    def update(self, keys):
        """Обновляет анимацию и движение персонажа."""
        self.animation.update()
        self.image = self.animation.get_current_frame()

        # Обработка движения
>>>>>>> Stashed changes
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Вверх
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Вниз
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Влево
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Вправо
            self.rect.x += self.speed

if __name__ == '__main__':
<<<<<<< Updated upstream
    fps = 50  # Кадры в секунду
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()
    card = Map('Map2.tmx')
    Main_Person = Person(player)
=======
    fps = 50  # Кадр/с
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()

    # Загружаем спрайт-лист с анимацией
    sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    Main_Person = Person(sprite_sheet, columns=6, rows=1, groups=all_sprites)

    card = Map('Map2.tmx')
>>>>>>> Stashed changes

    while running:  # Главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Получаем текущее состояние клавиш
        keys = pygame.key.get_pressed()

<<<<<<< Updated upstream
        # Очищаем экран
        screen.fill((0, 0, 0))

        # Рендерим карту
        card.render(screen)

        # Обновляем и рисуем спрайты
        all_sprites.update()
        player.update(keys)  # Передаем состояние клавиш для обновления игрока
        all_sprites.draw(screen)
        player.draw(screen)

        # Обновляем экран
=======
        screen.fill((0, 0, 0))
        card.render(screen)
        all_sprites.draw(screen)
        Main_Person.update(keys)  # Передаем состояние клавиш для обновления игрока
>>>>>>> Stashed changes
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()