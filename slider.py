import pygame
from utils import get_font
"""
Class for the Sliders in the options screen. Allow for the user to smoothly change settings.
"""
class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int, base_color, hovering_color):
        self.pos = pos
        self.size = size
        self.circle_radius = self.size[1] * .6

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos) * initial_val 

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        self.hovered = False
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.border_radius = 30


    def render(self, win):
        # Draw the circle (slider button) with overlapping container rectangle
        pygame.draw.rect(win, "white", self.container_rect, 2, border_radius=self.border_radius)

        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
    
        if self.hovered:
            pygame.draw.circle(win, "black", self.button_rect.center, self.circle_radius)
            pygame.draw.circle(win, self.hovering_color, self.button_rect.center, self.circle_radius * .9)
        else:
            pygame.draw.circle(win, "black", self.button_rect.center, self.circle_radius)
            pygame.draw.circle(win, self.base_color, self.button_rect.center, self.circle_radius * .9)


    def move_slider(self, mouse_pos):
       # Calculate the new x-coordinate for the slider button
        new_x = mouse_pos[0]
        
        # Limit the slider button's x-coordinate to the boundaries of the container rectangle
        if new_x < self.slider_left_pos + self.circle_radius:
            new_x = self.slider_left_pos + self.circle_radius
        elif new_x > self.slider_right_pos - self.circle_radius:
            new_x = self.slider_right_pos - self.circle_radius

        # Move the slider button to the new position
        self.button_rect.centerx = new_x


    def get_value(self):
        # Calculate the position of the slider button relative to the container rectangle's left boundary
        button_val = self.button_rect.centerx - (self.slider_left_pos + self.circle_radius)

        # Map the button position to the desired value range (e.g., from 0 to 1.2)
        value_range = self.max - self.min
        return (button_val / (self.slider_right_pos - self.slider_left_pos - 2 * self.circle_radius)) * value_range + self.min
    
    def draw_value_and_text(self, win, left_text, right_text, color):
        # Display slider value near the button
        value_text = get_font(20).render(f"{self.get_value():.2f}", True, color)
        value_rect = value_text.get_rect(center=(self.button_rect.centerx, self.button_rect.centery - 30))
        win.blit(value_text, value_rect)

        left_label_text = get_font(20).render(left_text, True, color)
        right_label_text = get_font(20).render(right_text, True, color)
        left_label_rect = left_label_text.get_rect(midtop=(self.slider_left_pos - (self.slider_left_pos * .1), self.slider_top_pos))
        right_label_rect = right_label_text.get_rect(midtop=(self.slider_right_pos + (self.slider_right_pos * .08), self.slider_top_pos))
        win.blit(left_label_text, left_label_rect)
        win.blit(right_label_text, right_label_rect)

    



        