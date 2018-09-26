import pygame


class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False
        self.last_pos = None

    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def draw(self, pos):
        if self.drawing:
            pygame.draw.line(self.screen, self.color, self.last_pos, pos, self.size * 2)
            self.last_pos = pos


class Text:
    def __init__(self, position, content):
        pygame.font.init()
        self.content = content
        self.position = position
        self.my_font = pygame.font.SysFont("arial", 16)
        self.text_surface = self.my_font.render(self.content, True, (0, 0, 0))

    def display_text(self, screen):
        x, y = self.position
        screen.blit(self.text_surface, (x, y))
