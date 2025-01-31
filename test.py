from settings import *
from map import Map
import pygame
import os

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
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 35  # Центрируем персонажа
        self.rect.y = height // 2 - 35
        self.speed = 5  # Скорость перемещения

    def update(self, keys):
        # Обработка движения в зависимости от нажатых клавиш
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Вверх
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Вниз
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Влево
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Вправо
            self.rect.x += self.speed

if __name__ == '__main__':
    fps = 50  # Кадры в секунду
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()
    card = Map('Map2.tmx')
    Main_Person = Person(player)

    while running:  # Главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Получаем текущее состояние клавиш
        keys = pygame.key.get_pressed()

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
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()