import pygame


class Camera:
    def __init__(self, width, height):
        self.background_image = None
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def update(self, rocket_x, rocket_y):
        self.x = rocket_x - self.width // 2
        self.y = rocket_y - self.height // 2

    def apply(self, screen):
        screen.fill((0, 0, 0))  # clear the screen
        screen.blit(self.background_image, (-self.x, -self.y))

    def load_background(self, path):
        self.background_image = pygame.image.load(path).convert()
