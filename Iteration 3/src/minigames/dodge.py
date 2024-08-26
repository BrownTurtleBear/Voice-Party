import pygame
import sys
from input.microphone import *
from elements.text import Text


def run(screen):
    mic_input = MicrophoneInput(0.0233)

    screen_center = screen.get_rect().center
    t_rocket_game = Text(screen, "Garamond", screen_center[0], screen_center[1], 50, (0, 0, 0), "Dodge Game")

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

            volume = mic_input.get_volume()

            screen.fill((255, 255, 255))

            t_rocket_game.show()

            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        # Clean up
        mic_input.cleanup()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Adjust size as needed
    pygame.display.set_caption("Dodge")
    run(screen)
