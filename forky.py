import pygame
import time
import random
from src.forklift import Forklift
from src.shelf import generate_shelves
from src.package import Package
from src.pedestrian import Pedestrian
from src.dropzone import DropZone
from src.config import *

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)


def show_game_over(score):
    screen.fill((0, 0, 0))  # Black background
    text = font.render(f"You lost! Score: {score} Press Enter to restart", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False  # Restart the game


def draw_safety_guard_bar(screen, current_time, active, on_cooldown, start_time, cooldown_start, duration, cooldown):
    """Draws a cooldown bar for the Safety Guard at the top of the screen."""
    bar_x = 10
    bar_y = 50
    bar_width = 200
    bar_height = 10
    border_color = (255, 255, 255)  # White border
    active_color = (100, 200, 255)  # Blue for active state
    cooldown_color = (150, 150, 150)  # Gray for cooldown state

    # Draw border
    pygame.draw.rect(screen, border_color, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)

    if active:
        # Calculate remaining time ratio for Safety Guard active duration
        elapsed = current_time - start_time
        ratio = max(0, 1 - elapsed / duration)
        pygame.draw.rect(screen, active_color, (bar_x, bar_y, int(bar_width * ratio), bar_height))
    elif on_cooldown:
        # Calculate cooldown progress ratio
        elapsed = current_time - cooldown_start
        ratio = max(0, 1 - elapsed / cooldown)
        pygame.draw.rect(screen, cooldown_color, (bar_x, bar_y, int(bar_width * ratio), bar_height))


def handle_events(forklift, package, drop_zone, safety_guard):
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not package.held and package.can_be_picked_up(forklift):
                    package.attach_to_forklift(forklift)
                elif package.held and package.drop(drop_zone):
                    return True
            if event.key == pygame.K_s and not safety_guard['active'] and not safety_guard['on_cooldown']:
                safety_guard['active'] = True
                safety_guard['start_time'] = current_time
    return False


def update_safety_guard(safety_guard):
    current_time = time.time()
    if safety_guard['active'] and current_time - safety_guard['start_time'] >= SAFETY_GUARD_DURATION:
        safety_guard['active'] = False
        safety_guard['on_cooldown'] = True
        safety_guard['cooldown_start'] = current_time
    if safety_guard['on_cooldown'] and current_time - safety_guard['cooldown_start'] >= SAFETY_GUARD_COOLDOWN:
        safety_guard['on_cooldown'] = False


def update_pedestrians(pedestrians, forklift, safety_guard):
    for ped in pedestrians:
        if safety_guard['active'] and ped.is_in_safety_guard_zone(forklift, SAFETY_GUARD_RADIUS):
            ped.move(SAFETY_GUARD_SLOWDOWN_FACTOR, forklift, safety_guard['active'])
        else:
            ped.move(1.0, forklift, safety_guard['active'])


def main():
    while True:
        score = 0
        safety_guard = {'active': False, 'on_cooldown': False, 'start_time': 0, 'cooldown_start': 0}
        shelves = generate_shelves(screen)
        forklift = Forklift(screen, show_game_over, shelves)
        package = Package(screen, shelves)
        drop_zone = DropZone(screen, shelves)
        pedestrians = [Pedestrian(INITIAL_PEDESTRIAN_SPEED, screen, shelves, forklift) for _ in range(INITIAL_PEDESTRIAN_COUNT)]
        running = True

        while running:
            if handle_events(forklift, package, drop_zone, safety_guard):
                score += 1
                package = Package(screen, shelves)
                drop_zone = DropZone(screen, shelves)

                # create new pedestrian with level up
                pedestrians.append(Pedestrian(INITIAL_PEDESTRIAN_SPEED, screen, shelves, forklift))

            update_safety_guard(safety_guard)
            update_pedestrians(pedestrians, forklift, safety_guard)

            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            # Apply forklift slowdown if Safety Guard is active
            speed_factor = SAFETY_GUARD_FORKLIFT_SLOWDOWN if safety_guard['active'] else 1.0

            # Ensure movement does not become zero when slowing down
            adjusted_dx = max(1, abs(int(dx * speed_factor))) * (1 if dx > 0 else -1) if dx != 0 else 0
            adjusted_dy = max(1, abs(int(dy * speed_factor))) * (1 if dy > 0 else -1) if dy != 0 else 0
            forklift.move(int(adjusted_dx), int(adjusted_dy), score)
            package.update_position(forklift)

            if any(forklift.rect.colliderect(shelf.rect) for shelf in shelves):
                show_game_over(score)
                break
            if not safety_guard['active'] and any(forklift.rect.colliderect(ped.rect) for ped in pedestrians):
                show_game_over(score)
                break

            screen.fill(BG_COLOR)
            if safety_guard['active']:
                pygame.draw.circle(screen, (100, 100, 255, 100), forklift.rect.center, SAFETY_GUARD_RADIUS, width=2)
            package.draw()
            drop_zone.draw()
            for ped in pedestrians:
                ped.draw()
            for shelf in shelves:
                shelf.draw()
            forklift.draw()
            screen.blit(font.render(f'Score: {score}', True, (255, 255, 255)), (10, 10))
            draw_safety_guard_bar(screen, time.time(), safety_guard['active'], safety_guard['on_cooldown'],
                                  safety_guard['start_time'], safety_guard['cooldown_start'],
                                  SAFETY_GUARD_DURATION, SAFETY_GUARD_COOLDOWN)
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    main()
