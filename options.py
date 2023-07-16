class UserOptions:
    def __init__(self):
        self.target_colors = ["red", "blue", "green", "yellow", "purple", "white"]
        #self.first_target_color = "red"
        #self.second_target_color = 'white'
        self.first_target_color_index = 0
        self.second_target_color_index = 5
        self.background_color = (0, 25, 40)

    def get_first_target_color(self):
        return self.target_colors[self.first_target_color_index]
    
    def get_second_target_color(self):
        return self.target_colors[self.second_target_color_index]
    
    def set_first_target_color(self):
        self.first_target_color = self.target_colors[self.first_target_color_index]
    
    def set_second_target_color(self):
        self.second_target_color = self.target_colors[self.second_target_color_index]

    def cycle_first_target_color(self):
        self.first_target_color_index = (self.first_target_color_index + 1) % len(self.target_colors)
        
    def cycle_second_target_color(self):
        self.second_target_color_index = (self.second_target_color_index + 1) % len(self.target_colors)

    def get_background_color(self):
        return self.background_color

    def set_background_color(self, color):
        self.background_color = color



