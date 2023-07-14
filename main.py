import pygame
import math
import time
import random 
from target import Target
pygame.init()

# Font for text instances
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# Width and height of the window
WIDTH, HEIGHT = 600, 400

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Workshop")

# Height of the top navigation bar 
NAV_BAR_HEIGHT = 50

# How often a unique target will appear
TARGET_INCREMENT = 900

# Target event
TARGET_EVENT = pygame.USEREVENT

# Padding for the target so that it is always fully on the screen
TARGET_PADDING = 30

# Color of the background
BG_COLOR = (0, 25, 40)

LIVES = 3

"""
Function for drawing the targets. 
"""
def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    # Draws all of the targets that have rendered up to this point
    pygame.display.update()

def draw_stats(win, elapsed_time, targets_clicked, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, NAV_BAR_HEIGHT))
    

"""
Contains the main game loop and logic
"""
def main():
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
                run = False
                break
            
            if (event.type == TARGET_EVENT):
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            
            if (event.type == pygame.MOUSEBUTTONDOWN):
                click = True
                ++clicks

        # Updates all of the targets prior to drawing
        for target in targets:
            target.update()

            # If target is not clicked (size goes to 0), target is removed from list
            if (target.size <= 0):
                targets.remove(target)
                ++misses
            
            # If the user has clicked their mouse and collided with a target,
            # remove the target and incriment targets clicked
            if click and target.collide(mouse_pos[0], mouse_pos[1]):
                targets.remove(target)
                ++targets_clicked 

        # Ends game if misses exceeds number of lives
        if misses >= LIVES:
            pass
        
        # Draws the targets
        draw(WIN, targets)
        draw_stats(WIN, elapsed_time, targets_clicked, misses)

    pygame.quit()

if __name__ == "__main__":
    main()
