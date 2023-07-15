import math

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

# Import values from main.py at the end of utils.py to avoid circular import error
from main import BG_COLOR, WIDTH