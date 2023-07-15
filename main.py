import pygame
from button import Button
from utils import draw, format_time, get_middle
from game_logic import radiating_targets
pygame.init()

# Width and height of the window
WIDTH, HEIGHT = 1280, 720

# Window/Screen for the game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Color of the background
BG_COLOR = (0, 25, 40)

# RGB Values for Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
MENU_FONT = pygame.font.SysFont("Arial", 32)
OPTION_FONT = pygame.font.SysFont("Arial", 24)
LABEL_FONT = pygame.font.SysFont("sans", 24)

"""
Creates the main menu for the game. 
"""
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

"""
Contains the main game loop and logic
"""
def play():
    radiating_targets(WIN, HEIGHT, WIDTH)
    pygame.quit()


"""
Creates the end screen for the game when the user runs out of lives. 
"""
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

if __name__ == "__main__":
    main_menu()
