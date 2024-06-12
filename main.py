import customtkinter as ctk 
from constants import *
from random import choice
from sys import exit
import os

class Game(ctk.CTk):
    def __init__(self):
        try:
            # setup
            super().__init__()
            self.title('Snake')
            self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')
            
            if os.path.exists('assets/icon/icon.ico'):
                self.iconbitmap('assets/icon/icon.ico')
            else:
                print("Icon file not found. Continuing without custom icon.")
            
            ctk.set_appearance_mode('dark')
            
            # layout
            self.columnconfigure(list(range(FIELDS[0])), weight= 1, uniform= 'a')
            self.rowconfigure(list(range(FIELDS[1])), weight= 1, uniform= 'a')
            
            # snake
            self.snake = [START_POS , (START_POS[0] - 1, START_POS[1]), (START_POS[0] - 2, START_POS[1])]
            self.direction = DIRECTIONS['right']
            
            self.bind('<Key>', self.get_input)
            
            # apple
            self.apple_position = ()
            self.place_apple()
            
            # draw logic
            self.draw_frames = []
            self.animate()
            
            # run
            self.mainloop()
        except Exception as e:
            print(f"Failed to initialize the game: {e}")
            exit()
    
    def animate(self):
        # create new head new head = old head + direction
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)
        
        # apple collision
        if self.snake[0] == self.apple_position:
            self.place_apple()
        else:
            # remove last part of the snake
            self.snake.pop()
        
        self.check_game_over()
        
        # drawing
        self.draw()
        # looping game (refresh every 250 ms)
        self.after(250, self.animate)
    
    def place_apple(self):
        possible_positions = [(x, y) for x in range(FIELDS[0]) for y in range(FIELDS[1])]
        for part in self.snake:
            if part in possible_positions:
                possible_positions.remove(part)
        self.apple_position = choice(possible_positions)
    
    def check_game_over(self):
        snake_head = self.snake[0]
        if snake_head[0] >= RIGHT_LIMIT or snake_head[1] >= DOWN_LIMIT or \
           snake_head[0] <= LEFT_LIMIT or snake_head[1] <= UP_LIMIT or \
           snake_head in self.snake[1:]:
            exit()
        
     
    def get_input(self, event):
        match event.keycode:
            case 37: self.direction = DIRECTIONS['left'] if self.direction != DIRECTIONS['right'] else self.direction # left arrow
            case 65: self.direction = DIRECTIONS['left'] if self.direction != DIRECTIONS['right'] else self.direction # a
            case 38: self.direction = DIRECTIONS['up'] if self.direction != DIRECTIONS['down'] else self.direction # up arrow
            case 87: self.direction = DIRECTIONS['up'] if self.direction != DIRECTIONS['down'] else self.direction # w
            case 39: self.direction = DIRECTIONS['right'] if self.direction != DIRECTIONS['left'] else self.direction # right arrow
            case 68: self.direction = DIRECTIONS['right'] if self.direction != DIRECTIONS['left'] else self.direction # d
            case 40: self.direction = DIRECTIONS['down'] if self.direction != DIRECTIONS['up'] else self.direction # down arrow
            case 83: self.direction = DIRECTIONS['down'] if self.direction != DIRECTIONS['up'] else self.direction # s
        
           
    def draw(self):
        # empty the window
        if self.draw_frames:
            for frame, pos in self.draw_frames:
                frame.grid_forget()
            self.draw_frames.clear()
        
        apple_frame = ctk.CTkFrame(self, fg_color= APPLE_COLOR)
        self.draw_frames.append((apple_frame, self.apple_position))
        
        for index, position in enumerate(self.snake):
            color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
            snake_frame = ctk.CTkFrame(self, fg_color= color, corner_radius= 0)
            self.draw_frames.append((snake_frame, position))
            
        for frame, position in self.draw_frames:
            frame.grid(column = position[0], row = position[1])

        
if __name__ == '__main__':
    Game()
