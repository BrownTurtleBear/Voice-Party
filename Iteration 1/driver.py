import pygame
import sys
from src.input.microphone_input import MicrophoneInput

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Microphone Input Example - Iteration 1")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Circle properties
circle_x, circle_y = width // 2, height // 2
min_radius, max_radius = 20, 1000

# Initialize MicrophoneInput
mic_input = MicrophoneInput(update_frequency=0.0233)

# Main game loop
clock = pygame.time.Clock()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.USEREVENT + 1:
                mic_input.update()

        # Clear the screen
        screen.fill(BLACK)

        # Get and print the current volume
        volume = mic_input.get_volume()
        print(f"Microphone volume: {volume:.2f}")

        # Calculate circle radius based on volume
        radius = min(max(int(volume), min_radius), max_radius)

        if int(volume) > 250:
            COLOUR = BLUE
        else:
            COLOUR = RED

        # Draw the circle
        pygame.draw.circle(screen, COLOUR, (circle_x, circle_y), radius)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

except KeyboardInterrupt:
    # Clean up
    mic_input.cleanup()
    pygame.quit()
    sys.exit()
