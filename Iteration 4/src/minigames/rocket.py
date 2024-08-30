import sys

from elements.text import Text
from input.microphone import *
from sprite.spriteSheet import SpriteSheet
from sprite.sprites import RocketSprite
from view.gamecams import RocketCamera


def run(screen):
    speed = 0
    mic_input = MicrophoneInput(0.0233)

    rocket_image = pygame.image.load("assets/rocket/images/rocket.png").convert_alpha()
    rocket_sheet = SpriteSheet(rocket_image)
    rocket = RocketSprite(400, 500, rocket_sheet, 0, 1.3)

    camera = RocketCamera()
    camera.add(rocket)

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
            if speed < 0.5:
                speed = 0.4
            speed = rocket.move(speed)

            t_rocket_speed = Text(screen, "Garamond", 100, 100, 50,
                                  (255, 255, 255), str(speed))

            screen.fill((0, 0, 0))

            camera.custom_draw(rocket)

            t_rocket_speed.show()

            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        mic_input.cleanup()
        pygame.quit()
        sys.exit()
