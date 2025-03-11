import pygame
import random
from src.forklift import Forklift
from src.package import Package
from src.pedestrian import Pedestrian
from src.shelf import generate_shelves
from src.dropzone import DropZone
from src.config import SCREEN_HEIGHT, SCREEN_WIDTH, BG_COLOR

# Configuration Constants
INITIAL_PEDESTRIAN_SPEED = 1.5
PEDESTRIAN_INCREMENT_SPEED = 0.2
INITIAL_PEDESTRIAN_COUNT = 3
PEDESTRIAN_INCREMENT_COUNT = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


def show_game_over(score):
    screen.fill((0, 0, 0))

    # Game Over Nachricht
    game_over_text = font.render("Verloren! Drücke Enter um neu zu starten", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

    # Punktzahl anzeigen
    score_text = font.render(f"Punktzahl: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False  # Spiel neu starten

    main()  # Startet das Spiel neu


def is_position_free(x, y, forklift, shelves, pedestrians):
    forklift_rect = pygame.Rect(x, y, forklift.rect.width, forklift.rect.height)
    if any(forklift_rect.colliderect(shelf.rect) for shelf in shelves):
        return False
    if any(forklift_rect.colliderect(ped.rect) for ped in pedestrians):
        return False
    return True


import time  # Needed for timing


def draw_safety_guard_bar(screen, current_time, active, cooldown, start_time, cooldown_start, duration, cooldown_time):
    """Draws a transparent Safety Guard cooldown/loading bar."""
    bar_x = 50
    bar_y = SCREEN_HEIGHT - 30  # Position at bottom
    bar_width = SCREEN_WIDTH - 100
    bar_height = 20

    # Create a transparent surface
    bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

    # Set transparency (alpha)
    bar_surface.fill((0, 0, 0, 150))  # Black background with 150/255 transparency

    if active:
        elapsed = current_time - start_time
        progress = min(elapsed / duration, 1)  # Ensure it doesn't exceed 1
        pygame.draw.rect(bar_surface, (0, 255, 0, 200), (0, 0, progress * bar_width, bar_height))  # Green bar (Active)

    elif cooldown:
        elapsed = current_time - cooldown_start
        progress = min(elapsed / cooldown_time, 1)
        pygame.draw.rect(bar_surface, (255, 0, 0, 180), (0, 0, progress * bar_width, bar_height))  # Red bar (Cooldown)

    pygame.draw.rect(bar_surface, (255, 255, 255, 220), (0, 0, bar_width, bar_height), width=2)  # Outline

    # Blit the transparent surface onto the screen
    screen.blit(bar_surface, (bar_x, bar_y))


def main():
    level = 1
    score = 0
    safety_guard_active = False  # Safety Guard state
    safety_guard_on_cooldown = False  # Cooldown state
    SAFETY_GUARD_RADIUS = 100  # Effect radius
    SAFETY_GUARD_SLOWDOWN_FACTOR = 0.3  # Pedestrian speed reduction
    SAFETY_GUARD_FORKLIFT_SLOWDOWN = 0.4  # Forklift moves at 40% speed when active
    SAFETY_GUARD_DURATION = 4  # Active time in seconds
    SAFETY_GUARD_COOLDOWN = 10  # Cooldown time in seconds
    safety_guard_start_time = 0  # Timestamp when activated
    safety_guard_cooldown_start = 0  # Timestamp when cooldown starts

    forklift = Forklift(screen, show_game_over)
    shelves = generate_shelves(screen)
    package = Package(screen, shelves)
    drop_zone = DropZone(screen, shelves)
    pedestrians = [Pedestrian(INITIAL_PEDESTRIAN_SPEED, screen, shelves) for _ in range(INITIAL_PEDESTRIAN_COUNT)]

    running = True
    while running:
        current_time = time.time()  # Get current time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pick up/drop package
                    if not package.held and package.can_be_picked_up(forklift):
                        package.attach_to_forklift(forklift)
                    elif package.held and package.drop(drop_zone):
                        score += 1
                        package = Package(screen, shelves)
                        drop_zone = DropZone(screen, shelves)
                if event.key == pygame.K_s and not safety_guard_active and not safety_guard_on_cooldown:
                    safety_guard_active = True
                    safety_guard_start_time = current_time  # Set activation time

        # Check if Safety Guard should deactivate
        if safety_guard_active and current_time - safety_guard_start_time >= SAFETY_GUARD_DURATION:
            safety_guard_active = False
            safety_guard_on_cooldown = True
            safety_guard_cooldown_start = current_time  # Start cooldown timer

        # Check if cooldown is finished
        if safety_guard_on_cooldown and current_time - safety_guard_cooldown_start >= SAFETY_GUARD_COOLDOWN:
            safety_guard_on_cooldown = False

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Apply forklift slowdown if Safety Guard is active
        speed_factor = SAFETY_GUARD_FORKLIFT_SLOWDOWN if safety_guard_active else 1.0

        # Ensure movement does not become zero when slowing down
        adjusted_dx = dx * speed_factor
        adjusted_dy = dy * speed_factor

        if abs(adjusted_dx) < 1 and dx != 0:
            adjusted_dx = 1 if dx > 0 else -1  # Ensure movement direction is maintained

        if abs(adjusted_dy) < 1 and dy != 0:
            adjusted_dy = 1 if dy > 0 else -1  # Ensure movement direction is maintained

        forklift.move(int(adjusted_dx), int(adjusted_dy), score)

        package.update_position(forklift)

        # Apply Safety Guard effect
        for ped in pedestrians:
            if safety_guard_active and ped.is_in_safety_guard_zone(forklift, SAFETY_GUARD_RADIUS):
                ped.move(SAFETY_GUARD_SLOWDOWN_FACTOR, forklift, safety_guard_active)  # Slow movement & bounce behavior
            else:
                ped.move(1.0, forklift, safety_guard_active)

        # **Check for shelf collisions (ALWAYS lethal)**
        if any(forklift.rect.colliderect(shelf.rect) for shelf in shelves):
            show_game_over(score)
            return main()

        # **Only check for pedestrian collisions if Safety Guard is NOT active**
        if not safety_guard_active and any(forklift.rect.colliderect(ped.rect) for ped in pedestrians):
            show_game_over(score)
            return main()

        screen.fill(BG_COLOR)

        # Draw Safety Guard effect if active
        # Draw Safety Guard effect first
        if safety_guard_active:
            pygame.draw.circle(screen, (100, 100, 255, 100), forklift.rect.center, SAFETY_GUARD_RADIUS, width=2)

        # Draw all background elements first
        package.draw()
        drop_zone.draw()
        for ped in pedestrians:
            ped.draw()
        for shelf in shelves:
            shelf.draw()

        # **Always draw forklift last to ensure visibility**
        forklift.draw()

        screen.blit(font.render(f'Score: {score}', True, (255, 255, 255)), (10, 10))

        # Draw Safety Guard cooldown/loading bar
        draw_safety_guard_bar(screen, current_time, safety_guard_active, safety_guard_on_cooldown,
                              safety_guard_start_time, safety_guard_cooldown_start,
                              SAFETY_GUARD_DURATION, SAFETY_GUARD_COOLDOWN)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == '__main__':
    main()