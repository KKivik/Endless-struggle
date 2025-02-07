from settings import *

class Label_for_txt():
    def __init__(self, screen):
        self.screen = screen
        self.width,self.height = 110,80
        self.button_color=(0,100,100,80)
        self.text_color=(255,0,0)
        self.rect = pygame.Rect(0,0, self.width,self.height)
        self.rect.x = 10
        self.rect.y = 650

    def create_txt_1(self, text):
        self.text = pygame.font.Font(None, 40).render(text, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = self.rect.x + 5
        self.text_rect.y = self.rect.y + 5

    def create_txt_2(self, text):
        self.text = pygame.font.Font(None, 40).render(text, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = self.rect.x + 45
        self.text_rect.y = self.rect.y + 40


    def draw_button(self, text, fl):
        # Создаем поверхность с альфа-каналом для плашки
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        button_surface.fill(self.button_color)
        if fl:
            self.create_txt_1(text)
            self.screen.blit(button_surface, self.rect)
            self.screen.blit(self.text, self.text_rect)
        else:
            self.create_txt_2(text)
            self.screen.blit(button_surface, self.rect)
            self.screen.blit(self.text, self.text_rect)