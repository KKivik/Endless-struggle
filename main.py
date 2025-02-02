from settings import *
from map import Map
import pygame
import os

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

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()

if __name__ == '__main__':
    fps = 50  # Кадр/с
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()

    card = Map('Map2.tmx')
    sprite_sheet = pygame.image.load(os.path.join('data', 'skeleton-idle.png'))
    Main_Person = Person(sprite_sheet, columns=6, rows=1, groups=all_sprites)

    while running:  # Главный игровой цикл
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