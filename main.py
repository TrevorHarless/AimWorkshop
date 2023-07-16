import pygame
from button import Button
from utils import mock_draw, format_time, get_middle
from game_logic import radiating_targets
from options import UserOptions
from target import Target
pygame.init()

# Width and height of the window
WIDTH, HEIGHT = 1280, 720

# Window/Screen for the game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Workshop")

# Color of the background
BG_COLOR = (0, 25, 40)

# RGB Values for Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
MENU_FONT = pygame.font.SysFont("Arial", 32)
OPTION_FONT = pygame.font.SysFont("Arial", 24)
LABEL_FONT = pygame.font.SysFont("sans", 24)

options = UserOptions()


"""
Creates the main menu for the game. 
"""
def main_menu(options):
    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                         text_input="PLAY", font=MENU_FONT, base_color="white", hovering_color="#d7fcd4")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                         text_input="OPTIONS", font=MENU_FONT, base_color="white", hovering_color="#d7fcd4")
    QUIT_BUTTON =Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 550),
                         text_input="QUIT", font=MENU_FONT, base_color="white", hovering_color="#d7fcd4")

    bg_img = pygame.image.load("assets/Gradient Background.jpg")
    bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))   

    while True:
        WIN.blit(bg_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(options)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options_screen(options)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit()
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = MENU_FONT.render("MAIN MENU", 1, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
    
        pygame.display.update()

"""
Contains the main game loop and logic
"""
def play(options):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("black")

        PLAY_TEXT = MENU_FONT.render("GAME MODES", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
        WIN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_RADIATING_CIRCLES = Button(image=None, pos=(640, 250), 
                            text_input="RADIATING CIRCLES", font=MENU_FONT, base_color="White", hovering_color="Green")
        PLAY_BACK = Button(image=None, pos=(640, 550), 
                            text_input="BACK", font=MENU_FONT, base_color="White", hovering_color="Green")
        
        PLAY_RADIATING_CIRCLES.changeColor(PLAY_MOUSE_POS)
        PLAY_RADIATING_CIRCLES.update(WIN)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(options)
                if PLAY_RADIATING_CIRCLES.checkForInput(PLAY_MOUSE_POS):
                    radiating_targets(WIN, HEIGHT, WIDTH, options)

        pygame.display.update()

"""
Creates the end screen for the game when the user runs out of lives. 
"""
def end_screen(elapsed_time, targets_clicked, clicks, options):
    while True:
        END_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill("black")
        
        END_SCREEN_TEXT = MENU_FONT.render("GAME OVER", True, "White")
        END_SCREEN_RECT = END_SCREEN_TEXT.get_rect(center=(640, 100))
        WIN.blit(END_SCREEN_TEXT, END_SCREEN_RECT)
        
        END_SCREEN_BACK = Button(image=None, pos=(640, 600), 
            text_input="BACK", font=MENU_FONT, base_color="White", hovering_color="Green")
        
        END_SCREEN_BACK.changeColor(END_SCREEN_MOUSE_POS)
        END_SCREEN_BACK.update(WIN)

        time_label = LABEL_FONT.render(f"TIME: {format_time(elapsed_time)}", 1, "white")
        
        speed = round(targets_clicked / elapsed_time, 1)
        speed_label = LABEL_FONT.render(f"SPEED: {speed} t/s", 1, "white")
        
        hits_label = LABEL_FONT.render(f"HITS: {targets_clicked}", 1, "white")

        try:
            accuracy = round(targets_clicked / clicks * 100, 1)
        except ZeroDivisionError as e:
            accuracy = 0.0
        
        accuracy_label = LABEL_FONT.render(f"ACCURACY: {accuracy}", 1, "white")

        WIN.blit(time_label, (get_middle(time_label, WIDTH), 180))
        WIN.blit(speed_label, (get_middle(speed_label, WIDTH), 280))
        WIN.blit(hits_label, (get_middle(hits_label, WIDTH), 380))
        WIN.blit(accuracy_label, (get_middle(accuracy_label, WIDTH), 480))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if END_SCREEN_BACK.checkForInput(END_SCREEN_MOUSE_POS):
                    main_menu(options)

        pygame.display.update()

def options_screen(options):
    while True:
        OPTIONS_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill("black")
        
        OPTIONS_SCREEN_TEXT = MENU_FONT.render("OPTIONS", True, "White")
        OPTIONS_SCREEN_RECT = OPTIONS_SCREEN_TEXT.get_rect(center=(640, 100))
        WIN.blit(OPTIONS_SCREEN_TEXT, OPTIONS_SCREEN_RECT)

        mock_target = Target(1000, 235, 30)  
        mock_draw(WIN, mock_target, options)

        FIRST_TARGET_COLOR_BUTTON = Button(image=None, pos=(640, 180), 
            text_input="FIRST TARGET COLOR", font=MENU_FONT, base_color="White", hovering_color="Green")
        SECOND_TARGET_COLOR_BUTTON = Button(image=None, pos=(640, 280), 
            text_input="SECOND TARGET COLOR", font=MENU_FONT, base_color="White", hovering_color="Green")

        OPTIONS_SCREEN_BACK = Button(image=None, pos=(640, 600), 
            text_input="BACK", font=MENU_FONT, base_color="White", hovering_color="Green")
        
        OPTIONS_SCREEN_BACK.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        OPTIONS_SCREEN_BACK.update(WIN)
        FIRST_TARGET_COLOR_BUTTON.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        FIRST_TARGET_COLOR_BUTTON.update(WIN)
        SECOND_TARGET_COLOR_BUTTON.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        SECOND_TARGET_COLOR_BUTTON.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_SCREEN_BACK.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    main_menu(options)
                if FIRST_TARGET_COLOR_BUTTON.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    options.cycle_first_target_color()
                if SECOND_TARGET_COLOR_BUTTON.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    options.cycle_second_target_color()
        pygame.display.update()


if __name__ == "__main__":
    main_menu(options)
