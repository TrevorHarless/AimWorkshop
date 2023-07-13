import pygame
import math
import time
import random
pygame.init()


WIDTH, HEIGHT = 600, 400

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Workshop")

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        

def main():
    run = True

    # Checks if X was clicked to quit the game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()

        


