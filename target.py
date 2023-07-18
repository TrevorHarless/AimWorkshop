import pygame
import math

"""
Target class for all targets that are drawn onto the screen. 
"""
class Target:
    MAX_SIZE = 30
    #COLOR = "red"
    #SECOND_COLOR = "white"
    NUM_CIRCLES = 4

    def __init__(self, x, y, size, growth_rate):
        self.x = x
        self.y = y
        self.size = size
        self.grow = True
        self.growth_rate = growth_rate

    def update(self):
        if (self.size + self.growth_rate >= self.MAX_SIZE):
            self.grow = False
        if (self.grow):
            self.size += self.growth_rate
        else:
            self.size -= self.growth_rate

    """
    Draws a singular target which is represented by 4 circles in reducing size
    """
    def draw(self, win, options):
        for i in range(self.NUM_CIRCLES):
            circle_radius = self.size * (0.8 ** i)
            if i % 2 == 0:
                circle_color = options.get_first_target_color()
            else:
                circle_color = options.get_second_target_color()
            
            pygame.draw.circle(win, circle_color, (self.x, self.y), int(circle_radius))

    """
    Checks if where the user clicked is inside the radius of the target
    """
    def collide(self, x, y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size