import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FORKLIFT_COLOR, FORKLIFT_SPEED


class Forklift:
    def __init__(self, screen, game_over_callback, shelves):
        self.screen = screen
        self.game_over_callback = game_over_callback

        # ✅ Ensure forklift spawns in a valid position
        self.rect = self.get_valid_spawn_position(shelves)
        self.direction = (0, -1)

    def get_valid_spawn_position(self, shelves):
        """Finds a valid spawn position that does not collide with shelves."""
        while True:
            rect = pygame.Rect(
                random.randint(50, SCREEN_WIDTH - 90),
                random.randint(50, SCREEN_HEIGHT - 90),
                40, 40
            )
            if not any(rect.colliderect(shelf.rect) for shelf in shelves):
                return rect

    def move(self, dx, dy, score):
        if dx != 0 and dy != 0:
            if dx != 0:
                dy = 0
            else:
                dx = 0

        if dx != 0 or dy != 0:
            self.direction = (int(dx / abs(dx)) if dx != 0 else 0, int(dy / abs(dy)) if dy != 0 else 0)

            new_x = self.rect.x + dx * FORKLIFT_SPEED
            new_y = self.rect.y + dy * FORKLIFT_SPEED

            # Always end game if the Forklift hits the screen border, even during Safety Guard
            if new_x < 0 or new_x + self.rect.width > SCREEN_WIDTH or new_y < 0 or new_y + self.rect.height > SCREEN_HEIGHT:
                self.game_over_callback(score)  # Game Over
                return

            # Move only if not hitting the border
            self.rect.x = new_x
            self.rect.y = new_y

    def draw(self):
        pygame.draw.rect(self.screen, FORKLIFT_COLOR, self.rect)

        fork_width, fork_height = 5, 15
        left_fork, right_fork = None, None

        if self.direction == (0, -1):  # Up
            left_fork = pygame.Rect(self.rect.x + 8, self.rect.y - fork_height, fork_width, fork_height)
            right_fork = pygame.Rect(self.rect.x + self.rect.width - 13, self.rect.y - fork_height, fork_width,
                                     fork_height)
        elif self.direction == (0, 1):  # Down
            left_fork = pygame.Rect(self.rect.x + 8, self.rect.y + self.rect.height, fork_width, fork_height)
            right_fork = pygame.Rect(self.rect.x + self.rect.width - 13, self.rect.y + self.rect.height, fork_width,
                                     fork_height)
        elif self.direction == (-1, 0):  # Left
            left_fork = pygame.Rect(self.rect.x - fork_height, self.rect.y + 8, fork_height, fork_width)
            right_fork = pygame.Rect(self.rect.x - fork_height, self.rect.y + self.rect.height - 13, fork_height,
                                     fork_width)
        elif self.direction == (1, 0):  # Right
            left_fork = pygame.Rect(self.rect.x + self.rect.width, self.rect.y + 8, fork_height, fork_width)
            right_fork = pygame.Rect(self.rect.x + self.rect.width, self.rect.y + self.rect.height - 13, fork_height,
                                     fork_width)

        if left_fork and right_fork:
            pygame.draw.rect(self.screen, FORKLIFT_COLOR, left_fork)
            pygame.draw.rect(self.screen, FORKLIFT_COLOR, right_fork)
