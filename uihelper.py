import pygame 

FONT_NAME = "sans-serif"
FONT_SIZE_SMALL = 25

COLORS = {
	"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "RED": (255, 0, 0),
	"BLUE": (0, 0, 255), "GREEN": (106, 170, 100), "YELLOW": (201, 180, 88), 
	"GRAY": (120, 124, 126), "LIGHT_GRAY": (211, 214, 218), "BG": (251, 252, 255)
}

class Button:
    def __init__ (self, x, y, w, h, text, callback, color=(100, 100, 200)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color = color
        self.font = pygame.font.SysFont(FONT_NAME, 30)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, COLORS["WHITE"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class TextInput:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.font = pygame.font.SysFont(FONT_NAME, 25)
    def draw(self, screen):
        color = (255, 255, 255) if self.active else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)

        display_text = self.text if self.text else self.placeholder
        color_text = (0,0,0) if self.text else (150,150,150)
        
        surface = self.font.render(display_text, True, color_text)
        screen.blit(surface, (self.rect.x + 5, self.rect.y + 10))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                pass 
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode