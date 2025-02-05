from settings import *

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



class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, columns, rows, groups):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(groups)
        self.animation = AnimatedSpriteEnemy(sprite_sheet, columns, rows)
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        # self.rect.x = width // 2 - 35
        # self.rect.y = height // 2 - 35
        # self.main_person = main_person
        # self.main_person_cords = self.main_person.image.get_rect()
        # self.rect.x = width // 2 - 150
        # self.rect.y = height // 2 - 150
        

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

            if top_or_low == "low":
                self.rect.x = random.choice(range(1, width))
                self.rect.y = height + 10

        if ver_or_hor == "horizontal":
            if top_or_low == "top":
                self.rect.x = -10
                self.rect.y = random.choice(range(1, height))

            if top_or_low == "low":
                self.rect.x = width + 10
                self.rect.y = random.choice(range(1, height))
        # self.rect.x = random.choice(range(1, width))
        # self.rect.y = random.choice(range(1, height))

    def update(self):
        self.animation.update()
        self.image = self.animation.get_current_frame()

        far_x = abs(self.rect.x - (width // 2 - 35))
        far_y = abs(self.rect.y - (height // 2 - 35))
        
        if far_x > far_y:
            if self.rect.x > width // 2 - 35:
                self.rect.x -= 2
            elif self.rect.x < width // 2 - 35:
                self.rect.x += 2
        else:
            if self.rect.y > height // 2 - 35:
                   self.rect.y -= 2
            elif self.rect.y < height // 2 - 35:
                   self.rect.y += 2
        # # # if self.rect.x > 
    def get_cords(self):
        return self.rect.x, self.rect.y


class Enemies():
    def __init__(self, sprite_sheet, columns, rows, groups):
        self.sprite_sheet = sprite_sheet
        self.columns = columns
        self.rows = rows
        self.groups = groups

        self.center_of_screen = (width // 2 - 35, height // 2 - 35)

        self.all_enemy_list = [] #list of every enemy


    def spawn(self):
        new_enemy = Enemy(self.sprite_sheet, self.columns, self.rows, self.groups)
        print(new_enemy.get_cords())
        self.all_enemy_list.append(new_enemy)
    
        
    def nearest_enemy(self):
        pass
        
    def update(self):
        for current_enemy in self.all_enemy_list:
            current_enemy.update()

    def set_spawn_rate(self):
        self.animation_speed = 1000  # Скорость анимации
        self.last_update = pygame.time.get_ticks()
        
        
    def spawning(self):
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.spawn()
            self.last_update = now