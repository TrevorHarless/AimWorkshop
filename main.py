import pygame
import math
import time
import random 
from target import Target
pygame.init()

# Font for text instances
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# Width and height of the window
WIDTH, HEIGHT = 1200, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Workshop")

# Height of the top navigation bar 
NAV_BAR_HEIGHT = 50

# How often a unique target will appear
TARGET_INCREMENT = 500

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

# Returns a neatly formatted time with minutes, seconds, and milliseconds
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000 / 100))
    seconds = int(round(secs % 60, 1))
    minutes = int(seconds // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

# Creates the top navigation bar which includes 
def draw_nav_bar(win, elapsed_time, targets_clicked, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, NAV_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    
    speed = round(targets_clicked / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    
    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (250, 5))
    win.blit(hits_label, (550, 5))
    win.blit(lives_label, (750, 5))

    

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
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
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
            pass
        
        # Draws the targets
        draw(WIN, targets)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
