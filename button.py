"""
Button class for the main menu and ending screen. Handles
updating the button onto the screen, checking for input, and
changing the color when the user hovers the button. 
"""
class Button():
    
    # Initialize properties
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, 1, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Updates the image and text for the button onto the window
    def update(self, win):
        if self.image is not None:
            win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    # Checks if the user is clicking on the button
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    # Checks if the user is hovering over the button to change the color
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, 1, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, 1, self.base_color)

    
