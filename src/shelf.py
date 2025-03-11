from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, SHELF_COLOR, MIN_SHELVES, MAX_SHELVES
import pygame
import random

class Shelf:
    def __init__(self, x, y, width, height, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, SHELF_COLOR, self.rect)

def generate_shelves(screen):
    shelves = []
    num_shelves = random.randint(MIN_SHELVES, MAX_SHELVES)  # Get the number from config.py

    shelf_sizes = [
        (80, 20), (20, 80),  # Small shelves
        (120, 20), (20, 120),  # Medium shelves
        (160, 20), (20, 160),  # Long shelves
        (200, 20), (20, 200),  # Extra-long shelves
        (250, 20), (20, 250)   # Super-long shelves
    ]

    max_attempts = 50  # Limit attempts to avoid infinite loops

    for _ in range(num_shelves):
        width, height = random.choice(shelf_sizes)  # Pick a random size
        attempts = 0

        while attempts < max_attempts:
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(0, SCREEN_HEIGHT - height)
            new_shelf = pygame.Rect(x, y, width, height)

            # Check if this shelf overlaps with any existing shelves
            if not any(new_shelf.colliderect(shelf.rect) for shelf in shelves):
                shelves.append(Shelf(x, y, width, height, screen))
                break  # Shelf placed successfully, exit loop

            attempts += 1

    return shelves



