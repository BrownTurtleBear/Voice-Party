import sys
import pygame
from input.microphone import MicrophoneInput
from sprite.sprites import RocketSprite, BulletManager
from view.gamecams import RocketCamera

pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
INITIAL_SPEED = 0
SPEED_INCREMENT = 0.5
MIN_SPEED = 0.4
MAX_SPEED = 7

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Game - Iteration 4")
clock = pygame.time.Clock()

# Initialize game components
speed = INITIAL_SPEED
mic_input = MicrophoneInput(0.0233)
rocket = RocketSprite()
bullet_manager = BulletManager()
camera = RocketCamera()

# Add rocket and bullet manager to camera
camera.add(rocket)

debug_font = pygame.font.Font(None, 36)

# Debug toggle
debug_mode = False


# Helper functions
def handle_input():
    global speed, running
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket.rotate_left()
    if keys[pygame.K_RIGHT]:
        rocket.rotate_right()
    if keys[pygame.K_w]:
        speed += SPEED_INCREMENT
    if keys[pygame.K_s]:
        speed -= SPEED_INCREMENT
    speed = max(MIN_SPEED, min(speed, MAX_SPEED))  # Constrain speed


def toggle_debug(board):
    global debug_mode
    if board.key == pygame.K_d:
        debug_mode = not debug_mode


def draw_debug_info():
    debug_text = debug_font.render(f"Bullets: {len(bullet_manager.sprites())}", True, (255, 255, 255))
    screen.blit(debug_text, (10, 10))

    rocket_speed_text = debug_font.render(f"Speed: {speed:.2f}", True, (255, 255, 255))
    screen.blit(rocket_speed_text, (10, 40))

    rocket_position_text = debug_font.render(f"Position: {rocket.rect.center}", True, (255, 255, 255))
    screen.blit(rocket_position_text, (10, 70))

    fps = clock.get_fps()
    fps_text = debug_font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 100))


def draw_bullets(surface):
    for bullet in bullet_manager.sprites():
        screen_pos = bullet.rect.topleft - camera.offset
        surface.blit(bullet.image, screen_pos)


running = True

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.USEREVENT + 1:
                mic_input.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    bullet_manager.shoot(rocket.rect.centerx, rocket.rect.centery, rocket.angle)
                elif event.key == pygame.K_F3:
                    debug_mode = not debug_mode

        # Handle input
        handle_input()

        # Update game state
        speed = rocket.move(speed)
        camera.update()
        bullet_manager.update()

        bullet_manager.set_camera_offset(camera.offset)

        screen.fill((0, 0, 0))

        # Draw Sprites
        camera.custom_draw(rocket)

        bullet_manager.draw(screen, debug_mode)

        if debug_mode:
            draw_debug_info()

        fps = clock.get_fps()
        fps_text = debug_font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 100))

        pygame.display.flip()
        clock.tick(FPS)


except KeyboardInterrupt:
    mic_input.cleanup()
    pygame.quit()
    sys.exit()
