class UserOptions:
    def __init__(self):
        self.target_colors = ["red", "blue", "green", "yellow", "purple", "white"]
        self.first_target_color_index = 0
        self.second_target_color_index = 5
        self.bg_colors = [ "#213972", "#a69cbc", "#2e5c7f", "#72071c", "#679683", "#4f6a05", "#453430", "#b8b3e9", "#b25c1f", "#e5f0bb", "#c6b9b7", "#d44d51"]
        self.bg_color_index = 0
        self.growth_rate = .4
 
    def get_first_target_color(self):
        return self.target_colors[self.first_target_color_index]
    
    def get_second_target_color(self):
        return self.target_colors[self.second_target_color_index]
    
    def cycle_first_target_color(self):
        self.first_target_color_index = (self.first_target_color_index + 1) % len(self.target_colors)
        
    def cycle_second_target_color(self):
        self.second_target_color_index = (self.second_target_color_index + 1) % len(self.target_colors)

    def get_bg_color(self):
        return self.bg_colors[self.bg_color_index]

    def cycle_bg_image(self):
        self.bg_color_index = (self.bg_color_index + 1) % len(self.bg_colors)

    def get_growth_rate(self):
        return self.growth_rate
    
    def set_growth_rate(self, growth_rate):
        self.growth_rate = growth_rate

   



