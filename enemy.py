from settings import *

# AnimatedSprite class for Enemy class (probably has no sense)
class AnimatedSpriteEnemy:
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


# Class of a singular enemy (In game cycle we manage it in Enemies class)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, columns, rows, groups):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(groups)
        self.animation = AnimatedSpriteEnemy(sprite_sheet, columns, rows)
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()

        #SPAWNING ENEMY ON RANDOM PLACE AT WINDOW
        # self.rect.x = random.choice(range(1, width))
        # self.rect.y = random.choice(range(1, height))


        # SPAWNING ENEMY OUT OF WINDOW
        ver_or_hor = random.choice(("vertical", "horizontal"))
        top_or_low = random.choice(("top", "low"))
        if ver_or_hor == "vertical":
            if top_or_low == "top":
                self.rect.x = random.choice(range(1, width))
                self.rect.y = -10
            else:
                self.rect.x = random.choice(range(1, width))
                self.rect.y = height + 10
        else:
            if top_or_low == "top":
                self.rect.x = -10
                self.rect.y = random.choice(range(1, height))
            else:
                self.rect.x = width + 10
                self.rect.y = random.choice(range(1, height))

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()
        target_x = width // 2 - 35
        target_y = height // 2 - 35
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.rect.x += int(2 * dx / distance)
            self.rect.y += int(2 * dy / distance)


class Enemies:
    def __init__(self, sprite_sheet, columns, rows, target_groups):
        self.sprite_sheet = sprite_sheet
        self.columns = columns
        self.rows = rows
        self.target_groups = target_groups
        self.enemies_group = pygame.sprite.Group()
        self.center = (width // 2 - 35, height // 2 - 35)
        self.set_spawn_rate()
        self.number_of_killed_enemies = 0


    def spawn(self):
        groups = self.target_groups + [self.enemies_group]
        Enemy(self.sprite_sheet, self.columns, self.rows, groups)

    def update(self):
        self.enemies_group.update()

    # Sets the spawn speed
    def set_spawn_rate(self):
        self.animation_speed = 1000  # Speed of spawning
        self.last_update = pygame.time.get_ticks()
        
    # Makes enemies spawning on a constant time gap
    def spawning(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.spawn()
            self.last_update = now

        # Gives back the nearest Enemy (we can get cords from Enemy's method)          
    def nearest_enemy(self):
        nearest_list = []
        for current_enemy in self.all_enemy_list:
            cords_x, cords_y = current_enemy.get_cords()
            distance = (self.center_of_screen[0] - cords_x) **2 + (self.center_of_screen[1] - cords_y)**2
            nearest_list.append([distance, current_enemy])
        if nearest_list:
            # return sorted(nearest_list)[0][1]
            return sorted(nearest_list, key=lambda x: x[0])[0][1]
        else:
            return "Empty list of enemies", "123"

    def number_of_killed(self):
        return self.number_of_killed_enemies

    def add_dead_body(self):
        self.number_of_killed_enemies += 1

