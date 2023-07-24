import time
import pygame
import math
import main
"""
Target class for all targets that are drawn onto the screen. 
"""
class Target:
    MAX_SIZE = 30
    NUM_CIRCLES = 4

    def __init__(self, x, y, size, growth_rate, is_static=False, has_gravity = False, velocity_x=0, velocity_y=0): 
        self.x = x
        self.y = y
        self.size = size
        self.grow = True
        self.is_static = is_static
        self.growth_rate = growth_rate
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.spawn_time = time.time()
        self.has_gravity = has_gravity

    def update(self, gravity_constant=0.2):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.has_gravity:
            self.velocity_y += gravity_constant

        # Check for collisions with the screen edges
        if self.x - self.size < 0 or self.x + self.size > main.WIDTH:
            self.velocity_x *= -1
        if self.y - self.size < 0 or self.y + self.size > main.HEIGHT:
            self.velocity_y *= -1
        
        if not self.is_static:
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