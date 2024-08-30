import os

import pygame


class Text:
    def __init__(self, screen, font, x_pos, y_pos, size, colour, text, is_button=False):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        font_path = os.path.join(base_dir, "assets", "fonts", f"{font}.ttf")

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"The font file at {font_path} does not exist.")

        self.font = pygame.font.Font(font_path, size)
        self.text_string = text
        self.text = self.font.render(text, True, colour)
        self.text_rect = self.text.get_rect(center=(x_pos, y_pos))
        self.screen = screen
        self.colour = colour
        self.is_button = is_button
        self.pressed = False
        self.hover = False

    def show(self):
        if self.is_button and self.hover:
            hover_colour = tuple(max(0, c - 30) for c in self.colour)
            hover_text = self.font.render(self.text_string, True, hover_colour)
            self.screen.blit(hover_text, self.text_rect)
        else:
            self.screen.blit(self.text, self.text_rect)

    def check(self, event):
        if self.is_button:
            mouse_pos = pygame.mouse.get_pos()
            self.hover = self.text_rect.collidepoint(mouse_pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hover:
                    self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.hover and self.pressed:
                    self.pressed = False
                    return True
                self.pressed = False
        return False
