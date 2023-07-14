import pygame
import math
import time
import random

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if (self.size + self.GROWTH_RATE >= self.MAX_SIZE):
            self.grow = False
        if (self.grow):
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    """
    Draws a singular target which is represented by 4 circles in reducing size
    """
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    """
    Checks if where the user clicked is inside the radius of the target
    """
    def collide(self, x, y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size