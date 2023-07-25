import pygame
import time
import random
from target import Target
from utils import draw, draw_nav_bar, NAV_BAR_HEIGHT, show_explanation_screen
import main as main


# Target event
TARGET_EVENT = pygame.USEREVENT

# Padding for the target so that it is always fully on the screen
TARGET_PADDING = 30

# Number of lives
LIVES = 3

FPS = 60

EXPLANATION_TIME = 8

def radiating_targets(WIN, HEIGHT, WIDTH, options):
    # Explanation screen before the game starts
    show_explanation_screen(WIN, options, WIDTH, HEIGHT,
        "RADIATING TARGETS MODE: Targets must be shot before they disappear or lives will be lost!")
    
    # How often a unique target will appear
    target_increment = options.get_spawn_rate()  

    run = True
    targets = []
    clock = pygame.time.Clock()
    pygame.time.set_timer(TARGET_EVENT, int(target_increment))
    targets_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Game loop
    while run:
        # Sets framerate to 60 // How fast the while loop will run
        clock.tick(FPS)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit()
            
            if (event.type == TARGET_EVENT):
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, 0, options.get_growth_rate())
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
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses, WIDTH, LIVES)
        pygame.display.update()

def no_gravity_mode(WIN, HEIGHT, WIDTH, options):
    # Explanation screen before the game starts
    show_explanation_screen(WIN, options, WIDTH, HEIGHT, 
        "NO GRAVITY MODE: Targets are NOT affected by gravity. Lives are lost if a target is alive for longer than 6 seconds!")

    target_increment = 1400
    # Amount of seconds the target can be on the screen before a life is taken
    max_target_time = 6
    run = True
    targets = []
    clock = pygame.time.Clock()
    pygame.time.set_timer(TARGET_EVENT, target_increment)
    targets_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Game loop
    while run:
        # Sets framerate to 60 // How fast the while loop will run
        clock.tick(FPS)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, 30, options.get_growth_rate(), is_static=True, velocity_x=random.randint(-5, 5), velocity_y=random.randint(-5, 5))
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        # Updates all of the targets prior to drawing
        for target in targets:
            target.update()

            elapsed_time_since_spawn = time.time() - target.spawn_time
            if elapsed_time_since_spawn > max_target_time:
                targets.remove(target)
                misses += 1

            # If the user has clicked their mouse and collided with a target,
            # remove the target and increment targets clicked
            if click and target.collide(mouse_pos[0], mouse_pos[1]):
                targets.remove(target)
                targets_clicked += 1

        # Ends game if misses exceed the number of lives
        if misses >= LIVES:
            main.end_screen(elapsed_time, targets_clicked, clicks, options)

        # Draws the targets
        draw(WIN, targets, options)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses, WIDTH, LIVES)
        pygame.display.update()

def gravity_mode(WIN, HEIGHT, WIDTH, options):
    # Explanation screen before the game starts
    show_explanation_screen(WIN, options, WIDTH, HEIGHT, 
        "GRAVITY MODE: Targets ARE affected by gravity. Lives are lost if a target is alive for longer than 6 seconds!")

    gravity_constant = 0.2
    target_increment = 1400
    # Amount of seconds the target can be on the screen before a life is taken
    max_target_time = 6
    run = True
    targets = []
    clock = pygame.time.Clock()
    pygame.time.set_timer(TARGET_EVENT, target_increment)
    targets_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Game loop
    while run:
        # Sets framerate to 60 // How fast the while loop will run
        clock.tick(FPS)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, 30, options.get_growth_rate(), is_static=True, has_gravity=True, velocity_x=random.randint(-5, 5), velocity_y=random.randint(-5, 5))
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        # Updates all of the targets prior to drawing
        for target in targets:
            target.update(gravity_constant=gravity_constant)

            elapsed_time_since_spawn = time.time() - target.spawn_time
            if elapsed_time_since_spawn > max_target_time:
                targets.remove(target)
                misses += 1

            # If the user has clicked their mouse and collided with a target,
            # remove the target and increment targets clicked
            if click and target.collide(mouse_pos[0], mouse_pos[1]):
                targets.remove(target)
                targets_clicked += 1

        # Ends game if misses exceed the number of lives
        if misses >= LIVES:
            main.end_screen(elapsed_time, targets_clicked, clicks, options)

        # Draws the targets
        draw(WIN, targets, options)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses, WIDTH, LIVES)
        pygame.display.update()

def static_mode(WIN, HEIGHT, WIDTH, options):
    # Explanation screen before the game starts
    show_explanation_screen(WIN, options, WIDTH, HEIGHT, 
        "STATIC MODE: Lives are lost if a target is alive for longer than 6 seconds!")

    target_increment = 1400
    # Amount of seconds the target can be on the screen before a life is taken
    max_target_time = 6
    run = True
    targets = []
    clock = pygame.time.Clock()
    pygame.time.set_timer(TARGET_EVENT, target_increment)
    targets_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Game loop
    while run:
        # Sets framerate to 60 // How fast the while loop will run
        clock.tick(FPS)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + NAV_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, 30, options.get_growth_rate(), is_static=True)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        # Updates all of the targets prior to drawing
        for target in targets:
            target.update()

            elapsed_time_since_spawn = time.time() - target.spawn_time
            if elapsed_time_since_spawn > max_target_time:
                targets.remove(target)
                misses += 1

            # If the user has clicked their mouse and collided with a target,
            # remove the target and increment targets clicked
            if click and target.collide(mouse_pos[0], mouse_pos[1]):
                targets.remove(target)
                targets_clicked += 1

        # Ends game if misses exceed the number of lives
        if misses >= LIVES:
            main.end_screen(elapsed_time, targets_clicked, clicks, options)

        # Draws the targets
        draw(WIN, targets, options)
        draw_nav_bar(WIN, elapsed_time, targets_clicked, misses, WIDTH, LIVES)
        pygame.display.update()


            
            
