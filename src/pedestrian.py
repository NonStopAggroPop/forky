import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PEDESTRIAN_COLOR

class Pedestrian:
    def __init__(self, speed, screen, shelves, forklift):
        self.screen = screen
        self.shelves = shelves  # Store shelves for collision checking
        self.speed = speed
        self.rect = self.generate_valid_position(forklift)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def generate_valid_position(self, forklift):
        """Finds a valid position that does not collide with shelves or the forklift."""
        while True:
            x = random.randint(20, SCREEN_WIDTH - 20)
            y = random.randint(20, SCREEN_HEIGHT - 20)
            new_rect = pygame.Rect(x, y, 20, 20)

            if all(not new_rect.colliderect(shelf.rect) for shelf in self.shelves) and \
               not new_rect.colliderect(forklift.rect):
                return new_rect

    def is_in_safety_guard_zone(self, forklift, radius):
        """Check if the pedestrian is inside the Safety Guard zone."""
        distance = math.sqrt((self.rect.centerx - forklift.rect.centerx) ** 2 +
                             (self.rect.centery - forklift.rect.centery) ** 2)
        return distance <= radius

    def move(self, speed_factor=1.0, forklift=None, safety_guard_active=False):
        """Moves the pedestrian, applying a slowdown if needed. Bounces off obstacles if necessary."""
        if random.random() < 0.1:  # Increase direction change probability from 2% to 10%
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        # Apply slowdown effect if active
        speed = self.speed * speed_factor
        new_x = self.rect.x + self.direction[0] * speed
        new_y = self.rect.y + self.direction[1] * speed

        # **Check collisions before moving**
        new_rect_x = pygame.Rect(new_x, self.rect.y, self.rect.width, self.rect.height)
        new_rect_y = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)

        # **Prevent moving off-screen**
        if new_x < 0 or new_x + self.rect.width > SCREEN_WIDTH or any(
                new_rect_x.colliderect(shelf.rect) for shelf in self.shelves):
            self.direction = (-self.direction[0], self.direction[1])  # Reverse X direction
        else:
            self.rect.x = new_x  # Only update X if it's a valid move

        if new_y < 0 or new_y + self.rect.height > SCREEN_HEIGHT or any(
                new_rect_y.colliderect(shelf.rect) for shelf in self.shelves):
            self.direction = (self.direction[0], -self.direction[1])  # Reverse Y direction
        else:
            self.rect.y = new_y  # Only update Y if it's a valid move


    def draw(self):
        pygame.draw.rect(self.screen, PEDESTRIAN_COLOR, self.rect)
