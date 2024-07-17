import pygame
import random
import time
import os

pygame.init()
pygame.mixer.init()

class Card:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.revealed = False
        self.matched = False
        self.width = 80
        self.height = 120
        self.back_color = (200, 200, 200)
        self.flip_progress = 0
        self.flipping = False

    def draw(self, screen):
        if self.flipping:
            progress = self.flip_progress / 10
            if progress < 0.5:
                color = self.back_color
                width = int(self.width * (1 - progress * 2))
            else:
                color = self.color
                width = int(self.width * ((progress - 0.5) * 2))
            height = self.height
            pygame.draw.rect(screen, color, (self.x + (self.width - width) // 2, self.y, width, height))
        elif self.matched or self.revealed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.back_color, (self.x, self.y, self.width, self.height))

        # border
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def flip(self):
        self.flipping = True
        self.flip_progress = 0

    def update_flip(self):
        if self.flipping:
            self.flip_progress += 1
            if self.flip_progress >= 10:
                self.flipping = False
                self.revealed = not self.revealed

class Game:
    def __init__(self, size):
        self.rows = size
        self.cols = size
        self.cards = []
        self.generate_cards()
        self.first_card = None
        self.second_card = None
        self.can_click = True
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 36)
        self.game_over = False

        # background image
        self.background = pygame.image.load(os.path.join('images', 'background.jpg'))
        self.background = pygame.transform.scale(self.background, (800, 600))

        # sound effects
        self.flip_sound = pygame.mixer.Sound(os.path.join('sounds', 'flip.mp3'))
        self.match_sound = pygame.mixer.Sound(os.path.join('sounds', 'match.mp3'))
        self.no_match_sound = pygame.mixer.Sound(os.path.join('sounds', 'failed.mp3'))

    def generate_cards(self):
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Purple
            (0, 128, 0),    # Dark Green
            (128, 128, 255),# Light Blue
            (255, 128, 128),# Pink
            (128, 64, 0),   # Brown
            (0, 128, 128),  # Teal
            (128, 128, 0),  # Olive
            (255, 192, 203),# Light Pink
            (64, 224, 208)  # Turquoise
        ]
        values = colors[:((self.rows * self.cols) // 2)] * 2
        random.shuffle(values)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * 100 + 50
                y = i * 140 + 50
                self.cards.append(Card(values.pop(), x, y))

    def handle_click(self, pos):
        if not self.can_click or self.game_over:
            return

        for card in self.cards:
            if self.is_card_clicked(card, pos):
                if not card.revealed and not card.matched:
                    card.flip()
                    self.flip_sound.play()
                    if self.first_card is None:
                        self.first_card = card
                    elif self.second_card is None:
                        self.second_card = card
                        self.can_click = False
                break

    def is_card_clicked(self, card, pos):
        return (card.x <= pos[0] <= card.x + card.width and
                card.y <= pos[1] <= card.y + card.height)

    def update(self):
        for card in self.cards:
            card.update_flip()

        if self.first_card and self.second_card and not self.first_card.flipping and not self.second_card.flipping:
            self.moves += 1
            if self.first_card.color == self.second_card.color:
                self.first_card.matched = True
                self.second_card.matched = True
                self.score += 10
                self.match_sound.play()
            else:
                pygame.time.wait(500)
                self.first_card.flip()
                self.second_card.flip()
                self.score -= 1
                self.no_match_sound.play()
            
            self.first_card = None
            self.second_card = None
            self.can_click = True

        if all(card.matched for card in self.cards):
            self.game_over = True

    def draw(self, screen):
        # background
        screen.blit(self.background, (0, 0))

        for card in self.cards:
            card.draw(screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        moves_text = self.font.render(f"Moves: {self.moves}", True, (255, 255, 255))
        time_text = self.font.render(f"Time: {int(time.time() - self.start_time)}s", True, (255, 255, 255))
        
        screen.blit(score_text, (10, 10))
        screen.blit(moves_text, (10, 50))
        screen.blit(time_text, (10, 90))

        if self.game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("Game Over!", True, (255, 255, 255))
            final_score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            play_again_text = self.font.render("Click to Return to Menu", True, (255, 255, 255))

            screen.blit(game_over_text, (350, 250))
            screen.blit(final_score_text, (350, 300))
            screen.blit(play_again_text, (300, 350))

    def reset(self):
        self.__init__(self.rows)
