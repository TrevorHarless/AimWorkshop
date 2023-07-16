import pygame
import time
import random
from target import Target
from utils import draw, draw_nav_bar, NAV_BAR_HEIGHT
import main as main

# How often a unique target will appear
TARGET_INCREMENT = 300

# Target event
TARGET_EVENT = pygame.USEREVENT

# Padding for the target so that it is always fully on the screen
TARGET_PADDING = 30

# Number of lives
LIVES = 3

def radiating_targets(WIN, HEIGHT, WIDTH, options):
    run = True

    targets = []

    clock = pygame.time.Clock()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    targets_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    # Game loop
    while run:
        # Sets framerate to 60 // How fast the while loop will run
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit()
            
            if (event.type == TARGET_EVENT):
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, 0)
                # TODO: May need to change color here
                targets.append(target)
            
            if (event.type == pygame.MOUSEBUTTONDOWN):
                click = True
                clicks += 1

        # Updates all of the targets prior to drawing
        for target in targets:
            target.update()

            # If target is not clicked (size goes to 0), target is removed from list
            if (target.size <= 0):
                targets.remove(target)
                misses += 1
            
            # If the user has clicked their mouse and collided with a target,
            # remove the target and incriment targets clicked
            if click and target.collide(mouse_pos[0], mouse_pos[1]):
                targets.remove(target)
                targets_clicked += 1

        # Ends game if misses exceeds number of lives
        if misses >= LIVES:
            main.end_screen(elapsed_time, targets_clicked, clicks, options)

        # Draws the targets
        draw(WIN, targets, options)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses)
        pygame.display.update()