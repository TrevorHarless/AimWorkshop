import math
import pygame

# Height of the top navigation bar 
NAV_BAR_HEIGHT = 50

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

# Easily position text or rectangles in the middle of the screen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2  

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

# Import values from main.py at the end of utils.py to avoid circular import error
from main import BG_COLOR, WIDTH, LABEL_FONT
from game_logic import LIVES