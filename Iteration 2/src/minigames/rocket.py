import sys

from input.microphone import *
from elements.text import Text
from sprite.sprites import RocketSprite
from sprite.spriteSheet import SpriteSheet


def run(screen):
    speed = 0
    mic_input = MicrophoneInput(0.0233)

    screen_center = screen.get_rect().center
    t_rocket_game = Text(screen, "Garamond", screen_center[0], screen_center[1], 50,
                         (255, 255, 255), "Rocket Game")

    rocket_image = pygame.image.load("assets/rocket/images/rocket.png").convert_alpha()
    rocket_sheet = SpriteSheet(rocket_image)
    rocket = RocketSprite(400, 500, rocket_sheet, 0)

    boundary_rect = pygame.Rect(50, 50, 700, 500)

    running = True
    clock = pygame.time.Clock()

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt
                elif event.type == pygame.USEREVENT + 1:
                    mic_input.update()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            # volume = mic_input.get_volume()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                rocket.rotate_left()
            if keys[pygame.K_RIGHT]:
                rocket.rotate_right()
            if keys[pygame.K_w]:
                speed += 0.5
            if keys[pygame.K_s]:
                speed -= 0.5
            if speed > 7:
                speed = 7
            if speed < 2:
                speed = 1.9999
            speed = rocket.move(speed)

            t_rocket_speed = Text(screen, "Garamond", 100, 100, 50,
                                  (255, 255, 255), str(speed))

            screen.fill((0, 0, 0))

            t_rocket_game.show()
            t_rocket_speed.show()

            rocket.draw(screen)
            rocket.rect.clamp_ip(boundary_rect)

            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        mic_input.cleanup()
        pygame.quit()
        sys.exit()
