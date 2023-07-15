import pygame
import math
import time
import random 
from target import Target
from button import Button
from utils import draw, format_time, get_middle

pygame.init()

# Width and height of the window
WIDTH, HEIGHT = 1280, 720

# Window/Screen for the game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Height of the top navigation bar 
NAV_BAR_HEIGHT = 50

# How often a unique target will appear
TARGET_INCREMENT = 300

# Target event
TARGET_EVENT = pygame.USEREVENT

# Padding for the target so that it is always fully on the screen
TARGET_PADDING = 30

# Color of the background
BG_COLOR = (0, 25, 40)

# Number of lives
LIVES = 3

# RGB Values for Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
MENU_FONT = pygame.font.SysFont("Arial", 32)
OPTION_FONT = pygame.font.SysFont("Arial", 24)
LABEL_FONT = pygame.font.SysFont("sans", 24)

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


def main_menu():
    pygame.display.set_caption("Menu")
    WIN.fill("black")
    
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    
    MENU_TEXT = MENU_FONT.render("MAIN MENU", 1, "white")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                         text_input="PLAY", font=MENU_FONT, base_color="#d7fcd4", hovering_color="white")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                         text_input="OPTIONS", font=MENU_FONT, base_color="#d7fcd4", hovering_color="white")
    QUIT_BUTTON =Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                         text_input="QUIT", font=MENU_FONT, base_color="#d7fcd4", hovering_color="white")

    WIN.blit(MENU_TEXT, MENU_RECT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit()
        
        WIN.fill("black")
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
    
        pygame.display.update()


def end_screen(win, elapsed_time, targets_clicked, clicks):
    pygame.display.set_caption("Game Over!")
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    
    speed = round(targets_clicked / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    
    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "white")

    try:
        accuracy = round(targets_clicked / clicks * 100, 1)
    except ZeroDivisionError as e:
        accuracy = 0.0
    
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}", 1, "white")

    win.blit(time_label, (get_middle(time_label), 50))
    win.blit(speed_label, (get_middle(speed_label), 150))
    win.blit(hits_label, (get_middle(hits_label), 250))
    win.blit(accuracy_label, (get_middle(accuracy_label), 350))

    pygame.display.update()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

"""
Contains the main game loop and logic
"""
def play():
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
            end_screen(WIN, elapsed_time, targets_clicked, clicks)
        
        # Draws the targets
        draw(WIN, targets)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
