import pygame
import random
import math  # Needed for distance calculation
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PACKAGE_COLOR

MIN_DROPZONE_DISTANCE = 50  # Minimum distance from shelves

class DropZone:
    def __init__(self, screen, shelves):
        self.screen = screen
        self.shelves = shelves
        self.rect = self.generate_valid_position()

    def generate_valid_position(self):
        """Generate a position that is not too close to a shelf."""
        size = 40  # Drop zone size
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50 - size)
            y = random.randint(50, SCREEN_HEIGHT - 50 - size)
            new_rect = pygame.Rect(x, y, size, size)

            # Ensure the drop zone is not too close to any shelf
            if all(self.get_distance(new_rect.center, shelf.rect.center) >= MIN_DROPZONE_DISTANCE for shelf in self.shelves):
                return new_rect

    def get_distance(self, pos1, pos2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def draw(self):
        pygame.draw.rect(self.screen, PACKAGE_COLOR, self.rect, width=3)  # Outlined box
