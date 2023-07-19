import pygame
"""
Button class for the main menu and ending screen. Handles
updating the button onto the screen, checking for input, and
changing the color when the user hovers the button. 
"""
class Button():
    # Initialize properties
    def __init__(self, pos, text_input, font, base_color, hovering_color, padding=10):
        #self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, 1, self.base_color)
        self.padding = padding
        # if self.image is None:
        #     self.image = self.text
        # self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        #self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.text.get_width() + 2 * self.padding, self.text.get_height() + 2 * self.padding)

    # Updates the image and text for the button onto the window
    def update(self, win):
        # if self.image is not None:
        #     win.blit(self.image, self.rect)
        # win.blit(self.text, self.text_rect)

        pygame.draw.rect(win, "#6200EE", self.rect)
        win.blit(self.text, (self.rect.centerx - self.text.get_width() // 2, self.rect.centery - self.text.get_height() // 2))

    # Checks if the user is clicking on the button
    def checkForInput(self, position):
        # if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
        #     return True
        # return False
    
        return self.rect.collidepoint(position)
    
    # Checks if the user is hovering over the button to change the color
    def changeColor(self, position):
        # if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
        #     self.text = self.font.render(self.text_input, 1, self.hovering_color)
        # else:
        #     self.text = self.font.render(self.text_input, 1, self.base_color)
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    
