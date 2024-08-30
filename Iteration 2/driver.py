import pygame
import sys

from elements import text
from minigames import rocket, dodge

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Voice Party - Iteration 2")

MENU = 0
ROCKET = 1
DODGE = 2

t_main = text.Text(screen, "Garamond", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, (255, 255, 255),
                   "Main Menu")
tb_rocket = text.Text(screen, "Garamond", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 40, (255, 0, 0),
                      "Rocket Game", is_button=True)
tb_dodge = text.Text(screen, "Garamond", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130, 40, (0, 255, 0),
                     "Dodge Game", is_button=True)

text_buttons = [tb_rocket, tb_dodge]


class Game:
    def __init__(self):
        self.state = MENU

    def run(self):
        while True:
            if self.state == MENU:
                self.menu()
            elif self.state == ROCKET:
                rocket.run(screen)
                self.state = MENU
            elif self.state == DODGE:
                dodge.run(screen)
                self.state = MENU

    def menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for button in text_buttons:
                    if button.check(event):
                        if button == tb_rocket:
                            self.state = ROCKET
                            return
                        elif button == tb_dodge:
                            self.state = DODGE
                            return

            screen.fill((0, 0, 0))
            t_main.show()
            for button in text_buttons:
                button.show()
            pygame.display.flip()

            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    game = Game()
    game.run()
