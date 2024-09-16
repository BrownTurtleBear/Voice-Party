import math
import pygame
import random
import os

from sprite.baseSprite import BaseSprite
from sprite.spriteSheet import SpriteSheet


class RocketSprite(BaseSprite):
    def __init__(self):
        self.image = pygame.image.load("assets/rocket/images/rocket.png").convert_alpha()
        self.sheet = SpriteSheet(self.image)
        self.current_frame = 0
        self.frames = [self.sheet.get_image(frame, 32, 32, 4) for frame in range(8)]
        rocket = self.frames[self.current_frame]
        rocket = pygame.transform.scale(rocket, (
            int(rocket.get_width() * 1.3), int(rocket.get_height() * 1.3)))

        screen_width, screen_height = pygame.display.get_surface().get_size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        self.pos = [center_x, center_y]

        super().__init__(self.pos[0], self.pos[1], rocket)
        self.angle = 0
        self.rotation_speed = 3
        self.scale_factor = 1.3

    def rotate_left(self):
        self.angle += self.rotation_speed
        self.rotate()

    def rotate_right(self):
        self.angle -= self.rotation_speed
        self.rotate()

    def rotate(self):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.pos)

    def update_frame(self, speed):
        self.current_frame = min(math.trunc(speed), len(self.frames) - 1)
        self.original_image = self.frames[self.current_frame]
        self.original_image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * self.scale_factor),
            int(self.original_image.get_height() * self.scale_factor)))
        self.rotate()

    def move(self, speed):
        min_x, max_x = -1800, 1800
        min_y, max_y = -1800, 1800

        min_speed = 0.5
        max_speed = 7

        rocket_speed = min(max(speed, min_speed), max_speed)
        if speed < min_speed:
            rocket_speed = 0

        angle_rad = math.radians(self.angle)
        new_x = self.pos[0] - rocket_speed * math.sin(angle_rad)
        new_y = self.pos[1] - rocket_speed * math.cos(angle_rad)

        self.pos[0] = max(min_x, min(new_x, max_x))
        self.pos[1] = max(min_y, min(new_y, max_y))

        self.rect.center = self.pos
        self.update_frame(round(rocket_speed))

        return rocket_speed


class AsteroidSprite(BaseSprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.image = pygame.image.load("assets/rocket/images/asteroid.png").convert_alpha()
        self.sheet = SpriteSheet(self.image)
        self.current_frame = 0
        self.frames = [self.sheet.get_image(frame, 16, 16, 3) for frame in range(8)]
        asteroid = self.frames[self.current_frame]
        asteroid = pygame.transform.scale(asteroid, (
            int(asteroid.get_width() * 1.3), int(asteroid.get_height() * 1.3)))

        self.image = asteroid
        self.rect = self.image.get_rect()
        self.true_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.rect.center = self.true_pos

        self.collision = True

        self.rotation = 0
        self.rotation_type = random.choice(["Clockwise", "Anti-Clockwise"])
        self.rotation_speed = random.uniform(0.5, 2)

        self.speed = random.uniform(0.5, 3)

    def rotate(self):
        if self.rotation_type == "Clockwise":
            self.rotation += self.rotation_speed
        else:
            self.rotation -= self.rotation_speed

        self.image = pygame.transform.rotate(self.frames[self.current_frame], self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, camera_offset):
        self.rotate()

        self.rect.center = self.true_pos - camera_offset


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        # Load the original bullet image
        load_image = pygame.image.load("assets/rocket/images/bullets.png").convert_alpha()
        scaled_image = pygame.transform.scale(load_image, (128, 128))
        self.original_image = pygame.transform.rotate(scaled_image, angle)
        self.image = self.original_image  # Start with the normal image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.angle = angle
        self.pos = pygame.math.Vector2(x, y)

    def update(self):
        # Movement logic remains the same
        angle_rad = math.radians(self.angle)
        movement = pygame.math.Vector2(-self.speed * math.sin(angle_rad), -self.speed * math.cos(angle_rad))
        self.pos += movement
        self.rect.center = self.pos

        # Off-screen check
        if self.rect.left < -2000 or self.rect.right > 2000 or self.rect.top < -2000 or self.rect.bottom > 2000:
            self.kill()


def is_in_viewport(screen_pos, screen_width, screen_height):
    margin = 100  # Margin around the screen to keep bullets visible when near the edge
    return (-margin < screen_pos[0] < screen_width + margin and
            -margin < screen_pos[1] < screen_height + margin)


def draw_normal_bullet(surface, bullet, screen_pos):
    surface.blit(bullet.original_image, screen_pos)


def draw_debug_bullet(surface, bullet, screen_pos):
    small_font = pygame.font.Font(None, 20)

    # Draw green debug circle
    debug_bullet_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    pygame.draw.circle(debug_bullet_surface, (0, 255, 0), (32, 32), 10)
    surface.blit(debug_bullet_surface, screen_pos)

    # Display bullet position
    x_pos, y_pos = round(bullet.pos.x), round(bullet.pos.y)
    position_text = small_font.render(f"({x_pos}, {y_pos})", True, (255, 255, 255))
    text_pos = (screen_pos[0] + 20, screen_pos[1] - 10)
    surface.blit(position_text, text_pos)


class BulletManager(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.camera_offset = pygame.math.Vector2(0, 0)

    def shoot(self, x, y, angle):
        bullet_offset_distance = 40

        angle_rad = math.radians(angle)

        bullet_x = x - bullet_offset_distance * math.sin(angle_rad)
        bullet_y = y - bullet_offset_distance * math.cos(angle_rad)

        new_bullet = Bullet(bullet_x, bullet_y, angle)
        self.add(new_bullet)

    def update(self):
        for bullet in self.sprites():
            bullet.update()
        # print(f"BulletManager updated. Total bullets: {len(self.sprites())}")

    def draw(self, surface, debug_mode=False):
        screen_width, screen_height = surface.get_size()

        for bullet in self.sprites():
            screen_pos = bullet.rect.topleft - self.camera_offset

            # Only draw if the bullet is within the screen bounds (with margin)
            if is_in_viewport(screen_pos, screen_width, screen_height):
                if debug_mode:
                    draw_debug_bullet(surface, bullet, screen_pos)
                else:
                    draw_normal_bullet(surface, bullet, screen_pos)

    def set_camera_offset(self, offset):
        self.camera_offset = offset
