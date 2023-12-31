import pygame
from button import Button
from utils import mock_draw, format_time, get_middle, get_font, center_vertically, center_x, render_scores
from game_logic import radiating_targets, no_gravity_mode, gravity_mode, static_mode
from options import UserOptions
from target import Target
from slider import Slider
from database import Database
pygame.init()

# Width and height of the window
WIDTH, HEIGHT = 1280, 720

# Window/Screen for the game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Workshop")

LABEL_FONT = pygame.font.SysFont("assets/fonts/Inter-Regular", 24)

# Colors
BUTTON_COLOR = "#F8F9F8"
PRIMARY_COLOR = "#F8F9F8"
PRIMARY_VAR = "#3700B3"
SECONDARY_VAR = "#018786"
ON_PRIMARY = "#212026"
ON_SECONDARY = "#A4CFC9"

# Sliders for Options Screen
growth_rate_slider = Slider((WIDTH / 2, 460), (100, 30), .5, 0.1, 1.2, PRIMARY_COLOR, ON_SECONDARY)
spawn_rate_slider = Slider((WIDTH / 2, 585), (100, 30), .5, 400, 2000, PRIMARY_COLOR, ON_SECONDARY)

"""
Creates the main menu for the game. Includes the Play, Options, Stats, and Quit buttons. 
"""
def main_menu(options, db):
    PLAY_BUTTON = Button(pos=(0, 0),
                         text_input="PLAY", font=get_font(60), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
    OPTIONS_BUTTON = Button(pos=(0, 0),
                         text_input="OPTIONS", font=get_font(60), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
    STATS_BUTTON = Button(pos=(0, 0),
                         text_input="STATS", font=get_font(60), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
    QUIT_BUTTON =Button(pos=(0, 0),
                         text_input="QUIT", font=get_font(60), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)

    buttons = [PLAY_BUTTON, OPTIONS_BUTTON, STATS_BUTTON, QUIT_BUTTON]
    # Spacing between buttons on main menu screen
    spacing = 35 

    center_vertically(buttons, spacing, 50, WIDTH, HEIGHT)

    
    while True:
        WIN.fill(options.get_bg_color())
        MENU_TEXT = get_font(75).render("AIM WORKSHOP", True, PRIMARY_COLOR)
        WIN.blit(MENU_TEXT, (get_middle(MENU_TEXT, WIDTH), 45))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(options, db)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options_screen(options, growth_rate_slider, spawn_rate_slider, db)
                if STATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    stats_screen(options, db)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit()
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        pygame.display.update()

"""
Play screen. Includes all of the game modes that the user can play as well as a back button
that routes to the main menu. 
"""
def play(options, db):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill(options.get_bg_color())

        PLAY_TEXT = get_font(75).render("GAME MODES", True, PRIMARY_COLOR)
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH / 2, 70))
        WIN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_RADIATING_CIRCLES = Button(pos=(0, 0), 
                            text_input="RADIATING CIRCLES", font=get_font(35), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        PLAY_GRAVITY = Button(pos=(0, 0), 
                            text_input="GRAVITY", font=get_font(35), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        PLAY_NO_GRAVITY = Button(pos=(0, 0), 
                            text_input="NO GRAVITY", font=get_font(35), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        PLAY_STATIC = Button(pos=(0, 0), 
                            text_input="STATIC", font=get_font(35), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        
        PLAY_BACK = Button(pos=(0, 0), 
                            text_input="BACK", font=get_font(35), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        
        buttons = [
            PLAY_RADIATING_CIRCLES, PLAY_GRAVITY, PLAY_NO_GRAVITY, PLAY_STATIC, PLAY_BACK
        ]

        # Spacing between buttons on play screen
        spacing = 35

        center_vertically(buttons, spacing, 0, WIDTH, HEIGHT)
        
        PLAY_RADIATING_CIRCLES.changeColor(PLAY_MOUSE_POS)
        PLAY_RADIATING_CIRCLES.update(WIN)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WIN)
        PLAY_NO_GRAVITY.changeColor(PLAY_MOUSE_POS)
        PLAY_NO_GRAVITY.update(WIN)
        PLAY_STATIC.changeColor(PLAY_MOUSE_POS)
        PLAY_STATIC.update(WIN)
        PLAY_GRAVITY.changeColor(PLAY_MOUSE_POS)
        PLAY_GRAVITY.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(options, db)
                if PLAY_RADIATING_CIRCLES.checkForInput(PLAY_MOUSE_POS):
                    radiating_targets(WIN, HEIGHT, WIDTH, db, options)
                if PLAY_GRAVITY.checkForInput(PLAY_MOUSE_POS):
                    gravity_mode(WIN, HEIGHT, WIDTH, db, options)
                if PLAY_NO_GRAVITY.checkForInput(PLAY_MOUSE_POS):
                    no_gravity_mode(WIN, HEIGHT, WIDTH, db, options)
                if PLAY_STATIC.checkForInput(PLAY_MOUSE_POS):
                    static_mode(WIN, HEIGHT, WIDTH, db, options)

        pygame.display.update()

"""
Creates the end screen for the game when the user runs out of lives. Displays different
stats for the user to see how they did on that round. 
"""
def end_screen(elapsed_time, targets_clicked, clicks, score, options, db, current_game):
    while True:
        END_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        
        WIN.fill(options.get_bg_color())
        
        END_SCREEN_TEXT = get_font(75).render("GAME OVER", True, PRIMARY_COLOR)
        END_SCREEN_RECT = END_SCREEN_TEXT.get_rect(center=(640, 100))
        WIN.blit(END_SCREEN_TEXT, END_SCREEN_RECT)
        
        END_SCREEN_BACK = Button(pos=(0, 0), 
            text_input="BACK", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        RESTART_BUTTON = Button(pos=(0, 0), 
            text_input="RESTART", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)

        buttons = [RESTART_BUTTON, END_SCREEN_BACK]

        # Spacing between buttons on play screen
        spacing = 35

        center_vertically(buttons, spacing, 150, WIDTH, HEIGHT)
        
        END_SCREEN_BACK.changeColor(END_SCREEN_MOUSE_POS)
        END_SCREEN_BACK.update(WIN)
        RESTART_BUTTON.changeColor(END_SCREEN_MOUSE_POS)
        RESTART_BUTTON.update(WIN)

        time_label = get_font(24).render(f"TIME: {format_time(elapsed_time)} seconds", 1, PRIMARY_COLOR)
        
        speed = round(targets_clicked / elapsed_time, 1)
        speed_label = get_font(24).render(f"SPEED: {speed} targets/second", 1, PRIMARY_COLOR)
        
        hits_label = get_font(24).render(f"HITS: {targets_clicked}", 1, PRIMARY_COLOR)

        score_label = get_font(24).render(f"SCORE: {score}", 1, PRIMARY_COLOR)

        try:
            accuracy = round(targets_clicked / clicks * 100, 1)
        except ZeroDivisionError as e:
            accuracy = 0.0
        
        accuracy_label = get_font(24).render(f"ACCURACY: {accuracy}%", 1, PRIMARY_COLOR)

        WIN.blit(score_label, (get_middle(score_label, WIDTH), 180))
        WIN.blit(time_label, (get_middle(time_label, WIDTH), 230))
        WIN.blit(speed_label, (get_middle(speed_label, WIDTH), 280))
        WIN.blit(hits_label, (get_middle(hits_label, WIDTH), 330))
        WIN.blit(accuracy_label, (get_middle(accuracy_label, WIDTH), 380))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if END_SCREEN_BACK.checkForInput(END_SCREEN_MOUSE_POS):
                    main_menu(options, db)
                if RESTART_BUTTON.checkForInput(END_SCREEN_MOUSE_POS):
                    if current_game == 1:
                        radiating_targets(WIN, HEIGHT, WIDTH, db, options)
                    elif current_game == 2:
                        no_gravity_mode(WIN, HEIGHT, WIDTH, db, options)
                    elif current_game == 3:
                        gravity_mode(WIN, HEIGHT, WIDTH, db, options)
                    elif current_game == 4:
                        static_mode(WIN, HEIGHT, WIDTH, db, options)

        pygame.display.update()

"""
Options screen which includes changing the color of the target, changing the background color,
and changing the growth rate of the targets. 
"""
def options_screen(options, growth_rate_slider, spawn_rate_slider, db):
    while True:
        WIN.fill(options.get_bg_color())
        
        OPTIONS_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_SCREEN_TEXT = get_font(75).render("OPTIONS", True, PRIMARY_COLOR)
        OPTIONS_SCREEN_RECT = OPTIONS_SCREEN_TEXT.get_rect(center=(WIDTH / 2, 70))
        WIN.blit(OPTIONS_SCREEN_TEXT, OPTIONS_SCREEN_RECT)

        mock_target = Target(900, 160, 30, 0)  
        mock_draw(WIN, mock_target, options)

        FIRST_TARGET_COLOR_BUTTON = Button(pos=(0, 0), 
            text_input="FIRST TARGET COLOR", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        SECOND_TARGET_COLOR_BUTTON = Button(pos=(0, 0), 
            text_input="SECOND TARGET COLOR", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        BACKGROUND_BUTTON = Button(pos=(0, 0), 
            text_input="BACKGROUND", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)
        
        buttons = [
            FIRST_TARGET_COLOR_BUTTON, SECOND_TARGET_COLOR_BUTTON, 
            BACKGROUND_BUTTON
        ]

        # Spacing between buttons on options screen
        spacing = 25

        center_vertically(buttons, spacing, -120, WIDTH, HEIGHT)

        OPTIONS_SCREEN_BACK = Button(pos=(0, 0), 
            text_input="BACK", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)

        center_x(OPTIONS_SCREEN_BACK, WIDTH)
        OPTIONS_SCREEN_BACK.rect.y = HEIGHT * 0.9
        
        OPTIONS_SCREEN_BACK.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        OPTIONS_SCREEN_BACK.update(WIN)
        FIRST_TARGET_COLOR_BUTTON.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        FIRST_TARGET_COLOR_BUTTON.update(WIN)
        SECOND_TARGET_COLOR_BUTTON.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        SECOND_TARGET_COLOR_BUTTON.update(WIN)
        BACKGROUND_BUTTON.changeColor(OPTIONS_SCREEN_MOUSE_POS)
        BACKGROUND_BUTTON.update(WIN)
        
        GROWTH_RATE_TEXT = get_font(32).render("GROWTH RATE", True, PRIMARY_COLOR)
        WIN.blit(GROWTH_RATE_TEXT, (get_middle(GROWTH_RATE_TEXT, WIDTH), 370))

        SPAWN_RATE_TEXT = get_font(32).render("SPAWN RATE", True, PRIMARY_COLOR)
        WIN.blit(SPAWN_RATE_TEXT, (get_middle(SPAWN_RATE_TEXT, WIDTH), 500))

        growth_rate_slider.draw_value_and_text(WIN, "slowest", "fastest", PRIMARY_COLOR)
        spawn_rate_slider.draw_value_and_text(WIN, "fastest", "slowest", PRIMARY_COLOR)

        if growth_rate_slider.container_rect.collidepoint(OPTIONS_SCREEN_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                growth_rate_slider.move_slider(OPTIONS_SCREEN_MOUSE_POS)
                options.set_growth_rate(growth_rate_slider.get_value())
        growth_rate_slider.render(WIN)

        if spawn_rate_slider.container_rect.collidepoint(OPTIONS_SCREEN_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                spawn_rate_slider.move_slider(OPTIONS_SCREEN_MOUSE_POS)
                options.set_spawn_rate(spawn_rate_slider.get_value())
        spawn_rate_slider.render(WIN)
        
        
        # for slider in sliders:
        #     if slider.container_rect.collidepoint(OPTIONS_SCREEN_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
        #         slider.move_slider(OPTIONS_SCREEN_MOUSE_POS)
        #         options.set_growth_rate(slider.get_value())
        #     slider.render(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_SCREEN_BACK.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    main_menu(options, db)
                if FIRST_TARGET_COLOR_BUTTON.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    options.cycle_first_target_color()
                if SECOND_TARGET_COLOR_BUTTON.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    options.cycle_second_target_color()
                if BACKGROUND_BUTTON.checkForInput(OPTIONS_SCREEN_MOUSE_POS):
                    options.cycle_bg_image()
        pygame.display.update()

def stats_screen(options, db):
    while True:
        #db = Database()

        radiating_scores = db.get_radiating_scores()
        no_gravity_scores = db.get_no_gravity_scores()
        gravity_scores = db.get_gravity_scores()
        static_scores = db.get_static_scores()

        WIN.fill(options.get_bg_color())
        
        STATS_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        STATS_SCREEN_TEXT = get_font(75).render("STATS", True, PRIMARY_COLOR)
        STATS_SCREEN_RECT = STATS_SCREEN_TEXT.get_rect(center=(WIDTH / 2, 70))
        WIN.blit(STATS_SCREEN_TEXT, STATS_SCREEN_RECT)

        STATS_SCREEN_BACK = Button(pos=(0, 0), 
            text_input="BACK", font=get_font(32), base_color=ON_PRIMARY, hovering_color=ON_SECONDARY, button_color=BUTTON_COLOR)

        center_x(STATS_SCREEN_BACK, WIDTH)
        STATS_SCREEN_BACK.rect.y = HEIGHT * 0.9
        
        STATS_SCREEN_BACK.changeColor(STATS_SCREEN_MOUSE_POS)
        STATS_SCREEN_BACK.update(WIN)

        y_offset = 120  # Adjust this value to set the initial vertical position of the scores on the screen

        render_scores(radiating_scores, 100, y_offset, WIN, "Radiating")
        render_scores(gravity_scores, 400, y_offset, WIN, "Gravity")
        render_scores(no_gravity_scores, 700, y_offset, WIN, "No Gravity")
        render_scores(static_scores, 1000, y_offset, WIN, "Static")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if STATS_SCREEN_BACK.checkForInput(STATS_SCREEN_MOUSE_POS):
                    main_menu(options, db)
        pygame.display.update()

if __name__ == "__main__":
    try: 
        db = Database()
        options = UserOptions()
        main_menu(options, db)
    finally:
        db.close_connection()
