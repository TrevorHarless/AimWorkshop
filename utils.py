import math
import pygame

# Height of the top navigation bar 
NAV_BAR_HEIGHT = 50
NAV_BAR_WIDTH = 640

"""
Function for drawing the targets. 
"""
def draw(win, targets, options):
    win.fill(options.get_bg_color())
    for target in targets:
        target.draw(win, options)

def mock_draw(win, target, options):
    target.draw(win, options)

# Returns a neatly formatted time with minutes, seconds, and milliseconds
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000 / 100))
    seconds = int(round(secs % 60, 1))
    minutes = int(seconds // 60)

    if minutes > 0:
        return f"{minutes:02d}:{seconds:02d}.{milli}"
    elif seconds > 9:
        return f"{seconds}.{milli}"
    elif seconds > 0:
        return f"{seconds}.{milli}"
    else:
        return f"0.{milli}"

def show_explanation_screen(win, options, width, height, explanation_text):
    font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 22)
    text = font.render(explanation_text, True, "white")
    text_rect = text.get_rect(center=(width // 2, height // 2 - 80))
    note_text = font.render("Press SPACE to continue", True, "white")
    note_rect = note_text.get_rect(center=(width // 2, height // 2 + 80))
    start_time = pygame.time.get_ticks()
    duration = 8000  # 8 seconds 
    run = True
    while run and pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

        win.fill(options.get_bg_color())
        win.blit(text, text_rect)
        win.blit(note_text, note_rect)
        pygame.display.update()



# Easily position text or rectangles in the middle of the screen
def get_middle(surface, width):
    return width / 2 - surface.get_width() / 2  

# Creates the top navigation bar which includes 
def draw_nav_bar(win, elapsed_time, targets_clicked, misses, width, lives):
    container_rect = pygame.Rect(width / 4, 0, NAV_BAR_WIDTH, NAV_BAR_HEIGHT)
    pygame.draw.rect(win, "#F8F9F8", container_rect, border_bottom_left_radius=50, border_bottom_right_radius=50)

    # pygame.draw.rect(win, "white", self.container_rect, 2, border_radius=self.border_radius)

    speed = round(targets_clicked / elapsed_time, 1)
    
    time_label = get_font(20).render(f"{format_time(elapsed_time)}", 1, "#212026")
    speed_label = get_font(20).render(f"Speed: {speed} t/s", 1, "#212026")
    hits_label = get_font(20).render(f"Hits: {targets_clicked}", 1, "#212026")
    lives_label = get_font(20).render(f"Lives: {lives - misses}", 1, "#212026")

    win.blit(time_label, (container_rect.left + 25, container_rect.centery - time_label.get_height() // 2))
    win.blit(speed_label, (container_rect.left + 150, container_rect.centery - speed_label.get_height() // 2))
    win.blit(hits_label, (container_rect.left + 375, container_rect.centery - hits_label.get_height() // 2))
    win.blit(lives_label, (container_rect.left + 520, container_rect.centery - lives_label.get_height() // 2))

def get_font(size): 
    return pygame.font.Font("assets/fonts/Inter-Regular.ttf", size)


def center_vertically(buttons, spacing, offset_y, width, height):
    total_height = sum(button.rect.height for button in buttons)
    total_spacing = (len(buttons) - 1) * spacing
    start_y = (height - (total_height + total_spacing)) // 2

    for button in buttons:
        button.rect.center = (width / 2, start_y + button.rect.height // 2 + offset_y)
        start_y += button.rect.height + spacing

def center_x(button, width):
    button.rect.x = (width - button.rect.width) // 2

# TODO - Change color to what is being used
def render_scores(scores, x_offset, y_offset, win, label, limit=5):
    title_text = get_font(32).render(label, True, "white")
    win.blit(title_text, (x_offset, y_offset))
    y_offset += 60

    for i, score_tuple in enumerate(scores[:limit]):
        text = f"{i+1}. Score: {score_tuple[1]}"
        score_text = get_font(24).render(text, True, "white")
        win.blit(score_text, (x_offset, y_offset))
        y_offset += 40

# Import values from main.py at the end of utils.py to avoid circular import error
from main import LABEL_FONT