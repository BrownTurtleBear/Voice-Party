import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
