import pygame
from game import Game
from display import Display

def main():
    pygame.init()
    display = Display(800, 600)
    game = None
    menu = Menu()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left mouse button
                        if game.game_over:
                            game.reset()
                        else:
                            game.handle_click(pygame.mouse.get_pos())
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left mouse button
                        difficulty = menu.handle_click(pygame.mouse.get_pos())
                        if difficulty:
                            game = Game(difficulty)

        display.clear()
        if game:
            game.update()
            game.draw(display.screen)
        else:
            menu.draw(display.screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title = self.font.render("Memory Match Game", True, (255, 255, 255))
        self.easy = self.font.render("Easy (4x4)", True, (255, 255, 255))
        self.medium = self.font.render("Medium (6x6)", True, (255, 255, 255))
        self.hard = self.font.render("Hard (8x8)", True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.title, (300, 100))
        screen.blit(self.easy, (350, 200))
        screen.blit(self.medium, (350, 250))
        screen.blit(self.hard, (350, 300))

    def handle_click(self, pos):
        if 350 <= pos[0] <= 450:
            if 200 <= pos[1] <= 236:
                return 4  # easy
            elif 250 <= pos[1] <= 286:
                return 6  # medium
            elif 300 <= pos[1] <= 336:
                return 8  # hard
        return None

if __name__ == "__main__":
    main()