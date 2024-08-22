import pygame
import math

from sprite.baseSprite import BaseSprite


class RocketSprite(BaseSprite):
    def __init__(self, x, y, sheet, initial_frame):
        self.sheet = sheet
        self.current_frame = initial_frame
        self.frames = [self.sheet.get_image(frame, 32, 32, 3) for frame in range(8)]
        rocket = self.frames[self.current_frame]
        super().__init__(x, y, rocket)
        self.angle = 0
        self.rotation_speed = 3

    def rotate_left(self):
        self.angle += self.rotation_speed
        self.rotate()

    def rotate_right(self):
        self.angle -= self.rotation_speed
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_frame(self, speed):
        self.current_frame = math.trunc(speed)
        self.original_image = self.frames[self.current_frame]
        self.rotate()

    def move(self, speed):
        rocket_speed = 0
        min_speed = 2
        max_speed = 7

        if speed > max_speed:
            rocket_speed = max_speed
        if speed < min_speed:
            rocket_speed = 0
        if min_speed <= speed <= max_speed:
            rocket_speed = speed

        angle_rad = math.radians(self.angle)
        self.rect.x -= rocket_speed * math.sin(angle_rad)
        self.rect.y -= rocket_speed * math.cos(angle_rad)

        self.update_frame(round(rocket_speed))

        return speed
