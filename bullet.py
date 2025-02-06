from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, groups):
        super().__init__(groups)
        self.original_image = pygame.transform.scale(load_image('bullet.png'), (100, 100))  # Увеличим размер
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=start_pos)

        # Сохраняем мировые координаты
        self.world_x = start_pos[0]
        self.world_y = start_pos[1]

        # Рассчитываем направление в мировых координатах
        direction = Vector2(target_pos) - Vector2(start_pos)
        if direction.length() > 0:
            self.velocity = direction.normalize() * 15
        else:
            self.velocity = Vector2()

    def update(self):
        # Обновляем мировые координаты
        self.world_x += self.velocity.x
        self.world_y += self.velocity.y

        # Проверка границ в мировых координатах
        if not (-1000 < self.world_x < width + 1000 and -1000 < self.world_y < height + 1000):
            self.kill()
