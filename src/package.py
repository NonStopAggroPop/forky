import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PACKAGE_COLOR

class Package:
    def __init__(self, screen, shelves):
        self.screen = screen
        self.shelves = shelves
        self.held = False  # Wird das Paket gerade transportiert?
        self.rect = self.generate_valid_position()

    def generate_valid_position(self):
        """Generiert eine valide Position für das Paket (nicht zu nah an den Shelves)."""
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            new_rect = pygame.Rect(x, y, 20, 20)

            # Mindestabstand zu Shelves
            if all(new_rect.colliderect(shelf.rect) == False for shelf in self.shelves):
                return new_rect

    def attach_to_forklift(self, forklift):
        """Das Paket wird an die Gabel geheftet."""
        self.held = True
        self.rect.x = forklift.rect.centerx - 10
        self.rect.y = forklift.rect.y - 25  # Direkt vor die Gabel setzen

    def update_position(self, forklift):
        """Wenn das Paket gehalten wird, bleibt es immer vorne an den Gabeln."""
        if self.held:
            if forklift.direction == (0, -1):  # Nach oben
                self.rect.x = forklift.rect.centerx - self.rect.width // 2
                self.rect.y = forklift.rect.top - self.rect.height
            elif forklift.direction == (0, 1):  # Nach unten
                self.rect.x = forklift.rect.centerx - self.rect.width // 2
                self.rect.y = forklift.rect.bottom
            elif forklift.direction == (-1, 0):  # Nach links
                self.rect.x = forklift.rect.left - self.rect.width
                self.rect.y = forklift.rect.centery - self.rect.height // 2
            elif forklift.direction == (1, 0):  # Nach rechts
                self.rect.x = forklift.rect.right
                self.rect.y = forklift.rect.centery - self.rect.height // 2

    def drop(self, drop_zone):
        """Prüft, ob das Paket in der DropZone abgelegt werden kann."""
        if self.held and self.rect.colliderect(drop_zone.rect):
            self.held = False
            return True  # Paket erfolgreich abgelegt
        return False

    def draw(self):
        pygame.draw.rect(self.screen, PACKAGE_COLOR, self.rect)

    def can_be_picked_up(self, forklift, tolerance=10):
        """Überprüft, ob das Paket in Reichweite des Forklifts ist (mit Toleranz)."""
        extended_rect = forklift.rect.inflate(tolerance, tolerance)  # Vergrößert die Hitbox des Forklifts
        return extended_rect.colliderect(self.rect)

