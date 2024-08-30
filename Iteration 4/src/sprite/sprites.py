import math
import pygame

from sprite.baseSprite import BaseSprite


class RocketSprite(BaseSprite):
    def __init__(self, x, y, sheet, initial_frame, scale_factor=1.0):
        self.sheet = sheet
        self.current_frame = initial_frame
        self.frames = [self.sheet.get_image(frame, 32, 32, 3) for frame in range(8)]
        rocket = self.frames[self.current_frame]
        rocket = pygame.transform.scale(rocket, (
            int(rocket.get_width() * scale_factor), int(rocket.get_height() * scale_factor)))
        self.pos = [0, 0]

        super().__init__(x, y, rocket)
        self.angle = 0
        self.rotation_speed = 3
        self.scale_factor = scale_factor

    def rotate_left(self):
        self.angle += self.rotation_speed
        self.rotate()

    def rotate_right(self):
        self.angle -= self.rotation_speed
        self.rotate()

    def rotate(self):
        # Apply rotation and scaling
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        scaled_image = pygame.transform.scale(rotated_image, (
            int(rotated_image.get_width() * self.scale_factor), int(rotated_image.get_height() * self.scale_factor)))

        self.image = scaled_image
        self.rect = self.image.get_rect(center=self.pos)

    def update_frame(self, speed):
        self.current_frame = math.trunc(speed)
        self.original_image = self.frames[self.current_frame]
        self.original_image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * self.scale_factor),
            int(self.original_image.get_height() * self.scale_factor)))
        self.rotate()

    def move(self, speed):
        rocket_speed = 0
        min_speed = 0.5
        max_speed = 7

        if speed > max_speed:
            rocket_speed = max_speed
        if speed < min_speed:
            rocket_speed = 0
        if min_speed <= speed <= max_speed:
            rocket_speed = speed

        angle_rad = math.radians(self.angle)
        self.pos[0] -= rocket_speed * math.sin(angle_rad)
        self.pos[1] -= rocket_speed * math.cos(angle_rad)
        self.rect.center = self.pos
        self.update_frame(round(rocket_speed))

        return speed


class AsteroidSprite(BaseSprite):
    def __init__(self, x, y, sheet, initial_frame, scale_factor=1.0):
        self.sheet = sheet
        self.current_frame = initial_frame
        self.frames = [self.sheet.get_image(frame, 32, 32, 3) for frame in range(8)]
        asteroid = self.frames[self.current_frame]
        asteroid = pygame.transform.scale(asteroid, (
            int(asteroid.get_width() * scale_factor), int(asteroid.get_height() * scale_factor)))

        super().__init__(x, y, asteroid)
